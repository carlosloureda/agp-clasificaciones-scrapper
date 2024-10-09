import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def clean_text(text):
    replacements = {
        'Ã‘': 'Ñ',
        'Âª': 'ª',
        'Ã': 'Í',
        'Í“': 'Ó',
        'Âº': 'ª',
    }
    
    for key, value in replacements.items():
        text = text.replace(key, value)
    
    return text

def get_final_segment(input_string):
    # Split the string by hyphen and get the last segment
    segments = input_string.split('-')
    return segments[-1]

def get_temps_info(url, resultados, competicion_key):
    driver.get(url)

    # Espera a que el select 'anno' esté disponible
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "anno")))
    except TimeoutException:
        print("El elemento 'anno' no se encontró a tiempo.")
        driver.quit()
        return

    select_temporada = Select(driver.find_element(By.ID, "anno"))
    annos = [{'value': clean_text(option.get_attribute('value')), 'text': clean_text(option.text)} for option in select_temporada.options]

    for anno in annos:
        try:
            select_temporada.select_by_value(anno['value'])
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cambioano"))).click()

            time.sleep(2)  # Añadir una pequeña espera tras el click

            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "indice")))

            select_liga = Select(driver.find_element(By.ID, "indice"))
            ligas = [{'value': clean_text(option.get_attribute('value')).replace('|', '-').replace(' ', '-').lower(), 'label': clean_text(option.text)} for option in select_liga.options]
            
            # Guardamos las ligas bajo la temporada dentro de la ciudad 'a-coruna'
            temporada_key = get_final_segment(anno['text'].lower().replace(' ', '-'))
            resultados[competicion_key][temporada_key] = ligas

            driver.get(url)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "anno")))
            select_temporada = Select(driver.find_element(By.ID, "anno"))
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error al procesar el año {anno['text']}: {e}")
            continue

    # Escribimos el resultado en un archivo JSON
    with open('resultados_ligas.json', 'w', encoding='utf-8') as json_file:
        json.dump(resultados, json_file, ensure_ascii=False, indent=4)


driver = webdriver.Chrome()
def get_all_temps_info():
    competiciones=['competicioncoruna','competicionlugo','competicionorense','competicionpontevedra']

    resultados = {
        "coruna": {},
        "lugo": {},
        "orense": {},
        "pontevedra": {}
    }
    for competicion in competiciones:
        url = f'http://www.agpool.com/index.php?ctx=competicion&submenu={competicion}'
        competicion_key = competicion.replace('competicion', '').lower()
        get_temps_info(url, resultados, competicion_key)
    driver.quit()


get_all_temps_info()
# TODO: Use headless browser to scrape data in the server
# TODO: Scrape data for tables and create a nice json file
# TODO: Use the jsons in the website and put together both codes