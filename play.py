from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

from unidecode import unidecode



def clean_text(text):
    # Primero reemplazamos caracteres específicos que parecen estar mal codificados
    replacements = {
        'Ã‘': 'Ñ',
        'Âª': 'ª',
        'Ã': 'Í',
        'Í“':'Ó',
        'Âº':'ª',
        # Puedes añadir más reglas si es necesario
    }
    
    # Reemplaza los caracteres malformados en el texto
    for key, value in replacements.items():
        text = text.replace(key, value)
    
    return text

url='http://www.agpool.com/index.php?ctx=competicion&submenu=competicioncoruna'
driver = webdriver.Chrome()

driver.get(url)

# Espera a que el select 'anno' esté disponible
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "anno")))

# Encuentra todos los valores del select 'anno' (temporadas)
select_temporada = Select(driver.find_element(By.ID, "anno"))
annos = []
for option in select_temporada.options:
    annos.append({'value': clean_text(option.get_attribute('value')), 'text': clean_text(option.text)})

# Crear un diccionario para almacenar los resultados
resultados = {}

for anno in annos:
    # Selecciona cada 'anno'
    select_temporada.select_by_value(anno['value'])

    # Hacer clic en el botón "Cambio Año"
    driver.find_element(By.ID, "cambioano").click()

    # Espera a que el select 'indice' esté disponible
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "indice")))

    # Extraer los valores del select 'indice' (ligas) para el 'anno' actual
    select_liga = Select(driver.find_element(By.ID, "indice"))
    ligas = []
    for option in select_liga.options:

        # Dentro del bucle de las ligas:
        # ligas.append({'value': option.get_attribute('value'), 'text': clean_text(option.text)})
        # ligas.append({'value': option.get_attribute('value'), 'text': option.text})
        ligas.append({'value': clean_text(option.get_attribute('value')), 'text': clean_text(option.text)})

    # Almacenar los resultados de ligas por anno
    resultados[anno['text']] = ligas

    # Volver a la página principal para seleccionar un nuevo 'anno'
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "anno")))
    select_temporada = Select(driver.find_element(By.ID, "anno"))

# Mostrar los resultados
for anno, ligas in resultados.items():
    print(f"Temporada: {anno}")
    for liga in ligas:
        print(f"  Liga: {liga['text']} (valor: {liga['value']})")

driver.quit()
