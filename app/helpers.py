import json
import requests
from bs4 import BeautifulSoup


def get_specific_table_with_bs4(response):
    # Parseamos el HTML
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    # Intentamos encontrar la tabla externa
    outer_table = soup.find('table', {'width': '100%', 'border': '0', 'align': 'center'})
    
    if outer_table is None:
        # Si no se encuentra la tabla, devolvemos None o un resultado vacío
        return None  # o return {'tableInfo': [], 'info': []}
    
    # Intentamos encontrar la tabla anidada dentro de la tabla externa
    nested_table = outer_table.find('table', {'border': '1', 'width': '100%'})
    
    if nested_table is None:
        # Si no se encuentra la tabla anidada, devolvemos None o un resultado vacío
        return None  # o return {'tableInfo': [], 'info': []}
    
    # Continuamos con el procesamiento si ambas tablas se encontraron
    rows = nested_table.find_all('tr')
    
    info_texts = []
    headers = []
    data_entries = []
    
    for row in rows:
        cols = row.find_all('td')
        # Si la fila tiene una celda con colspan, es información adicional
        if len(cols) == 1 and cols[0].get('colspan'):
            info_text = cols[0].get_text(strip=True)
            info_texts.append(info_text)
        elif not headers and len(cols) > 1:
            # Obtenemos los encabezados, reemplazando claves vacías por 'POS'
            headers = [col.get_text(strip=True) or 'POS' for col in cols]
        else:
            values = [col.get_text(strip=True) for col in cols]
            if len(values) == len(headers):
                entry = dict(zip(headers, values))
                data_entries.append(entry)
            else:
                # Si el número de valores no coincide con el de encabezados, lo manejamos según sea necesario
                pass  # Puedes agregar lógica adicional aquí si lo deseas
    
    result = {
        'tableInfo': data_entries,
        'info': info_texts
    }
    
    return result



def get_table_page_and_data(input_json):
    url = "http://www.agpool.com/index.php?ctx=competiciones"
    # Initialize results dictionary
    results = {}

    # Iterate over each city, season, and league
    for city, seasons in input_json.items():
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
    with open('data/results_with_tables.json', 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)
