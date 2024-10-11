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

