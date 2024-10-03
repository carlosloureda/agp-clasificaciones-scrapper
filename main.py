import requests
from bs4 import BeautifulSoup

# URL of the page we want to scrape
url = "http://www.agpool.com/index.php?ctx=competicion&submenu=competicioncoruna"

def scrape_temporadas(url):
    #  Send a GET request to fetch the HTML content
    response = requests.get(url)

    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the select element with name 'anno'
    select_element = soup.find("select", {"name": "anno"})

    # Extract all options from the select element
    options = select_element.find_all("option")

    # Create a dictionary to store temporada ID and their names
    temporadas = {}

    for option in options:
        temporada_id = option.get("value")
        temporada_name = option.text.strip()
        temporadas[temporada_id] = temporada_name

    # Print the extracted temporada options
    print("Available Temporadas:")
    for temporada_id, temporada_name in temporadas.items():
        print(f"ID: {temporada_id}, Name: {temporada_name}")    


scrape_temporadas(url)       