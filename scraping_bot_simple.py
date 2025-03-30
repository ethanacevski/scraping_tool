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

#------------------------------------------------------------------------------
"""Importing Libaries throughout the project"""
import time
import csv
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#------------------------------------------------------------------------------
"""Defining paths and global variables"""
# Replace w/ own path to chromedrive -> See README
PATH = "/Users/ethanacevski/Applications/chromedriver"
service = Service(PATH)
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

# Website URL provided by OIF
website_url = (
    "https://www.booking.com/searchresults.en-gb.html?"
    "ss=Australia&ssne=Australia&ssne_untouched=Australia&"
    "label=gen173nr-1FCAEoggI46AdIM1gEaA-IAQGYAQm4AQfIAQzYAQHoAQH4AQ2IAgGoAgO4"
    "AqLR4r4GwAIB0gIkZjgwMmJmZDItYzYwNS00YmNiLTliYjEtYTNkMWYyZGQ5Yjc32AIG4AIB&"
    "sid=03bbe5a794b64ebe64733f727710b62d&aid=304142&lang=en-gb&sb=1&"
    "src_elem=sb&src=searchresults&dest_id=13&dest_type=country&"
    "checkin=2026-02-01&checkout=2026-02-02&group_adults=2&no_rooms=1&"
    "group_children=0"
)

# Setting driver
driver.get(website_url)
search_number = 0   # User input -> No. of properites wanting to be scraped

#------------------------------------------------------------------------------
"""Loop asking user to input the desired number of properties"""
#  - loop continues until a numeric value is provided
#  - if 'max' is typed then all properties are scrapped
while True:
    user_input = input("Enter the number of listings you want to scrape: ")
    try:
        if(user_input == 'max'):
            search_number = 9999999999
            break
        search_number = int(user_input)  # Check if input is an integer
        break
    except ValueError:
        print("That's not a valid number. Please try again.")


#------------------------------------------------------------------------------
"""Process total results and updating search number respectively"""
# Wait for listings to load on Website
wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR, 'div[data-testid="property-card"]'
)))

# Finding total number of listings available to ensure scraping cap
property_found = driver.find_element(
    By.XPATH,
    '/html/body/div[4]/div/div/div/div[2]/div[3]/div[2]/div[1]/h1'
).text
property_count = int(property_found.split(' ')[1].replace(',', ''))

# Ensuring the desired number of scrapings is within the total available
if property_count < search_number:
    print(f"There was only {property_count} available, now scraping for all "
          f"{property_count}")
    search_number = property_count
else:
    print(f"Now scraping for {search_number} properties")


#------------------------------------------------------------------------------
""" Scrolls the page in steps like a human would """

def human_like_scroll(driver, pause_range=(0.8, 1.8), max_pause=3):
    # Mimicking human scrolling w/ randomised delays and upward nudges
    # Dynamically adjusts search_number if no more listings load

    global search_number  # So we can update the outer variable

    last_height = driver.execute_script("return document.body.scrollHeight")
    same_height_count = 0

    while True:
        for _ in range(random.randint(2, 5)):
            scroll_by = random.randint(400, 700) # Increase to speed up scroll
            driver.execute_script(f"window.scrollBy(0, {scroll_by});")
            time.sleep(random.uniform(*pause_range))

        if random.random() < 0.3:
            driver.execute_script("window.scrollBy(0, -200);")
            time.sleep(random.uniform(0.5, 1.0))

        try:
            load_more = driver.find_element(
                By.XPATH,
                '//button[.//span[text()="Load more results"]]'
            )
            if load_more.is_displayed():
                listings = driver.find_elements(
                    By.CSS_SELECTOR, 'div[data-testid="property-card"]'
                )
                print(f"Clicking 'Load more' with {len(listings)} listings")
                driver.execute_script("arguments[0].click();", load_more)
                time.sleep(random.uniform(2, max_pause))
        except:
            pass

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            same_height_count += 1
        else:
            same_height_count = 0

        last_height = new_height

        listings = driver.find_elements(
            By.CSS_SELECTOR, 'div[data-testid="property-card"]'
        )

        if len(listings) >= search_number:
            break

        # In case Book.com doesn't let us view all listings on main page
        # then exit and update with scraped no. of properties
        if same_height_count >= 3:  
            print("No more listings loading. Adjusting search_number...")
            search_number = len(listings)
            break

    return listings[:search_number]


listings = human_like_scroll(driver)
print(f"Final listings scraped: {len(listings)}")


#------------------------------------------------------------------------------
""" Extraction of desired values from scraped data"""

results = []    # List to hold desired values from each property

for accomodation in listings:
    # Property title
    try:
        title = accomodation.find_element(
            By.CSS_SELECTOR, 'div[data-testid="title"]'
        ).text
    except:
        title = None

    # Address of Property
    try:
        address = accomodation.find_element(
            By.CSS_SELECTOR, 'span[data-testid="address"]'
        ).text
    except:
        address = None

    # Headline room type
    try:
        h_room_type = accomodation.find_element(
            By.CSS_SELECTOR, 'h4.abf093bdfe.e8f7c070a7'
        ).text
    except:
        h_room_type = None

    # Headline room cost
    try:
        h_room_cost_element = accomodation.find_element(
            By.CSS_SELECTOR,
            'span[data-testid="price-and-discounted-price"]'
        ).text
        h_room_cost = h_room_cost_element.split(' ')[1].replace(',', '')
    except:
        h_room_cost = "N/A - Cost"

    # Review score out of 5
    try:
        review_score_element = accomodation.find_element(
            By.CSS_SELECTOR,
            'div.a3b8729ab1.d86cee9b25 div.ac4a7896c7'
        ).text
        review_score = review_score_element.split(' ')[1]
    except:
        review_score = None

    # Total number of reviews received
    try:
        total_reviews_element = accomodation.find_element(
            By.CSS_SELECTOR,
            'div.abf093bdfe.f45d8e4c32.d935416c47'
        ).text
        total_reviews = total_reviews_element.split(" ")[0]
    except:
        total_reviews = None
    
    # Appending each property to results list
    results.append([
        title, address, h_room_type,
        h_room_cost, review_score, total_reviews
    ])

# Ensuring scraping process is slowed to mimic human interaction
time.sleep(4)   # Increase number in sleep to 999999999 if wanting to 
                # check website
driver.quit()   # Quits window once script it done


#------------------------------------------------------------------------------
"""Exporting results in a csv"""

with open("booking_results.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    # Row headers
    writer.writerow([
        "Index", "Title", "Address", "Headline Room Type",
        "Cost (AUD)", "Review Score", "# of Reviews"
    ])
    for idx, data in enumerate(results, start=1):
        writer.writerow([idx] + data)

print("✅ Process Complete")