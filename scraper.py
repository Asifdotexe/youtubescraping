# importing required libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# intializing a web driver instance to control the chrome window
# in headless mode
options = Options()
options.add_argument('--headless=new')

# creating the driver
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)
# scraping logic

# close the browser to free up resources
driver.quit()
