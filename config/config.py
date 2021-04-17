import json

class Config():
    appName = 'Cali'
    language = 'es'
    with open(f'languages/{language}.json') as file:
        dictionary = json.load(file)
