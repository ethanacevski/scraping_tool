# Booking.com Scraping Tool

####  By Ethan Acevski
---

#### Set-up

##### Chrome Drive Download
1.  Firstly press the 3 vertical dots in top right of Chrome browser -> Help 
    -> About Google Chrome
    - Shows the current version -> needed for next steps
2.  If your current verison of Chrome is earlier than 115 head to:
    - https://developer.chrome.com/docs/chromedriver/downloads 
3.  If Chrome version 115+ head to:
    - https://googlechromelabs.github.io/chrome-for-testing/
4. Drag the respective Chrome Drive on to your local computer and copy path and
    and replace the `PATH` variable on line 32 of `scraping_bot_simple.py`

##### Changing Flask Port
1. Go to `app.py` and change line 41 to the desired port number

---
#### Running Program
1. Enter `python3 scraping_bot_simple.py` into terminal
2. Once the Booking.com window displays the user will be prompted in the 
    terminal to enter the desired number of properties they wish to scrape
3. To view top 50 cheapest properties, run `python3 app.py`
    - *Note*: This was purposely seperated in case the user only required the
    CSV output. 


