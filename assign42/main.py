import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime


DATA_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_CSV = os.path.join(DATA_DIR, "users.csv")
USERFILES_CSV = os.path.join(DATA_DIR, "userfiles.csv")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")


# ---------- STORAGE SETUP ----------
def ensure_storage():
    os.makedirs(UPLOADS_DIR, exist_ok=True)

    if not os.path.exists(USERS_CSV):
        pd.DataFrame(
            columns=["userid", "username", "password_hash", "created_at"]
        ).to_csv(USERS_CSV, index=False)

    if not os.path.exists(USERFILES_CSV):
        pd.DataFrame(
            columns=["userid", "original_name", "saved_path", "uploaded_at"]
        ).to_csv(USERFILES_CSV, index=False)


# ---------- AUTH HELPERS ----------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_users():
    return pd.read_csv(USERS_CSV)


def save_user(username: str, password: str):
    users = load_users()

    if username in users["username"].values:
        return False, "Username already exists"

    userid = int(users["userid"].max()) + 1 if not users.empty else 1
    pw_hash = hash_password(password)

    # ✅ FIX: use loc instead of append
    users.loc[len(users)] = {
        "userid": userid,
        "username": username,
        "password_hash": pw_hash,
        "created_at": datetime.now().isoformat()
    }

    users.to_csv(USERS_CSV, index=False)
    return True, "User registered successfully"


def authenticate(username: str, password: str):
    users = load_users()

    if username not in users["username"].values:
        return False, "User not found"

    row = users[users["username"] == username].iloc[0]
    if row["password_hash"] == hash_password(password):
        return True, int(row["userid"])

    return False, "Invalid password"


# ---------- FILE TRACKING ----------
def record_upload(userid: int, original_name: str, saved_path: str):
    df = pd.read_csv(USERFILES_CSV)

    # ✅ FIX: use loc instead of append
    df.loc[len(df)] = {
        "userid": userid,
        "original_name": original_name,
        "saved_path": saved_path,
        "uploaded_at": datetime.now().isoformat()
    }

    df.to_csv(USERFILES_CSV, index=False)


def get_user_files(userid: int):
    df = pd.read_csv(USERFILES_CSV)
    return df[df["userid"] == userid]


# ---------- STREAMLIT APP ----------
def main():
    ensure_storage()

    if "user" not in st.session_state:
        st.session_state.user = None

    st.sidebar.title("Menu")

    if not st.session_state.user:
        choice = st.sidebar.selectbox("Choose", ["Home", "Login", "Register"])
    else:
        choice = st.sidebar.selectbox(
            "Choose", ["Explore CSV", "See history", "Logout"]
        )

    st.title("CSV Explorer App")

    if choice == "Home":
        st.write("Welcome! Please Login or Register from the sidebar to begin.")

    elif choice == "Register":
        st.header("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            ok, msg = save_user(username, password)
            st.success(msg) if ok else st.error(msg)

    elif choice == "Login":
        st.header("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pw")

        if st.button("Login"):
            ok, res = authenticate(username, password)
            if ok:
                st.session_state.user = {
                    "userid": res,
                    "username": username
                }
                st.success("Logged in successfully")
            else:
                st.error(res)

    elif choice == "Logout":
        st.session_state.user = None
        st.success("Logged out")

    elif choice == "Explore CSV":
        st.header("Explore CSV")
        st.write(f"Logged in as: **{st.session_state.user['username']}**")

        uploaded = st.file_uploader("Upload a CSV", type=["csv"])
        if uploaded is not None:
            saved_name = (
                f"user{st.session_state.user['userid']}_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_"
                f"{uploaded.name}"
            )
            save_path = os.path.join(UPLOADS_DIR, saved_name)

            with open(save_path, "wb") as f:
                f.write(uploaded.getbuffer())

            record_upload(
                st.session_state.user["userid"],
                uploaded.name,
                save_path
            )

            st.success("File uploaded successfully")
            df = pd.read_csv(save_path)
            st.dataframe(df)

        files_df = get_user_files(st.session_state.user["userid"])
        if not files_df.empty:
            selected = st.selectbox(
                "Or select an uploaded file",
                files_df["saved_path"].tolist()
            )
            if st.button("Load selected"):
                df = pd.read_csv(selected)
                st.dataframe(df)

    elif choice == "See history":
        st.header("Upload History")
        st.write(f"Logged in as: **{st.session_state.user['username']}**")

        files_df = get_user_files(st.session_state.user["userid"])
        if files_df.empty:
            st.info("No uploads yet.")
        else:
            st.dataframe(files_df)


if __name__ == "__main__":
    main()
