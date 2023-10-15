import pandas as pd
df = pd.DataFrame()
df["col1"] = ""
df["col2"] = ""
df["col3"] = ""

df.loc["row1", "col1"] = "v1"
df.loc["row2", "col2"] = "v4"
df.loc["row3", "col3"] = "v9"
print(df)