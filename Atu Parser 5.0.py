import requests
from bs4 import BeautifulSoup
import csv
import os
from vin_decoder import ( # type: ignore
    get_manufacturer_id,
    get_model_and_plant_ids,
    get_enterprise_id,
    get_manufacturer_plant_id
)

# Функция для парсинга таблиц и записи данных в CSV
def parse_tables(urls, output_file, table_index=0):
    file_exists = os.path.exists(output_file)
    vehicle_id = 80000
    record_id = 50000

    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Записываем заголовки в файл, если он создаётся впервые
        if not file_exists:
            writer.writerow([
                "VehicleId", "VehicleRecordId", "EnterpriseId", "ModelId", 
                "VehicleManufacturerId", "VehicleManufacturerPlantId", "Number",
                "NumberPlate", "StartDate", "StartDate_Accuracy", "EndDate",
                "EndDate_Accuracy", "BuiltYear", "BuiltYear_Accuracy", "ModelSerialNumber",
                "VIN", "ChassisModelId", "ChassisNumber", "BodyModelId", "BodyNumber", 
                "Note", "VehicleService", "VehicleState", "BindMode", "History", 
                "HiddenComment", "ScrapDate", "ScrapDate_Accuracy"
            ])

        # Парсинг каждой таблицы из списка URL
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')

            # Проверяем индекс таблицы
            if table_index >= len(tables):
                print(f"Error: Table index out of range for URL: {url}")
                continue

            table = tables[table_index]

            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) < 7:  # Пропуск строк с недостаточным количеством данных
                    continue

                # Извлекаем данные из ячеек таблицы
                fleet_number = cells[0].text.strip()
                year = cells[2].text.strip()
                vin = cells[3].text.strip()
                license_plate = cells[4].text.strip()[:7] if len(cells) > 4 else ""
                garage = cells[5].text.strip()
                status = cells[6].text.strip()  # Предполагается, что это 7-я колонка

                # Определяем дополнительные данные с помощью функций из библиотеки
                manufacturer_id = get_manufacturer_id(vin)
                model_id, plant_id = get_model_and_plant_ids(vin, manufacturer_id)
                enterprise_id = get_enterprise_id(garage)
                manufacturer_plant_id = get_manufacturer_plant_id(vin)

                # Преобразуем год в нужный формат
                months = {
                    "January": "01", "February": "02", "March": "03", "April": "04",
                    "May": "05", "June": "06", "July": "07", "August": "08",
                    "September": "09", "October": "10", "November": "11", "December": "12"
                }
                if '/' in year and len(year) == 7:  # Формат MM/YYYY
                    month, year_part = year.split('/')
                    built_year = f"{year_part}-{month}-00"
                elif any(month in year for month in months):
                    for month, num in months.items():
                        if month in year:
                            year = year.replace(month, num)
                    built_year = f"{year.split()[1]}-{year.split()[0]}-00"
                else:
                    built_year = f"{year}-00-00"

                # Определяем состояние автомобиля
                vehicle_state = "OutOfService" if "Retired" in status else "InService"

                # Записываем строку в CSV
                writer.writerow([
                    vehicle_id, record_id, enterprise_id, model_id, manufacturer_id, 
                    manufacturer_plant_id, fleet_number, license_plate, "", "Exact", 
                    "0000-00-00", "Exact", built_year, "Exact", vin[-6:], vin, "", "", 
                    "", "", "", "Passenger", vehicle_state, "False", 
                    f"Data on CPTDB - {url}", "", "", "", ""
                ])

                # Увеличиваем VehicleId и RecordId
                vehicle_id += 1
                record_id += 1

# Список URL для парсинга
urls = [
    "https://cptdb.ca/wiki/index.php/Edmonton_Transit_System_4523-4753",
]

# Путь к выходному файлу
output_file = r'C:\Users\danya\Documents\atu_db_client\Edmonton-Fix.csv'

# Индекс таблицы для обработки
table_index = 1  # Настройте значение по необходимости

# Запуск функции
parse_tables(urls, output_file, table_index)

print("Data has been scraped and saved to", output_file)
