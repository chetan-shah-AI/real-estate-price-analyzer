from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from get_area_square_footage import get_area_footage_data
from URLs import urls_zoopla



# url = "https://www.zoopla.co.uk/for-sale/property/london/?q=london&search_source=home"



# list_cities = ["Leicester", "Birmingham", "London", "Glasgow", "Edinburgh", "Newcastle", "Bristol", "Manchester", "Notingham", "Sheffield", "Liverpool", "Cardiff", "Belfast", "Leeds", "Southampton"]
list_cities = ["Belfast"]

for city in list_cities:
    time.sleep(3)
    
    # Setup driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.get(urls_zoopla[city])

    # wait for page to load
    time.sleep(5)

    # Accept cookies if popup appears
    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        time.sleep(2)
    except:
        pass

    properties = []

    # cards = driver.find_elements(By.CSS_SELECTOR, "[class='Listings_listingRow__bBao4']")
    cards = driver.find_elements(By.CSS_SELECTOR, "[class='layout_layoutGridSlim__aaK4p layout_isPremiumOrFeatured__zP3do fjlmpi5']")


    print(f"Found {len(cards)} properties on the page.")

    print(cards)



    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "[class='summary_address__Y3xS6 fjlmpi9']").text
        except:
            title = None

        try:
            location = card.find_element(By.CSS_SELECTOR, "[class='summary_address__Y3xS6 fjlmpi9']").text
        except:
            location = None


        try:
            price = card.find_element(By.CSS_SELECTOR, "[class='price_priceText__TArfK fjlmpi6']").text
        except:
            price = None

        try:
            property_type = card.find_element(By.CSS_SELECTOR, "[class='_6zgk9i0 _6zgk9i4 fjlmpib']").text
        except:
            property_type = None

        try:
            beds_baths_reception_area = card.find_elements(By.CSS_SELECTOR, "[class='amenities_amenityItemSlim__CPhtG']")
        except:
            beds_baths_reception_area = None

        try:
            # beds = card.find_element(By.CSS_SELECTOR, "[class='amenities_amenityItemSlim__CPhtG']").text
            beds = beds_baths_reception_area[0].text
        except:
            beds = None
        
        try:
            # bathrooms = card.find_element(By.CSS_SELECTOR, "[class='amenities_amenityItemSlim__CPhtG']").text
            bathrooms = beds_baths_reception_area[1].text
        except:
            bathrooms = None

        try:
            link = card.find_elements(By.TAG_NAME, "a")[0].get_attribute("href")
            # link = card.find_element(By.CSS_SELECTOR, "[class='lib_detailsPageLink__U9Wqi']").text
        except:
            link = None

        try:
            # area = card.find_element(By.CSS_SELECTOR, "[class='amenities_amenityItemSlim__CPhtG']").text
            area = beds_baths_reception_area[3].text
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
    df.to_csv(f"zoopla_properties_{city}.csv", index=False)