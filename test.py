import pandas


df = pandas.read_excel("Invoice.xlsx")
columns = df.iloc[13, :]
df = df.iloc[14:,:]
df.columns = columns
print()