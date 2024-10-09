import re

def clean_text(text):
    # Primero reemplazamos caracteres específicos que parecen estar mal codificados
    replacements = {
        'Ã‘': 'Ñ',
        'Âª': 'ª',
        'Ã': 'Í',
        'ª': 'a',
        '©': 'e',
        '¢': 'c',
        # Puedes añadir más reglas si es necesario
    }
    
    # Reemplaza los caracteres malformados en el texto
    for key, value in replacements.items():
        text = text.replace(key, value)
    
    return text

text = 'Liga: 2Âª CATEGORÃA A CORUÃ‘A (valor: 1023|2Âª CATEGORÃA A CORUÃ‘A)'
decoded_text = clean_text(text)
print(decoded_text)
