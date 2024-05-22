from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
# Install chromedriver
chromedriver_autoinstaller.install()

# Set up Chrome options
options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True)

# Initialize the Chrome driver
driver = webdriver.Chrome(options=options)

# Navigate to the website
driver.get(r'https://www.celtictuning.co.uk/')

license_plate_enter = driver.find_element(By.CLASS_NAME, 'mod_ctvc-dvlaCheck')
license_plate_enter.send_keys('Sc06LMM')

get_remap_info = driver.find_element(By.ID, 'mod_ctvc-dvla-search-submit')
get_remap_info.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctvc-title")))

current_url = driver.current_url
print(f"Current URL: {current_url}")

# Get the page source after the elements are loaded
page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')

bhp_div = soup.find_all('div', class_='ctvc_gauge_text')
