from bs4 import BeautifulSoup
import requests


def get_vehicle_stats(plate: str) -> None:
    """
    :param plate: Entering license plate to get information about.
    :return: None
    """
    try:

        page = requests.get('https://totalcarcheck.co.uk/FreeCheck?regno=' + plate)
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
