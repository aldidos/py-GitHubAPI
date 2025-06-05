import sys
sys.path.append('.')
from pyGitHubAPI.github_api import ghAPI
import csv
from pathlib import Path
import json

class RepositoryDownloaer : 

    def __init__(self, download_path) : 
        self.logs = open('./error_logs/download_repositories.txt', mode = 'w')
        self.download_path = Path(download_path)  

    def close_log_file(self) : 
        self.logs.close()

    def download_repo(self, owner, repo) : 
        res = ghAPI.get_repository(owner, repo)
        if res.status_code == 200 : 
            repository = json.loads(res.text)
            repo_id = repository['id']
            output_path = self.download_path / f'{repo_id}.json'
            output_path.write_text(res.text, encoding = 'utf-8')
            self.logs.write(f'{owner}\t{repo}\tSUCCESS\n')
        else : 
            self.logs.write(f'{owner}\t{repo}\tFAILED\n')

def download_repo(id, owner, repo) : 
    res = ghAPI.get_repository(owner, repo)
    if res.status_code == 200 : 
        
        with open(f'./repo_content/REPOSITORY/{id}.json', mode = 'w', encoding = 'utf-8') as f : 
            f.write(res.text)

def main() :     
    downloader = RepositoryDownloaer('./repo_content/REPOSITORY')

    with open('./args/download_repos/repository_list.csv') as f : 
         reader = csv.DictReader(f)
         for row in reader : 
            repo_owner = row['repo_owner']
            repo_name = row['repo_name']

            downloader.download_repo( repo_owner, repo_name )
            print(f'{repo_owner}/{repo_name}')

         downloader.close_log_file()

if __name__ == '__main__' : 
    main() 
