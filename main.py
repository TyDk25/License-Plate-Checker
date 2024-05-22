from bs4 import BeautifulSoup
import requests
def get_vehicle_stats(plate: str) -> None:

    try:

        page = requests.get('https://totalcarcheck.co.uk/FreeCheck?regno=' + plate)
        soup = BeautifulSoup(page.content, 'html.parser')
        stats = soup.find_all(class_='certData certBasic')
        manufacturer = stats[0].text if len(stats) > 1 else 'Not Available'
        model = stats[1].text
        fuel_type = stats[6].text
        litre = stats[7].text
        bhp = stats[9].text

        try:
            zero_to_60 = 'Secs'
            for td in soup.find_all('td', class_='certData certBasic'):
                span = td.find('span')
                if span and zero_to_60 in span.get_text():
                    seconds = span.get_text()

            years = [
                td.find_next_sibling('td').find('span').text.strip()
                for td in soup.find_all('td', class_='certLabel')
                if td.find('label') and td.find('label').text.strip() == "Year of Manf."
            ]

            print(f"Manufacturer: {manufacturer}")
            print(f"Model: {model}")
            print(f"Fuel Type: {fuel_type}")
            print(f'BHP:{bhp}')
            print(f"Litre: {litre}")
            print(f'0-60: {seconds}')

            for year in years:
                print(f'\nYear: {year}')

        except UnboundLocalError:
            print('0-60 Seconds do not exist for this car.')

    except IndexError as e:
        print(e.__repr__())
        print('This license plate does not exist.')



get_vehicle_stats('DF16YFE')




