import re

from unidecode import unidecode

# Also we could test from slugify import slugify
def clean_text(text):
    replacements = {
        'Ã‘': 'Ñ',
        'Âª': 'ª',
        'Ã': 'Í',
        'Í“': 'Ó',
        'Âº': 'ª',
        'r?a': 'ría',
        'R?A': 'RÍA',
        '1?': '1ª',
        'í‰': 'e',
        'i%0': 'e',
        'Í‰': 'E'
    }
    
    for key, value in replacements.items():
        text = text.replace(key, value)

    return text

def custom_slugify(text):
    text = clean_text(text)
    # Replace accents and slashes into hiphons
    return unidecode(text).replace('/', '-')    

def get_final_segment(input_string):
    # Split the string by hyphen and get the last segment
    segments = input_string.split('-')
    return segments[-1]

