import requests
from bs4 import BeautifulSoup
import re

# OneDrive/Документы/Atu-Parser 2.0.py

import configparser
import requests  # Make sure to import the 'requests' library

def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    url = config.get("Settings", "url", fallback="")
    print(f"Read URL from config: {url}")
    return url

def parse_webpage(url, table_index):
    print(f"Attempting to fetch data from URL: {url}")
    response = requests.get(url)
    # Continue with the rest of your code

def main():
    url = read_config()

    if not url:
        print("URL not provided in the configuration file.")
        return

    print(f"Running script with URL: {url}")

    table_index = 0

    try:
        parsed_data = parse_webpage(url, table_index)
        # Continue with the rest of your script logic

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


def parse_webpage(url, table_index):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing the data based on the specified index
        tables = soup.find_all('table', {'class': 'sortable'})
        
        # Check if the specified table index is valid
        if 0 <= table_index < len(tables):
            table = tables[table_index]
            
            # Initialize an empty list to store the results
            results = []
            
            # Iterate through rows in the table (skip the header row)
            for row in table.find_all('tr')[1:]:
                # Extract data from columns
                columns = row.find_all('td')
                
                # Check if there are enough columns in the row
                if len(columns) >= 5:
                    fleet_number = columns[0].get_text(strip=True)
                    
                    # Extract the text from the second column and remove values in brackets
                    license_plate_full = columns[4].get_text(strip=True)
                    license_plate = re.sub(r'\([^)]*\)', '', license_plate_full)
                    
                    # Take only the first seven characters from the license plate
                    license_plate = ' '.join(license_plate.split()[:2])
                    
                    # Extract the full VIN from the third column
                    vin_full = columns[3].get_text(strip=True)
                    
                    # Extract the last 6 digits of the VIN and remove leading zeros
                    last_six_digits = str(int(vin_full[-6:]))
                    
                    # Combine the data in the desired format
                    result = f'{fleet_number};{license_plate.strip()};{last_six_digits};{vin_full.strip()}'
                    
                    # Append the result to the list
                    results.append(result)
                else:
                    print(f"Error: Row with insufficient columns found. Exiting script.")
                    return None
            
            return results
        else:
            print(f"Error: Invalid table index. No table found at index {table_index}.")
    else:
        # If the request was not successful, print an error message
        print(f"Error: Unable to fetch the webpage. Status code: {response.status_code}")

# URL of the webpage containing the tables
url = "https://cptdb.ca/wiki/index.php/York_Region_Transit_1080-1094"

# Specify the index of the table you want to parse (0 for the first table, 1 for the second table, and so on)
table_index = 0

# Call the function and print the results
parsed_data = parse_webpage(url, table_index)
if parsed_data:
    for data in parsed_data:
        print(data)
