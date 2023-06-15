import requests
import pandas as pd
from pymongo import MongoClient

def apiScrapping():
    # Headers details of the API
    headers = {"Content-Type": "application/json"}

    # request.get() method used for a get api call, If you have a header, it should included with a request
    response = requests.get("https://reqres.in/api/users?page=2", headers=headers)

    # Assign the response details in a data variable as a json
    data = response.json()

    # Get the specific data object from the API
    data = data["data"]

    # Return the data variable to the function
    return data

# Assign the retured values from a apiScrapping() function and assined to the scrapped_data variable
scrapped_data = apiScrapping()

'''   Export the scrapped details into the MongoDB   '''

# Screate a client varibale and assign the MongoClient connect status
client = MongoClient("mongodb://localhost:27017")

# Create or Manage with a existing db with a name of Scrapdata
db = client["Scrapdata"]

# Create or Manage with a existing collection with a name of API Scrap
collection = db["API Scrap"]

'''   Store the All the Infromation from the scrapped_data   '''

collection.insert_many(scrapped_data)

'''   Store the specific Infromation from the scrapped_data   '''

filtered_data = [
    {"email": item["email"], "first_name": item["first_name"]} for item in scrapped_data
]

collection.insert_many(filtered_data)

'''   Export the scrapped details into the CSV File   '''

'''   Store the All the Infromation from the scrapped_data   '''

# Change the data struture to the table formate by using pandas library
DataFrame = pd.DataFrame(scrapped_data)

# Export data as a CSV file and index=False means we avoid the default table content from DataFrame
DataFrame.to_csv("api_scraping_all_data.csv", index=False)

'''   Store the specific Infromation from the scrapped_data   '''

# Change the data struture to the table formate by using pandas library
DataFrame = pd.DataFrame(scrapped_data, columns=["email", "first_name"])

# Export data as a CSV file and index=False means we avoid the default table content from DataFrame
DataFrame.to_csv("api_scraping_Specific_data.csv", index=False)