import sys
sys.path.append('.')
from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.config import make_ghurl
from pyGitHubAPI.pagenator import Pagenator
from pathlib import Path
import csv

def write_to_file(repo_id, num, text) : 
    path_str = f'./repo_content/REPOSITORY_CONTRIBUTORS/{repo_id}'
    path = Path(path_str)    
    path.mkdir(exist_ok = True)
    path = path / f'{num}.json'
    path.write_text(text)

def get_repository_contributors(repo_id, owner, repo) : 
    pagenator = ghAPI.get_repository_contributors(owner, repo)
    n = 1    
    try : 
        for res in pagenator : 
            if res.status_code == 200 : 
                write_to_file(repo_id, n, res.text)
            n += 1
    except : 
        Path(f'./error_logs/download_repository_contributors/{repo_id}').mkdir(exist_ok=True)

with open('./args/download_repos/list_repos.csv', encoding = 'utf-8-sig') as f :
    reader = csv.DictReader(f)   
    for row in reader : 
        repo_id = row['id']
        owner = row['owner']
        repo = row['name']

        print(repo_id)
        get_repository_contributors(repo_id, owner, repo)