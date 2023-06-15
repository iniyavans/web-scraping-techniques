import requests
import pandas as pd
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Base url of the target website
base_url = "https://www.amazon.in/gp/most-wished-for/books/"

# It is a dictionary containing HTTP headers that will be sent with the requests made to the website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "ignoreHttpErrors": "True",
    "ignoreContentType": "True",
}

# End this

def return_scrap_data():

    # Initiate the empty object as a scrap_data_detail
    scrap_data_detail = []

    # request.get() method used for a get api call, If you have a header, it should included with a request
    response = requests.get(base_url, headers=headers)

    # raise_for_status() is raises an exception if the response status is not in the 200 range.
    response.raise_for_status()

    # Create a BeautifulSoup object with a response content
    doc = BeautifulSoup(response.content, "html.parser")

    # selects all <div> elements with the class "a-cardui".
    products = doc.select("div.a-cardui")

    for x in range(1, 2):

        for product in products:
            # Create a empty dictionary to store the scraped data for each product.
            scrap_data_details = {}

            # Extracts the URL of the product by selecting the <a> element with the class "a-link-normal" and retrieving the value of the "href" attribute.
            scrap_data_details["url"] = product.select_one("a.a-link-normal")["href"]

            # extracts the image URL of the product by selecting the <img> element and retrieving the value of the "src" attribute.
            scrap_data_details["image"] = product.select_one("img")["src"]

            # extracts the name of the product by selecting the <div> element with the class "_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y" and retrieving the inner text.
            scrap_data_details["name"] = product.select_one(
                "div._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"
                ).text.strip()

            # extracts the  ce of the product by selecting the <div> element with the class "a-row" and retrieving the inner text.
            scrap_data_details["Author"] = product.select_one("div.a-row").text.strip()

            # adds the scraped product details to the scrap_data_detail list. witha append() method
            scrap_data_detail.append(scrap_data_details)

    return scrap_data_detail


# Calls the return_scrap_data function to get the scrapped data and assigned to the scrap_data_detail variable.
scrap_data_detail = return_scrap_data()

'''   Export the scrapped details into the MongoDB   '''

# Screate a client varibale and assign the MongoClient connect status
client = MongoClient("mongodb://localhost:27017")

# Create or Manage with a existing db with a name of Scrapdata
db = client["Scrapdata"]

# Create or Manage with a existing collection with a name of API Scrap
collection = db["HTML Parsing"]

'''   Store the All the Infromation from the scrapped_data   '''

collection.insert_many(scrap_data_detail)

'''   Store the specific Infromation from the scrapped_data   '''

filtered_data = [
    {"name": item["name"], "image": item["image"]} for item in scrap_data_detail
]

collection.insert_many(filtered_data)

'''   Export the scrapped details into the CSV File   '''

'''   Store the All the Infromation from the scrapped_data   '''

# Change the data struture to the table formate by using pandas library
DataFrame = pd.DataFrame(scrap_data_detail)

# Export data as a CSV file and index=False means we avoid the default table content from DataFrame
DataFrame.to_csv("HTML_Parsing_all_data.csv", index=False)

'''   Store the specific Infromation from the scrapped_data   '''

# Change the data struture to the table formate by using pandas library
DataFrame = pd.DataFrame(scrap_data_detail, columns=["name", "image"])

# Export data as a CSV file and index=False means we avoid the default table content from DataFrame
DataFrame.to_csv("HTML_Parsing_Specific_data.csv", index=False)
