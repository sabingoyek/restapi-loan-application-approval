import random
import pandas as pd
import sqlite3
import psycopg2
from database import engine

# Read initial house data
df = pd.read_csv('HousePricePrediction.csv')

# Generate is_on_market column
is_on_market_col_data_dic = {
    "is_on_market": []
}

for i in range(0, df.shape[0]):
    if random.randint(0, 1):
        is_on_market_col_data_dic["is_on_market"].append("True")
    else:
        is_on_market_col_data_dic["is_on_market"].append("False")

is_on_market_col = pd.DataFrame(is_on_market_col_data_dic)
# print(is_on_market_col.head())
# print(is_on_market_col.shape[0])
# is_on_market_col.to_csv("is_on_market_col.csv")

# Add is_on_market column to initial data
result = pd.concat([df, is_on_market_col], axis=1)
# print(result.shape[0])
# print(result.head())
# print(result.tail())

# print(result.isnull().sum())
result.dropna(inplace=True)

# print(result.isnull().sum())
# print(f"Shape after removing rows containing null value: {result.shape[0]}")

# rebuild id field because some rows has been droped
result.drop(['id'], axis=1, inplace=True)
id_data_dict = {
    'id': list(range(1, result.shape[0]+1))
}

id_col = pd.DataFrame(id_data_dict)
# print(id_col)


result = pd.concat([id_col, result], axis=1)
print(result.tail())

result.to_csv('HousePrice.csv')

# Connect to PostgreSQL server

# conn = sqlite3.connect('house_db')
conn = engine.connect()

#pd.read_sql("DELETE FROM houses", conn)

result.to_sql("houses", conn, if_exists='append', index=False)


df2 = pd.read_sql("SELECT * FROM houses LIMIT 5", conn)
print(df2)

conn.close()
