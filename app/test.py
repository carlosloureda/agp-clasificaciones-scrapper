foo = '1021-2a-categoria-salni%0s'


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
    }
    
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


foocleaned = clean_text(foo)

print(foocleaned)