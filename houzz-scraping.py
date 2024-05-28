import requests
from bs4 import BeautifulSoup
import json
import csv
import os

GO_ON = True
NUMBER = 15
LAST_NUMBER = 4980

while True:
    url = f'https://www.houzz.com/professionals/general-contractor/ontario-ca-probr0-bo~t_11786~r_6093943?fi={NUMBER}'
    print(f"<<URL NUMBER: {NUMBER}>>")



    response = requests.get(url)

    if response.status_code == 200:
        page_content = response.content

        # BeautifulSoup object mein content parse karna
        soup = BeautifulSoup(page_content, 'html.parser')

        # <script> tag ka content nikalna
        script_tags = soup.find_all('script', type='application/ld+json')

        # CSV file ko write karne ke liye ya read karne ke liye nayi file open karna
        csv_file_path = 'houzz-info.csv'
        file_exists = os.path.isfile(csv_file_path)

        with open(csv_file_path, 'a+', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Telephone', 'Image', 'StreetAddress', 'AddressLocality', 'AddressRegion', 'PostalCode', 'AddressCountry']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # If file exists and is not empty, do not write header again
            if file_exists and os.stat(csv_file_path).st_size != 0:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            else:
                writer.writeheader()

            # JSON data extract karke CSV mein likhna
            for script_tag in script_tags:
                json_data_list = json.loads(script_tag.string)
                if isinstance(json_data_list, list):
                    for json_data in json_data_list:
                        if json_data.get('@type') == 'LocalBusiness':
                            writer.writerow({'Name': json_data.get('name', ''),
                                             'Telephone': json_data.get('telephone', ''),
                                             'Image': json_data.get('image', ''),
                                             'StreetAddress': json_data.get('address', {}).get('streetAddress', ''),
                                             'AddressLocality': json_data.get('address', {}).get('addressLocality', ''),
                                             'AddressRegion': json_data.get('address', {}).get('addressRegion', ''),
                                             'PostalCode': json_data.get('address', {}).get('postalCode', ''),
                                             'AddressCountry': json_data.get('address', {}).get('addressCountry', '')})
                else:
                    if json_data_list.get('@type') == 'LocalBusiness':
                        writer.writerow({'Name': json_data_list.get('name', ''),
                                         'Telephone': json_data_list.get('telephone', ''),
                                         'Image': json_data_list.get('image', ''),
                                         'StreetAddress': json_data_list.get('address', {}).get('streetAddress', ''),
                                         'AddressLocality': json_data_list.get('address', {}).get('addressLocality', ''),
                                         'AddressRegion': json_data_list.get('address', {}).get('addressRegion', ''),
                                         'PostalCode': json_data_list.get('address', {}).get('postalCode', ''),
                                         'AddressCountry': json_data_list.get('address', {}).get('addressCountry', '')})
    # now i want to add 15+ to the number

    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

    NUMBER += 15
    if NUMBER == 4980 or NUMBER > 4980:
        break