from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_remap_info(plate: str) -> str:
    """
    :param plate: Entering plate to get remap information about
    :return str: Remapped BHP.
    """
    # Install chromedriver
    chromedriver_autoinstaller.install()

    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=options)

    # Navigate to the website
    driver.get(r'https://www.celtictuning.co.uk/')

    license_plate_enter = driver.find_element(By.CLASS_NAME, 'mod_ctvc-dvlaCheck')
    license_plate_enter.send_keys(plate)

    get_remap_info = driver.find_element(By.ID, 'mod_ctvc-dvla-search-submit')
    get_remap_info.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctvc-title")))

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    bhp_div = soup.find_all('div', class_='ctvc_gauge_text')

    bhp_values = [
        div.find('h5').text.strip()
        for div in bhp_div
        if div.find('h5') is not None
    ]

    counter = 0
    for bhp in bhp_values:
        if counter == 1:
            remap = bhp
            break
        counter += 1

    return remap



