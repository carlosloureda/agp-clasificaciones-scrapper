from bs4 import BeautifulSoup

html = '''<div align="center">                
                

<div><table width="100%" border="0" align="center"><tbody><tr><td align="center"><table border="1" width="100%"><tbody><tr><td colspan="100" bgcolor="#0B663A" align="center"><div style="font-size:18pt;color:#FFFFFF;">RANKING 2ª CATEGORÍA AS PONTES - 1º BLOQUE<div></div></div></td></tr><tr><td colspan="100" bgcolor="FFFFFF" align="center"><div style="font-size:9pt;color:##187615;"><div></div></div></td></tr><tr><td colspan="100" bgcolor="FFFFFF" align="center"><div style="font-size:9pt;color:##187615;"><div></div></div></td></tr><tr><td colspan="100" bgcolor="FFFFFF" align="center"><div style="font-size:9pt;color:##187615;"><div></div></div></td></tr><tr><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">&nbsp;</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">AGP</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">NOMBRE</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">P1</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">P2</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">P3</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">PF</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">PC</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">DP</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">PT</div></td></tr><tr><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">1</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:9pt;color:#000000;">18026</div></td><td bgcolor="FFFFFF"><div style="font-size:9pt;color:#000000;">DAVID RODRIGUEZ OTERO</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:8pt;color:#000000;">14</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:8pt;color:#000000;">&nbsp;</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:8pt;color:#000000;">&nbsp;</div></td><td bgcolor="#CCF9CA" align="center"><div style="font-size:8pt;color:#000000;">25</div></td><td bgcolor="#CCF9CA" align="center"><div style="font-size:8pt;color:#000000;">11</div></td><td bgcolor="#CCF9CA" align="center"><div style="font-weight:bold;font-size:8pt;color:#000000;">14</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">14</div></td></tr><tr><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">2</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:9pt;color:#000000;">14824</div></td><td bgcolor="FFFFFF"><div style="font-size:9pt;color:#000000;">LINO LUACES PIÑEIRO</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:8pt;color:#000000;">7</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:8pt;color:#000000;">&nbsp;</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:8pt;color:#000000;">&nbsp;</div></td><td bgcolor="#CCF9CA" align="center"><div style="font-size:8pt;color:#000000;">12</div></td><td bgcolor="#CCF9CA" align="center"><div style="font-size:8pt;color:#000000;">14</div></td><td bgcolor="#CCF9CA" align="center"><div style="font-weight:bold;font-size:8pt;color:#000000;">-2</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">7</div></td></tr></tbody></table></td></tr></tbody></table></div>             
            </div>'''

from bs4 import BeautifulSoup

# Parseamos el HTML
soup = BeautifulSoup(html, 'html.parser')

# Encontramos la tabla específica
outer_table = soup.find('table', {'width': '100%', 'border': '0', 'align': 'center'})

# Encontramos la tabla anidada que contiene los datos
nested_table = outer_table.find('table', {'border': '1', 'width': '100%'})

# Obtenemos todas las filas de la tabla anidada
rows = nested_table.find_all('tr')

info_texts = []
headers = []
data_entries = []

for row in rows:
    cols = row.find_all('td')
    # Si la fila tiene una celda con colspan="100", es información adicional
    if len(cols) == 1 and cols[0].get('colspan') == '100':
        info_text = cols[0].get_text(strip=True)
        info_texts.append(info_text)
    # Si aún no hemos obtenido los encabezados y la fila tiene múltiples celdas, asumimos que es la fila de encabezados
    elif not headers and len(cols) > 1:
        # headers = [col.get_text(strip=True) for col in cols]
        headers = [col.get_text(strip=True) or 'POS' for col in cols]
    # De lo contrario, es una fila de datos
    elif headers:
        values = [col.get_text(strip=True) for col in cols]
        # Creamos un diccionario para la fila de datos
        entry = dict(zip(headers, values))
        data_entries.append(entry)

# Creamos el resultado final
result = {
    'tableInfo': data_entries,
    'info': info_texts
}

# Imprimimos el resultado
print(result)
