""" Part 1 - Booking.com Bot Scraper

1. Booking.com contains a large quantity of listings for Australia, we want to scrape these for the 1st-2nd February 2026 (Search). 
2. Use Selenium (Python) to scrape all listings:
    - Title
    - Address
    - Headline Room Type
    - Cost (AUD)
    - Review Score
    - \# of Reviews
3. Scrape as many listings as you can, however your code should be designed to handle an arbitrary number of listings. Care should be taken to mimic human-like behaviour.
4. Structure your output in a CSV.

"""

"""Selenium Tips:

ID = "id"
NAME = "name"
XPATH = "xpath"
LINK_TEXT = "link text"
PARTIAL_LINK_TEXT = "partial link text"
TAG_NAME = "tag name"
CLASS_NAME = "class name"
CSS_SELECTOR = "css selector"    

# Search "Australia" -> Assuming this is already done by provided website w/ search request
# search_box = driver.find_element(By.ID, ':rh:')
# search_box.clear()
# search_box.send_keys("Australia")
# search_box.send_keys("\n")

"""

import time
import csv
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "/Users/ethanacevski/Applications/chromedriver"
service = Service(PATH)
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)
website_url = "https://www.booking.com/searchresults.en-gb.html?ss=Australia&ssne=Australia&ssne_untouched=Australia&label=gen173nr-1FCAEoggI46AdIM1gEaA-IAQGYAQm4AQfIAQzYAQHoAQH4AQ2IAgGoAgO4AqLR4r4GwAIB0gIkZjgwMmJmZDItYzYwNS00YmNiLTliYjEtYTNkMWYyZGQ5Yjc32AIG4AIB&sid=03bbe5a794b64ebe64733f727710b62d&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=13&dest_type=country&checkin=2026-02-01&checkout=2026-02-02&group_adults=2&no_rooms=1&group_children=0"
driver.get(website_url)


while True:
    user_input = input("Enter the number of listings you want to scrape: ")
    try:
        search_number = int(user_input)  # Use int(user_input) if you only want integers
        break
    except ValueError:
        print("That's not a valid number. Please try again.")


# Wait for listings to load
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="property-card"]')))


# Finding total number of listings available
property_found = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div[3]/div[2]/div[1]/h1').text
property_count = int(property_found.split(' ')[1].replace(',',''))

# Ensuring the desired number of scrapings is within the limit of the total properties available
if(property_count<search_number):
    print(f"There was only {property_count} available, now scraping for all {property_count}")
    search_number = property_count
else:
    print(f"Now scraping for {search_number} properties")


def human_like_scroll(driver, pause_range=(0.8, 1.8), max_pause=3):
    """ Scrolls the page in steps like a human would """
    last_height = driver.execute_script("return document.body.scrollHeight")
    same_height_count = 0

    while True:
        # Scroll in small steps
        for _ in range(random.randint(2, 5)):
            scroll_by = random.randint(400, 700)
            driver.execute_script(f"window.scrollBy(0, {scroll_by});")
            time.sleep(random.uniform(*pause_range))

        # Occasionally scroll up a little
        if random.random() < 0.3:
            driver.execute_script("window.scrollBy(0, -200);")
            time.sleep(random.uniform(0.5, 1.0))

        # Click "Show more" if available
        try:
            load_more = driver.find_element(By.XPATH, '//button[.//span[text()="Load more results"]]')
            if load_more.is_displayed():
                print("🧩 Found 'Load more results' button — clicking")
                driver.execute_script("arguments[0].click();", load_more)
                time.sleep(random.uniform(2, max_pause))
        except:
            pass  # Button not found or already clicked

        # Check if height changed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            same_height_count += 1
        else:
            same_height_count = 0

        last_height = new_height

        # Get current listings
        listings = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
        print(f"📦 Listings collected: {len(listings)}")

        if len(listings) >= search_number:
            break

    return listings[:search_number]

listings = human_like_scroll(driver)
print(f"✅ Final total listings found: {len(listings)}")

results = []

for x in listings:  # Adjust range for more listings
    try:
        title = x.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text
        # print(title)
    except:
        title = None
   
    # Address
    try:
        address = x.find_element(By.CSS_SELECTOR, 'span[data-testid="address"]').text
        # print(f"address found - {address}")
    except:
        address = None
    

    # Headline Room Type
    try:
        h_room_type = x.find_element(By.CSS_SELECTOR, 'h4.abf093bdfe.e8f7c070a7').text
        # print(f"headline room type found - {h_room_type}")
    except:
        h_room_type = None
        
    # Cost
    try:
        h_room_cost_element = x.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text
        h_room_cost = h_room_cost_element.split(' ')[1].replace(',','')
        print(f"headline room cost found - {h_room_cost}")
    except:
        h_room_cost = "N/A - Cost"

    # Review Score
    try:
        review_score_element = x.find_element(By.CSS_SELECTOR, 'div.a3b8729ab1.d86cee9b25 div.ac4a7896c7').text
        review_score = review_score_element.split(' ')[1]
        # print(f"review score found - {review_score}")
    except:
        print("review score fail")
        review_score = None

    # No. of Reviews
    try:
        total_reviews_element = x.find_element(By.CSS_SELECTOR, 'div.abf093bdfe.f45d8e4c32.d935416c47').text
        total_reviews = total_reviews_element.split(" ")[0]
        # print(f"No. of Reviews found - {total_reviews}")
    except:
        total_reviews = None
        
    # Appending scraped data for each property to a list
    results.append([title, address, h_room_type, h_room_cost, review_score, total_reviews])
    

# Keep browser open for 2 seconds
time.sleep(4)
for x in enumerate(results):
    print(f"{x} - {results[0]}")

# Optional: Close the browser afterwards
driver.quit()

# Outputting results into a CSV
with open("booking_results.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # Write header row
    writer.writerow([
        "Index", "Title", "Address", "Headline Room Type",
        "Cost (AUD)", "Review Score", "# of Reviews"
    ])

    # Write each result row with a counter starting at 1
    for idx, data in enumerate(results, start=1):
        writer.writerow([idx] + data)  # Prepend index to each row