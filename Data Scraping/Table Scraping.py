from pprint import pprint
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient

# Target page URL
base_url = "https://www.coingecko.com/"

# Header details of the website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "ignoreHttpErrors": "True",
    "ignoreContentType": "True"
}

def return_scrap_data():
    # Initiate a expty object with tables variable
    tables = []

    # Scraping the details, used loop for a page. Depends on the loop the pages will get scraped.
    for i in range(1, 2):

        params = {

            'page': i

        }

        url = base_url

        # request.get() method used for a get api call, If you have a header, it should included with a request
        response = requests.get(url, headers=headers, params=params)

        soup = BeautifulSoup(response.content, 'html.parser')

        tables.append(pd.read_html(str(soup))[0])

    master_table = pd.concat(tables)

    master_table = master_table.loc[:, master_table.columns[1:-1]]

    return master_table

# Calls the return_scrap_data function to get the scrapped data and assigned to the scrap_data_detail variable.
scrap_data_detail = return_scrap_data()

# Convert table data to DataFrame values
scrap_data_detail = scrap_data_detail.to_dict(orient="records")

'''   Export the scrapped details into the MongoDB   '''

# Screate a client varibale and assign the MongoClient connect status
client = MongoClient("mongodb://localhost:27017")

# Create or Manage with a existing db with a name of Scrapdata
db = client["Scrapdata"]

# Create or Manage with a existing collection with a name of Table Scrap
collection = db["Table Scraping"]

'''   Store the All the Infromation from the scrapped_data   '''

collection.insert_many(scrap_data_detail)

'''   Store the specific Infromation from the scrapped_data   '''

filtered_data = [
    {"Coin": item["Coin"], "Price": item["Price"]} for item in scrap_data_detail
]

collection.insert_many(filtered_data)

'''   Export the scrapped details into the CSV File   '''

'''   Store the All the Infromation from the scrapped_data   '''

# Change the data struture to the table formate by using pandas library
DataFrame = pd.DataFrame(scrap_data_detail)

# Export data as a CSV file and index=False means we avoid the default table content from DataFrame
DataFrame.to_csv("Table Scraping all data.csv", index=False)

'''   Store the specific Infromation from the scrapped_data   '''

# Change the data struture to the table formate by using pandas library
DataFrame = pd.DataFrame(scrap_data_detail, columns=["Coin", "Price"])

# Export data as a CSV file and index=False means we avoid the default table content from DataFrame
DataFrame.to_csv("Table Scraping Specific data.csv", index=False)