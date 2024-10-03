from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json

url='http://www.agpool.com/index.php?ctx=competicion&submenu=competicioncoruna'
driver = webdriver.Chrome()

driver.get(url)


time.sleep(3)

# Encontrar el select y seleccionar la opción
select_temporada = Select(driver.find_element(By.ID, "anno"))
select_temporada.select_by_value('150')  # Selecciona la opción de A CORUÑA 24/25

# Hacer clic en el botón "Cambio Año"
driver.find_element(By.ID, "cambioano").click()

# Esperar unos segundos para la carga de la nueva página
time.sleep(3)


# Clicka en las temporadas

select_liga = Select(driver.find_element(By.ID, "indice"))
# select_liga.select_by_value('941|3Âª CATEGORÃA CORUÃ‘A') 
select_liga.select_by_index(4)
driver.find_element(By.ID, "clasificacion1").click()


time.sleep(3)

# 948|2Âª CATEGORÃA CORUÃ‘A

def get_table():

    # # Extraer la tabla de resultados
    # table = driver.find_element(By.XPATH, '//table[@border="1"]')

    # # Iterar sobre las filas de la tabla y extraer los datos
    # rows = table.find_elements(By.TAG_NAME, "tr")

    # for row in rows[1:]:  # Saltar el encabezado de la tabla
    #     cells = row.find_elements(By.TAG_NAME, "td")
    #     data = [cell.text for cell in cells]  # Extraer el texto de cada celda
    #     print(data)
    # Extraer la tabla de resultados
   # Extraer la tabla de resultados
    table = driver.find_element(By.XPATH, '//table[@border="1"]')

    # Extraer los encabezados de la tabla
    headers = [header.text for header in table.find_elements(By.XPATH, ".//tr[1]/td")]

    # Crear una lista para almacenar los datos
    table_data = []

    # Iterar sobre las filas de la tabla y extraer los datos
    rows = table.find_elements(By.XPATH, ".//tr[position()>1]")

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        # Asegurarse de que el número de celdas coincida con el número de encabezados
        row_data = {}
        for i in range(min(len(headers), len(cells))):
            row_data[headers[i]] = cells[i].text
        table_data.append(row_data)

    # Convertir los datos en formato JSON
    json_data = json.dumps(table_data, ensure_ascii=False, indent=4)

    # Imprimir el JSON o guardarlo en un archivo
    print(json_data)


get_table()
# Cerrar el navegador
driver.quit()        