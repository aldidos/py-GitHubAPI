import sys
sys.path.append('.')
from pyGitHubAPI.github_api import ghAPI
import csv

def download_repo(id, owner, repo) : 
    res = ghAPI.get_repository(owner, repo)
    if res.status_code == 200 : 
        
        with open(f'./repo_content/REPOSITORY/{id}.json', mode = 'w', encoding = 'utf-8') as f : 
            f.write(res.text)

def main() : 
    with open('./args/download_repos/list_repos.csv') as f : 
        reader = csv.DictReader(f)

        for row in reader : 
            id = row['id']
            owner = row['owner']
            repo = row['name']

            download_repo(id, owner, repo)
            print(id)

if __name__ == '__main__' : 
    main()    
