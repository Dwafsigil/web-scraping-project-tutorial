# Import dependencies
# import os
# from bs4 import BeautifulSoup
import requests
# import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import io
import pandas as pd
import numpy as np

# Install dependencies into the terminal
# pip install pandas requests lxml 

# Fetch the webpage
url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_anime_films"
# Websites think the request is a bot so need header
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"} # Look into later
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code != 200:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    # exit()
else:
    print("RESPONSE STATUS IS: ", response.status_code)

    # Extract tables with pandas
html = io.StringIO(response.text)  # Convert the HTML to a text file

# read_html() returns a list of DataFrames
tables = pd.read_html(html) # Scans for <table> tags and converts it into pandas DataFrame. Built to only parse for <table> default behavior
print(f"{len(tables)} tables were found.") # Checks the length of "tables" variable

# Inspect the first table
df = tables[0]

# Remove an unwanted column, one time use?
df.drop(columns=['Ref.'], inplace=True) 

# Rename for usability
df.columns = ["Name", "Revenue", "Year", "Format"]

# Remove unwanted characters in columns, specifically revenue
df["Revenue"] = df["Revenue"].str.replace("$", "", regex=False).replace(",","",regex=True).astype(int) # Interprets the $ sign as a literal string not a regular expression symbol

# print(df)

# Storing Data into a databse for query purposes
# conn = sqlite3.connect("top_japanese_films.db") # Opens a connection to SQLite database file

# # Create the table in SQLite
# df.to_sql("top_films", conn, if_exists="replace", index=False)
# cursor = conn.cursor() # Gets a curser object, cursor is basically a pen that writes what to do for the table

# cursor.execute("SELECT * FROM top_films") # Returns all rows from the table and loads results into the cursor
# print("Rows inserted:", cursor.fetchall()) # Retrieves entries

# Commited database changes and closed the connection
# conn.commit()
# conn.close()

# Visualize the Data

top10 = df.head(10).copy() # Explicitly define copy so no warnings
top10["Revenue"] = top10["Revenue"] / 1000000
plt.figure(figsize=(14, 8))
sns.barplot(data=top10, x="Revenue", y="Name", hue="Name", palette="magma", legend=False)
plt.title("Top 10 Grossing Japanese Films")
plt.xlabel("Revenue (Millions)")
plt.xticks(np.arange(0, 501, 50))  # tick marks every 10
plt.ylabel("Film")
plt.tight_layout()
plt.savefig("top10.png", dpi=200, bbox_inches="tight")
