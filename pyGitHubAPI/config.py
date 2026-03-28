from dotenv import dotenv_values

base_url = f'https://api.github.com/'

def make_ghurl(uri) : 
    return f'{base_url}{uri}'

def make_headers(token) : 
    return {
        'Accept' : 'application/vnd.github+json', 
        'Authorization' : f'Bearer {token}'    
    }