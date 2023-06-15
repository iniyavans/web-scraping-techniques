import pandas as pd
import re

from pymongo import MongoClient

targetText = "Hello Everyone my name in AI, and my email is ai@mailinator.com and my brother email is aibro@mailinator.com hope you got that. And you get me on https://www.ai.com. My phone number is +919487781351 And I have a credit card sorry debit card, the number is 4249-8830-1348-8298 so everyone sent your savings to this Account or $2000 to $2500, better $4000 is enough, I will take care of your money well. Just kidding. And The Html tags are <h1> and <html>. and I love #000000 Do you unterdatnd? and I hate #111111. Because I leave in a dark. And follow #Iambot in twitter. But I have SSN number it is 000-12-1292 and i was born in 14-06-2023 then try to destry in 17-6-23 and you guys are die in 01-07-2023."

def return_scrap_data():

    scrap_data_details = {}

    scrap_data_detail = []

    htmlTag_pattern = r"<[^>]+>"

    scrap_data_details["html_tags"] = re.findall(htmlTag_pattern, targetText)

    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    scrap_data_details["email_address"] = re.findall(email_pattern, targetText)

    url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"

    scrap_data_details["urls"] = re.findall(url_pattern, targetText)

    date_pattern = r"\b\d{1,2}-\d{1,2}-\d{2,4}\b"

    scrap_data_details["dates"] = re.findall(date_pattern, targetText)

    phoneNumber_pattern = r"(?:\+91)?(\d{10})"

    scrap_data_details["phone_number"] = re.findall(phoneNumber_pattern, targetText)

    hexadecimal_pattern = r"#[0-9a-fA-F]{6}\b"

    scrap_data_details["hexadecimal_values"] = re.findall(hexadecimal_pattern, targetText)

    SSN_pattern = r"\b\d{3}-\d{2}-\d{4}\b"

    scrap_data_details["SSN"] = re.findall(SSN_pattern, targetText)

    creditCard_pattern = r"\b\d{4}-\d{4}-\d{4}-\d{4}\b"

    scrap_data_details["credit_card"] = re.findall(creditCard_pattern, targetText)

    currency_pattern = r"\$\d+(?:\.\d{2})?"

    scrap_data_details["currency"] = re.findall(currency_pattern, targetText)

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
collection = db["Text Pattern Matching"]

'''   Store the All the Infromation from the scrapped_data   '''

collection.insert_many(scrap_data_detail)

'''   Store the specific Infromation from the scrapped_data   '''

filtered_data = [
    {"email_address": item["email_address"], "phone_number": item["phone_number"]} for item in scrap_data_detail
]

collection.insert_many(filtered_data)

'''   Export the scrapped details into the CSV File   '''

'''   Store the All the Infromation from the scrapped_data   '''

# Change the data struture to the table formate by using pandas library
DataFrame = pd.DataFrame(scrap_data_detail)

# Export data as a CSV file and index=False means we avoid the default table content from DataFrame
DataFrame.to_csv("Text Pattern Matching all data.csv", index=False)

'''   Store the specific Infromation from the scrapped_data   '''

# Change the data struture to the table formate by using pandas library
DataFrame = pd.DataFrame(scrap_data_detail, columns=["email_address", "phone_number"])

# Export data as a CSV file and index=False means we avoid the default table content from DataFrame
DataFrame.to_csv("Text Pattern Matching specific data.csv", index=False)

