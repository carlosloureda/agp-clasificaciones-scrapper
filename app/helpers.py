from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
from bs4 import BeautifulSoup

# def get_table(driver):
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table[@border="1"]')))
#     # Extraer la tabla de resultados
#     table = driver.find_element(By.XPATH, '//table[@border="1"]')
#     table_info = ''
#     # Iterar sobre las filas de la tabla y extraer los datos
#     rows = table.find_elements(By.TAG_NAME, "tr")
#     array_data = []
#     for row in rows[1:]:  # Saltar el encabezado de la tabla
#         cells = row.find_elements(By.TAG_NAME, "td")
#         data = [cell.text for cell in cells]  # Extraer el texto de cada celda
#         if (len(data) > 1):
#             array_data.append(data)
#         else:
#             table_info += data[0] + ', '  # create json data
#     headers = array_data[0]
#     json_data = [dict(zip(headers, row)) for row in array_data[1:]]
#     json_output = json.dumps(json_data, ensure_ascii=False, indent=4)
#     print(json_output)
#     print(table_info)
#     return json_data


def get_table_with_bs4(response):
    html = response.text
    print('html', html)
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the specific table
    table = soup.find('table', {'border': '1'})
    
    if table:
        headers = [header.text.strip() for header in table.find_all('th')]
        rows = table.find_all('tr')[1:]  # Skip the header

        array_data = []
        table_info = ''

        for row in rows:
            cells = row.find_all('td')
            data = [cell.text.strip() for cell in cells]
            if len(data) > 1:
                array_data.append(data)
            else:
                table_info += data[0] + ', '

        json_data = [dict(zip(headers, row)) for row in array_data]
        json_output = json.dumps(json_data, ensure_ascii=False, indent=4)

        print(json_output)
        print(table_info)
        return json_data
    else:
        print("No table found")
        return None



def get_specific_table_with_bs4(response):
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    # Locate the specific table by searching for a <div> with text "NOMBRE"
    target_table = None
    for table in soup.find_all('table'):
        if table.find('div', string="NOMBRE"):
            target_table = table
            break

    if target_table:
        headers = [header.text.strip() for header in target_table.find_all('th')]

        array_data = []
        table_info = ''
        rows = target_table.find_all('tr')[1:]  # Skip header row if needed

        for row in rows:
            cells = row.find_all('td')
            data = [cell.text.strip() for cell in cells]
            if len(data) > 1:
                array_data.append(data)
            else:
                table_info += data[0] + ', '

        json_data = [dict(zip(headers, row)) for row in array_data if len(row) == len(headers)]
        json_output = json.dumps(json_data, ensure_ascii=False, indent=4)

        print(json_output)
        print("Additional Info:", table_info)
        return json_data
    else:
        print("No table found with the specified condition")
        return None


def get_table_page_and_data(input_json):
    # print("Processing data...", input_json)
    url = "http://www.agpool.com/index.php?ctx=competiciones"
    # Initialize results dictionary
    results = {}

    # Iterate over each city, season, and league
    for city, seasons in input_json.items():
        # print("1...", city, seasons)
        results[city] = {}  # Initialize city in results

        for season, leagues in seasons.items():
            if season not in results[city]:
                results[city][season] = []  # Initialize season in results

            for league in leagues:
                # Prepare the POST data
                post_data = {
                    'menuweb': 'rankin',
                    'princompeticion': '1',
                    'tipo': 'rankin',
                    'submenu': f'competicion{city}',
                    'indicenew': league['value']
                }

                # Make the POST request
                response = requests.post(url, data=post_data)

                # Optional: Check response status
                if response.status_code == 200:
                    # Extract table data
                    table_data = get_specific_table_with_bs4(response)  # Replace with your logic
                    # table_data = 'sdfsd' # Replace with your logic
                    league_entry = {
                        'label': league['label'],
                        'table': table_data
                    }

                    results[city][season].append(league_entry)
                else:
                    print(f"Failed to retrieve data for {league['label']}")

    # Save results to a JSON file
    with open('results_with_tables.json', 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    print("Process complete! Results have been written to results_with_tables.json.")