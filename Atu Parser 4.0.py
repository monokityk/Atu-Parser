import requests
from bs4 import BeautifulSoup
import csv
import os

def get_manufacturer_id(vin):
    manufacturer_map = {
        "2FY": "154",
        "2NV": "165",
        "1VH": "244",
        "2B1": "243",
        "2BA": "243",
        "4RK": "242",
        "2G9": "233",
        "SFE": "238"
    }
    return manufacturer_map.get(vin[:3], "")

# Function to determine ModelId and VehicleManufacturerPlantId based on VIN digits
def get_model_and_plant_ids(vin):
    if len(vin) < 6:
        return "", ""  # Return empty values if VIN is too short

    vin_map = {
        "D8F": ("4659", "236"),   # XD40
        "D5F": ("5465", ""),      # D40LFR
        "D5Y": ("5483", ""),      # D60LFR
        "H5Y": ("12041", ""),     # DE60LFR
        "D8Y": ("5064", "236"),   # XD60
        "C8F": ("5065", "236"),   # XN40
        "H8F": ("5106", "236"),   # XDE40
        "H8Y": ("5106", "236"),   # XDE60
        "TBU": ("7359", "549")    # Enviro 500
    }

    return vin_map.get(vin[3:6], ("", ""))

# Function to determine EnterpriseId based on Garage
def get_enterprise_id(garage):
    garage_map = {
        "Arrow Rd": "7172",
        "Arrow Rd.": "7172",
        "McNicoll": "7180",
        "Mount Dennis": "7123",
        "Wilson": "7184",
        "Queensway": "7181",
        "Malvern": "7122",
        "Eglinton": "7175",
        "Birchmount": "7173",
        "Lakeshore": "7177",
        "Westwood": "9406"
    }
    return garage_map.get(garage, "")

def get_manufacturer_plant_id(vin):
    if vin.startswith("2FY"):
        if vin[10] in ["A", "D", "E", "P"]:
            return "154"
        elif vin[10] in ["B", "C", "F", "U"]:
            return "236"
    return ""

# Parsing tables and writing data to CSV
def parse_tables(urls, output_file, table_index=0):
    file_exists = os.path.exists(output_file)
    vehicle_id = 80000
    record_id = 50000

    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow(["VehicleId", "VehicleRecordId", "EnterpriseId", "ModelId", "VehicleManufacturerId",
                             "VehicleManufacturerPlantId", "Number", "NumberPlate", "StartDate", "StartDate_Accuracy",
                             "EndDate", "EndDate_Accuracy", "BuiltYear", "BuiltYear_Accuracy", "ModelSerialNumber",
                             "VIN", "ChassisModelId", "ChassisNumber", "BodyModelId", "BodyNumber", "Note",
                             "VehicleService", "VehicleState", "BindMode", "History", "HiddenComment", "ScrapDate",
                             "ScrapDate_Accuracy"])

        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            if table_index >= len(tables):
                print("Error: Table index out of range for URL:", url)
                continue
            table = tables[table_index]
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if cells:
                    fleet_number = cells[0].text.strip()
                    year = cells[2].text.strip()
                    vin = cells[3].text.strip()
                    license_plate = cells[4].text.strip()[:8] if len(cells) > 4 else ""
                    garage = cells[5].text.strip()
                    status = cells[6].text.strip()  # Assuming this is the 7th column (index 6)

                    # Transforming "April 2008" to "2008-04-00"
                    months = {
                        "January": "01", "February": "02", "March": "03", "April": "04",
                        "May": "05", "June": "06", "July": "07", "August": "08",
                        "September": "09", "October": "10", "November": "11", "December": "12"
                    }
                    if any(month in year for month in months):
                        for month, num in months.items():
                            if month in year:
                                year = year.replace(month, num)
                        built_year = f"{year.split()[1]}-{year.split()[0]}-00"
                    else:
                        built_year = year + "-00-00"

                    model_serial_number = vin[-6:]
                    manufacturer_id = get_manufacturer_id(vin[:3])
                    model_id, plant_id = get_model_and_plant_ids(vin)
                    enterprise_id = get_enterprise_id(garage)

                    # Set VehicleState based on status
                    vehicle_state = "OutOfService" if "Retired" in status else "InService"

                    # Write regular row
                    writer.writerow([vehicle_id, record_id, enterprise_id, model_id, manufacturer_id, plant_id,
                                     fleet_number, license_plate, "", "Exact", "0000-00-00", "Exact", built_year,
                                     "Exact", model_serial_number, vin, "", "", "", "", "", "Passenger", vehicle_state,
                                     "False", "Data on CPTDB - " + url, "", "", "", ""])

                    # Increment VehicleId and VehicleRecordId for next vehicle
                    vehicle_id += 1
                    record_id += 1

# List of URLs
urls = [
    "https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_1200-1423",
    "https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_1500-1689",
    "https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_7900-7979",
    "https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_8000-8099",
    "https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_8100-8219",
    "https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_8300-8334",
    "https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_8335-8396"
]

# Output CSV file
output_file = r'C:\Users\danya\Documents\atu_db_client\TTC Orions New.csv'

# Table index to parse
table_index = 1  # Adjust this value as needed

# Call the function
parse_tables(urls, output_file, table_index)

print("Data has been scraped and saved to", output_file)
