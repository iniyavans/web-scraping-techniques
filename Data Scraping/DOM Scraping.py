import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import pandas as pd

def domScrapping():
    # Initiate the chrome options object
    chrome_options = Options()

    # Control the behavior of web browser after the session end.
    chrome_options.add_experimental_option("detach", True)

    # Run the webdriver with headless mode
    chrome_options.add_argument("--headless")

    # Initiate the Webdriver as a chrome driver and declated with a driver object
    driver = webdriver.Chrome(options=chrome_options)

    # Get the mentioned URL
    driver.get("https://www.flipkart.com/q/Anime-back-cover")

    # Maximize the browser window to maximum level
    driver.maximize_window()
    # Initiate the webdriver wait with 20 sec, Now the driver didn't throw exception until 20 sec
    wait = WebDriverWait(driver, 20)

    # Wait until the target element precent into the website
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@class = '_4ddWXP']/a[@class = 's1Q9rs']")
        )
    )

    # Assign the Available elements into the elements varibale
    elements = driver.find_elements(
        By.XPATH, "//div[@class = '_4ddWXP']/a[@class = 's1Q9rs']"
    )

    # Initialize the empty object
    scrap_data_detail = []

    for element in elements:

        # Initialize the empty aray
        scrap_data_details = {}

        # Assign the title attribute value into name key
        scrap_data_details["name"] = element.get_attribute("title")

        # Assign the href attribute value into link key
        scrap_data_details["link"] = element.get_attribute("href")

        # Append all the data into the scrap_data_details array
        scrap_data_detail.append(scrap_data_details)

    # Quit the browser
    driver.quit()

    # Return the scrap_data_detail[] object
    return scrap_data_detail

# Assign the retured values from a domScrapping() function and assined to the scrapped_data variable
scrapped_data = domScrapping()

'''   Export the scrapped details into the MongoDB   '''

# Screate a client varibale and assign the MongoClient connect status
client = MongoClient("mongodb://localhost:27017")

# Create or Manage with a existing db with a name of Scrapdata
db = client["Scrapdata"]

# Create or Manage with a existing collection with a name of Dom Scrap
collection = db["Dom Scrap"]

'''   Store the All the Infromation from the scrapped_data   '''

collection.insert_many(scrapped_data)

'''   Store the specific Infromation from the scrapped_data   '''

filtered_data = [
    {"name": item["name"]} for item in scrapped_data
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
DataFrame = pd.DataFrame(scrapped_data, columns=["name"])

# Export data as a CSV file and index=False means we avoid the default table content from DataFrame
DataFrame.to_csv("api_scraping_Specific_data.csv", index=False)
