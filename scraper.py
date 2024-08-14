# importing required libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
import json
import re

# intializing a web driver instance to control the chrome window
# in headless mode
options = Options()
options.add_argument('--headless=new')

# creating the driver
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)

# url of target page
url = "https://youtu.be/9mwDag2F180?si=RaU2k_X4UH694p7W"
# visit the target page in the controlled browser
driver.get(url)

try:
    # wait up to 15 seconds for the consent dialog to show up
    consent_overlay = WebDriverWait(driver,15).until(
        EC.presence_of_element_located((By.ID,'dialog'))
    )

    # select the consent option buttons
    consent_buttons = consent_overlay.find_element(By.CSS_SELECTOR,
                    '.eom-buttons button.yt-spec-button-shape-next')
    # click on accept (consent) button
    if len(consent_buttons) > 1:
        # retrieve and click 'Accept all' button
        accept_all_button = consent_buttons[1]
        accept_all_button.click()
except TimeoutException:
    print('Cookie model missing')

# wait for Youtube to load the page data
WebDriverWait(driver,15).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR,'h1.ytd-watch-metadata')))

# intitalize the dictionary to contain the scraped data
video = {}

# scraping logic

# getting the title 
title = driver.find_element(
    By.CSS_SELECTOR,"h1.ytd-watch-metadata").text

# creating dictionary to store channel details
channel = {}

# extracting channel info attributes
channel_element = driver.find_element(
            By.ID,'owner')

channel_url = channel_element.find_element(
            By.CSS_SELECTOR, 'a.yt-simple-endpoint') \
            .get_attribute('href')

channel_name = channel_element.find_element(
            By.ID,'channel-name').text

channel_image = channel_element.find_element(
            By.ID,'img').get_attribute("src")

channel_subs = channel_element.find_element(
    By.ID,'owner-sub-count')\
    .text.replace(' subscribers','')

# storing the information
channel['url'] = channel_url
channel['name'] = channel_name
channel['image'] = channel_image
channel['subs'] = channel_subs

# click the description section to expand it
driver.find_element(By.ID, 'description-inline-expander').click()

info_container_elements  = driver.find_elements(By.CSS_SELECTOR,
                                                '#info-container span')
# scraping the number of views
views = info_container_elements[0].text.replace(' views','')
# scraping the publish date
publication_date = info_container_elements[2].text

# scraping the description section
description = driver.find_element(
    By.CSS_SELECTOR, 
    '#description-inline-expander .ytd-text-inline-expander span')\
    .text

# scraping the number of likes
likes = driver \
    .find_element(By.CSS_SELECTOR, '.yt-spec-button-shape-next__button-text-content').text

# Sample HTML element
# html_element = '<div class="yt-spec-button-shape-next__button-text-content">7.6K</div>'
# # Use regex to extract the value within the <div> tag
# likes = re.search(r"([\d.]+)", html_element).group()

# likes = WebDriverWait(driver, 10) \
#     .until(EC.presence_of_element_located(
#         (By.ID, 'segmented-like-button')))

# insert the information into the video dictionary
video['url'] = url
video['title'] = title
video['channel'] = channel
video['views'] = views
video['likes'] = likes
video['publication_date'] = publication_date
video['description'] = description

driver.close()

# exporting the scraped that into JSON
# path = "".json"
with open("video.json",'w') as f:
    json.dump(video,f)