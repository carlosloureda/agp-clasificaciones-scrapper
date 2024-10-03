from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json

url='http://www.agpool.com/index.php?ctx=competicion&submenu=competicioncoruna'
driver = webdriver.Chrome()

driver.get(url)


time.sleep(0.5)

# Encontrar el select y seleccionar la opción
select_temporada = Select(driver.find_element(By.ID, "anno"))
select_temporada.select_by_value('150')  # Selecciona la opción de A CORUÑA 24/25

# Hacer clic en el botón "Cambio Año"
driver.find_element(By.ID, "cambioano").click()

# Esperar unos segundos para la carga de la nueva página
time.sleep(0.5)


# Clicka en las temporadas

select_liga = Select(driver.find_element(By.ID, "indice"))
# select_liga.select_by_value('941|3Âª CATEGORÃA CORUÃ‘A') 
select_liga.select_by_index(4)
driver.find_element(By.ID, "clasificacion1").click()


time.sleep(0.5)

# 948|2Âª CATEGORÃA CORUÃ‘A

def get_table():
    # Extraer la tabla de resultados
    table = driver.find_element(By.XPATH, '//table[@border="1"]')
    table_info = ''
    # Iterar sobre las filas de la tabla y extraer los datos
    rows = table.find_elements(By.TAG_NAME, "tr")
    array_data = []
    for row in rows[1:]:  # Saltar el encabezado de la tabla
        cells = row.find_elements(By.TAG_NAME, "td")
        data = [cell.text for cell in cells]  # Extraer el texto de cada celda
        if (len(data) > 1):
            array_data.append(data)
        else:
            table_info += data[0] + ', '  # create json data
    headers = array_data[0]
    json_data = [dict(zip(headers, row)) for row in array_data[1:]]
    json_output = json.dumps(json_data, ensure_ascii=False, indent=4)
    print(json_output)
    print(table_info)


get_table()
# Cerrar el navegador
driver.quit()        