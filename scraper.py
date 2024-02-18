# importing required libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException

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
url = "https://youtu.be/ED_lz73y5Fc?si=PM6BVDKyLIVkYuEM"
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

driver.close()