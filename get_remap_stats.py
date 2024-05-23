import requests
from bs4 import BeautifulSoup
from remap_info import get_remap_info


def get_remap_potential(plate) -> None:
    """
       :param plate: Entering license plate to get information about.
       :return: None
       """
    page = requests.get('https://totalcarcheck.co.uk/FreeCheck?regno=' + plate)
    soup = BeautifulSoup(page.content, 'html.parser')
    remap = get_remap_info(plate)
    stock_bhp = [
        td.find_next_sibling('td').find('span').text.strip()
        for td in soup.find_all('td', class_='certLabel')
        if td.find('label').text.strip() == "BHP"
    ]

    for numbers in stock_bhp:
        stock_bhp_number = numbers

    print(f'Stock BHP -> {stock_bhp_number}: After Remap: -> {remap} BHP')


get_remap_potential()
