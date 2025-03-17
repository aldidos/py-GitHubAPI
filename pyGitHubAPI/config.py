from dotenv import dotenv_values

config = dotenv_values('.env')
token = config['GITHUB_TOKEN']

headers = {
    'Accept' : 'application/vnd.github+json', 
    'Authorization' : f'Bearer {token}'
    
}

base_url = f'https://api.github.com/'