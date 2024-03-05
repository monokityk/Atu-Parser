import requests
from bs4 import BeautifulSoup
import csv
import os

# Function to extract data from the table and append it to the CSV file
def parse_table(url, output_file, table_index=0):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables on the page
    tables = soup.find_all('table')

    # Check if the specified table_index is within range
    if table_index >= len(tables):
        print("Error: Table index out of range")
        return

    # Select the specified table
    table = tables[table_index]

    # Determine if the file exists
    file_exists = os.path.exists(output_file)

    # Open the CSV file in append mode ('a')
    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # If the file doesn't exist, write the header row
        if not file_exists:
            writer.writerow(["VehicleId", "VehicleRecordId", "EnterpriseId", "ModelId", "VehicleManufacturerId", 
                             "VehicleManufacturerPlantId", "Number", "NumberPlate", "StartDate", "StartDate_Accuracy", 
                             "EndDate", "EndDate_Accuracy", "BuiltYear", "BuiltYear_Accuracy", "ModelSerialNumber", 
                             "VIN", "ChassisModelId", "ChassisNumber", "BodyModelId", "BodyNumber", "Note", 
                             "VehicleService", "VehicleState", "BindMode", "History", "HiddenComment", "ScrapDate", 
                             "ScrapDate_Accuracy"])

        # Find all rows in the table body
        for row in table.find_all('tr'):
            # Extract data from each cell
            cells = row.find_all('td')
            if cells:
                # Extracting relevant data from cells if available
                fleet_number = cells[0].text.strip()
                year = cells[2].text.strip()
                vin = cells[3].text.strip()

                # Check if license plate exists before extracting
                license_plate = cells[4].text.strip()[:7] if len(cells) > 4 else ""

                # Append "-00-00" to the built year
                built_year = year + "-00-00"

                # Extract the last 6 digits of the VIN for ModelSerialNumber
                model_serial_number = vin[-6:]

                # Writing data to CSV
                writer.writerow(["", "", "", "", "", "", fleet_number, license_plate, "", "Exact", "0000-00-00", "Exact", built_year, "Exact", model_serial_number, vin, "", "", "", "", "", "Passenger", "InService", "False", "Data on CPTDB - " + url, "", "", "", ""])

# URL of the website
url = "https://cptdb.ca/wiki/index.php/Durham_Region_Transit_8579-8589"

# Output CSV file
output_file = "output.csv"

# Table index to parse
table_index = 1  # Adjust this value as needed

# Call the function
parse_table(url, output_file, table_index)

print("Data has been scraped and saved to", output_file)
