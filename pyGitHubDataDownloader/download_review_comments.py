import sys
sys.path.append('.')
from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.config import base_url
from pyGitHubAPI.pagenator import Pagenator
import csv
from pathlib import Path
from pyGitHubDataDownloader.repository_log import RepositoryLog

def download(id, page, pagenator) : 
    for res in pagenator : 
        if res.status_code == 200 : 
            with open( f'./repo_content/REVIEW_COMMENT/{id}/{page}.json', mode = 'w', encoding = 'utf-8' ) as wf : 
                wf.write(res.text)  
            page += 1 
        else : 
            raise Exception 

def main() : 
    error_repo_log_file_path = './logs/download_review_comment_repo_log.txt'
    error_repo_logs = RepositoryLog(error_repo_log_file_path)
    
    with open('./args/download_review_comments/list_repos.csv') as f : 
        reader = csv.DictReader(f)
        for row in reader : 
            id = row['id']
            owner = row['owner']
            repo = row['name']

            Path(f'./repo_content/REVIEW_COMMENT/{id}').mkdir(exist_ok = True)

            page = 1
            url = f'{base_url}repos/{owner}/{repo}/pulls/comments'
            params = {
                'per_page' : 100, 
                'page' : page
            }            
            pagenator = Pagenator(url, params)
            try : 
                download(id, page, pagenator)
            except : 
                error_repo_logs.put(id)
                Path(f'./error_logs/{id}').mkdir(exist_ok = True)

            print(f'{id}')

    error_repo_logs.write_to_file(error_repo_log_file_path)

if __name__ == '__main__' : 
    main()
    