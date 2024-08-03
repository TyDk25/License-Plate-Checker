import requests
import chromedriver_autoinstaller
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging


class VehicleStats:
    def __init__(self, plate):
        self.plate = plate

    def get_vehicle_stats(self) -> None:
        """
        Gets vehicle statistics from website
        :return: None
        """
        try:

            page = requests.get('https://totalcarcheck.co.uk/FreeCheck?regno=' + self.plate)
            soup = BeautifulSoup(page.content, 'html.parser')
            stats = soup.find_all(class_='certData certBasic')
            manufacturer = stats[0].text
            model = stats[1].text
            fuel_type = stats[6].text
            litre = stats[7].text

            bhp = [
                td.find_next_sibling('td').find('span').text.strip()
                for td in soup.find_all('td', class_='certLabel')
                if td.find('label').text.strip() == "BHP"
            ]

            try:
                zero_to_60 = 'Secs'
                for td in soup.find_all('td', class_='certData certBasic'):
                    span = td.find('span')
                    if span and zero_to_60 in span.get_text():
                        seconds = span.get_text()

                print(f"Manufacturer: {manufacturer}")
                print(f"Model: {model}")
                print(f"Fuel Type: {fuel_type}")
                for numbers in bhp:
                    print(f'BHP:\n{numbers}')
                print(f'\nLitre:{litre}')
                print(f'0-60:\n{seconds}')

            except UnboundLocalError:
                print('0-60 Seconds are not available.')

            years = [
                td.find_next_sibling('td').find('span').text.strip()
                for td in soup.find_all('td', class_='certLabel')
                if td.find('label').text.strip() == "Year of Manf."
            ]

            for year in years:
                print(f'\nYear:\n{year}')

        except IndexError:
            print('This license plate does not exist.')


class RemapInfo:

    def __init__(self, plate):
        self.plate = plate
        # Set up Chrome options
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        # Initialize the Chrome driver
        self.driver = webdriver.Chrome(options=options)
        # Navigate to the website
        self.driver.get(r'https://www.celtictuning.co.uk/')

    def get_remap_info(self) -> str:
        """
            Gets figure on what BHP will be after remap.
            :return str: Remapped BHP.
            """
        try:

            license_plate_enter = self.driver.find_element(By.CLASS_NAME, 'mod_ctvc-dvlaCheck')
            license_plate_enter.send_keys(self.plate)

            remap_info = self.driver.find_element(By.ID, 'mod_ctvc-dvla-search-submit')
            remap_info.click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "ctvc-title")))

            page_source = self.driver.page_source

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

        except TimeoutException as e:
            logging.error(f'Timeout Error Occurred Check License Plate: {self.plate} Is Correct.'
                          f': {e.__repr__()}')


        finally:
            self.driver.close()

    def get_remap_potential(self) -> None:
        """
        Shows what stock BHP is with BHP after map.
        :return: None
        """
        page = requests.get('https://totalcarcheck.co.uk/FreeCheck?regno=' + self.plate)
        soup = BeautifulSoup(page.content, 'html.parser')
        remap = self.get_remap_info()
        stock_bhp = [
            td.find_next_sibling('td').find('span').text.strip()
            for td in soup.find_all('td', class_='certLabel')
            if td.find('label').text.strip() == "BHP"
        ]

        for numbers in stock_bhp:
            stock_bhp_number = numbers

            print(f'Stock BHP -> {stock_bhp_number}: After Remap: -> {remap} BHP')


if __name__ == '__main__':
    RemapInfo('SC06LDM').get_remap_potential()
