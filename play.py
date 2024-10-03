from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("ws://browserless_host:port")
    page = browser.new_page()
    page.goto("http://www.agpool.com/index.php?ctx=competicion&submenu=competicioncoruna")
    
    # Aquí puedes interactuar con el DOM, hacer clics, etc.
    page.select_option('#anno', '153')  # Selecciona una opción del select
    page.click('#cambioano')  # Simula el click del botón
    
    # Espera la nueva página y extrae los datos
    page.wait_for_load_state('networkidle')
    print(page.content())  # Devuelve el contenido actualizado
