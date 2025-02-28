import json

def write_text_to_json(path : str, text : str) : 
    with open(path, mode='w', encoding='utf-8') as f : 
        json.dump( json.loads(text), f )