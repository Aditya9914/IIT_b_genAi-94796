import pandas as pd
import pandasql as ps

filepath = r"D:\GEN\D3 UI\demo2\filecsv.csv"
df = pd.read_csv(filepath)

print("Dataframe column Types:")
print(df.dtypes)

print("\nEmp data:")
print(df)

query = """
SELECT job, SUM(sal) AS total_sal
FROM df
GROUP BY job
"""


result = ps.sqldf(query, locals())
print("\nQuery Result:")
print(result)
