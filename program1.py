def main():
    sentence = input("Enter a sentence:")
    num_char = len(sentence)

    word = sentence.split()
    num_words = len(word)
    
    # Count vowels
    vowels = "aeiouAEIOU"
    num_vowels = sum(1 for char in sentence if char in vowels)
    
    # Display results
    print(f"Number of characters: {num_char}")
    print(f"Number of words: {num_words}")
    print(f"Number of vowels: {num_vowels}")

if __name__ == "__main__":
    main()