import json

def read_token() : 
    with open('./config/token.json', mode = 'r', encoding='utf-8') as f : 
        config = json.load(f)
        return config['token']

token = read_token()

headers = {
    'Accept' : 'application/vnd.github+json', 
    'Authorization' : f'Bearer {token}'
    
}

base_url = f'https://api.github.com/'