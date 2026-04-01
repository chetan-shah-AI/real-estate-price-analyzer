from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from get_area_square_footage import get_area_footage_data
from URLs import urls
from datetime import datetime

import logging
import logger  # ensures config is applied

logger = logging.getLogger(__name__)



# This is URL for properties in Leicester, Leicestershire with price range 50k-15m, any number of bedrooms, added in the last 24 hours
url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchLocation=Leicester%2C+Leicestershire&useLocationIdentifier=true&locationIdentifier=REGION%5E789&radius=10.0&minPrice=50000&maxPrice=15000000&minBedrooms=0&maxBedrooms=10&propertyTypes=detached%2Csemi-detached%2Cterraced&maxDaysSinceAdded=1&_includeSSTC=on"
# url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchLocation=Birmingham&useLocationIdentifier=true&locationIdentifier=REGION%5E162&radius=10.0&minPrice=50000&maxPrice=20000000&minBedrooms=0&maxBedrooms=10&_includeSSTC=on&index=960&sortType=2&channel=BUY&transactionType=BUY&displayLocationIdentifier=Birmingham.html"
# url = "https://www.rightmove.co.uk/property-for-sale/find.html?useLocationIdentifier=true&locationIdentifier=REGION%5E87490&minPrice=50000&maxPrice=20000000&minBedrooms=0&maxBedrooms=10&_includeSSTC=on&index=0&sortType=2&channel=BUY&transactionType=BUY&displayLocationIdentifier=London-87490.html"


list_cities = ["Glasgow", "Edinburgh", "Newcastle", "Bristol", "Manchester", "Notingham", "Sheffield", "Liverpool", "Cardiff", "Belfast", "Leeds", "Southampton"]

logger.info(f"Starting scraping for cities: {list_cities}")
logger.info(f"Scraping started at {datetime.now()}")


t1_overall = time.time()

for city in list_cities:

    t1_city = time.time()

    logger.info(f"Scraping properties for {city}")
    logger.info(f"time: {datetime.now()}")

    time.sleep(3)
    # Setup driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(urls[city])
    except Exception as e:
        print(f"Error loading page for {city}: {e}")
        continue

    # wait for page to load
    time.sleep(5)

    # Accept cookies if popup appears
    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        time.sleep(2)
    except:
        pass

    properties = []

    # cards = driver.find_elements(By.CSS_SELECTOR, "[data-testid='propertyCard']")
    # cards = driver.find_elements(By.CSS_SELECTOR, "[class='PropertyCard_propertyCardInfoSection__ZGLRU']")
    cards = driver.find_elements(By.CSS_SELECTOR, "[class='PropertyCard_propertyCardContainer__VSRSA']")


    print(f"Found {len(cards)} properties on the page.")

    print(cards)

    # TODO Title, Location, price, property type, no of bedrooms, no of bathrooms, area square footage, listing URL



    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "[class='PropertyAddress_addressContainer__yZC__']").text
        except:
            title = None

        try:
            location = card.find_element(By.CSS_SELECTOR, "[class='PropertyAddress_addressContainer__yZC__']").text
        except:
            location = None


        try:
            price = card.find_element(By.CSS_SELECTOR, "[data-testid='property-price']").text
        except:
            price = None

        try:
            property_type = card.find_element(By.CSS_SELECTOR, "[class='PropertyInformation_propertyType__u8e76']").text
        except:
            property_type = None

        try:
            beds = card.find_element(By.CSS_SELECTOR, "[class='PropertyInformation_bedContainer___rN7d']").text
        except:
            beds = None
        
        try:
            bathrooms = card.find_element(By.CSS_SELECTOR, "[class='PropertyInformation_bathContainer__ut8VY']").text
        except:
            bathrooms = None

        try:
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            link = None

        try:
            area = get_area_footage_data(link)
        except:
            area = None

        properties.append({
            "title": title,
            "location": location,
            "price": price,
            "property_type": property_type,
            "bedrooms": beds,
            "bathrooms": bathrooms,
            "area": area,
            "link": link,
        })

    driver.quit()

    df = pd.DataFrame(properties)
    print(df.head())
    df.to_csv(f"RAW_DATA/properties_with_bedrooms_auto_{city.lower()}.csv", index=False)
    t2_city = time.time()
    city_time = t2_city - t1_city

    logger.info(f"completed scraping for {city} at {datetime.now()}")
    logger.info(f"Time taken to scrape {city}: {city_time} seconds")


t2_overall = time.time()
total_time = t2_overall - t1_overall

logger.info(f"Total scraping time: {total_time}")
logger.info(f"Scraping completed at {datetime.now()}")
