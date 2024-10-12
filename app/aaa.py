from bs4 import BeautifulSoup

html = '''<div align="center">                
                

<div><table width="100%" border="0" align="center"><tbody><tr><td align="center"><table border="1" width="100%"><tbody><tr><td colspan="100" bgcolor="#0B663A" align="center"><div style="font-size:18pt;color:#FFFFFF;">RANKING 2ª CATEGORÍA AS PONTES - 1º BLOQUE<div></div></div></td></tr><tr><td colspan="100" bgcolor="FFFFFF" align="center"><div style="font-size:9pt;color:##187615;"><div></div></div></td></tr><tr><td colspan="100" bgcolor="FFFFFF" align="center"><div style="font-size:9pt;color:##187615;"><div></div></div></td></tr><tr><td colspan="100" bgcolor="FFFFFF" align="center"><div style="font-size:9pt;color:##187615;"><div></div></div></td></tr><tr><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">&nbsp;</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">AGP</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">NOMBRE</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">P1</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">P2</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">P3</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">PF</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">PC</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">DP</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">PT</div></td></tr><tr><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">1</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:9pt;color:#000000;">18026</div></td><td bgcolor="FFFFFF"><div style="font-size:9pt;color:#000000;">DAVID RODRIGUEZ OTERO</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:8pt;color:#000000;">14</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:8pt;color:#000000;">&nbsp;</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:8pt;color:#000000;">&nbsp;</div></td><td bgcolor="#CCF9CA" align="center"><div style="font-size:8pt;color:#000000;">25</div></td><td bgcolor="#CCF9CA" align="center"><div style="font-size:8pt;color:#000000;">11</div></td><td bgcolor="#CCF9CA" align="center"><div style="font-weight:bold;font-size:8pt;color:#000000;">14</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">14</div></td></tr><tr><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">2</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:9pt;color:#000000;">14824</div></td><td bgcolor="FFFFFF"><div style="font-size:9pt;color:#000000;">LINO LUACES PIÑEIRO</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:8pt;color:#000000;">7</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:8pt;color:#000000;">&nbsp;</div></td><td bgcolor="FFFFFF" align="center"><div style="font-size:8pt;color:#000000;">&nbsp;</div></td><td bgcolor="#CCF9CA" align="center"><div style="font-size:8pt;color:#000000;">12</div></td><td bgcolor="#CCF9CA" align="center"><div style="font-size:8pt;color:#000000;">14</div></td><td bgcolor="#CCF9CA" align="center"><div style="font-weight:bold;font-size:8pt;color:#000000;">-2</div></td><td bgcolor="#0B663A" align="center"><div style="font-weight:bold;font-size:8pt;color:#FFFFFF;">7</div></td></tr></tbody></table></td></tr></tbody></table></div>             
            </div>'''

def get_specific_table_with_bs4(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
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


print(get_specific_table_with_bs4(html))