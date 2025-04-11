import sys
sys.path.append('.')
from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.pagenator import Pagenator
from requests import Response
import json
import csv
from pathlib import Path

class GetRepositoryIssuesExecutor : 

    def __init__(self, owner, repo, state = 'all', sort = 'created', per_page = 100) : 
        self.owner = owner
        self.repo = repo
        self.state = state
        self.sort = sort
        self.per_page = per_page

    def execute(self) -> Response : 
        res = ghAPI.get_list_repository_issues(self.owner, self.repo, self.state, self.sort, self.per_page)
        if res.status_code == 200 : 
            return res
        print(res.status_code)
        print(res.text)
        return None            

def download_issue(owner, repo, state = 'closed', *, output_path) : 
    executor = GetRepositoryIssuesExecutor(owner, repo, state)
    res = executor.execute()
    if res :
        num = 1
        output_file_path = f'{output_path}/{num}.json'
        with open(output_file_path, mode = 'w', encoding = 'utf-8') as f : 
            result = json.loads( res.text )  
            json.dump( result, f ) 

        pagenator = Pagenator(res)
        for res in pagenator : 
            result = json.loads( res.text )
            num += 1
            output_file_path = f'{output_path}/{num}.json'
            with open(output_file_path, mode = 'w', encoding = 'utf-8') as f : 
                result = json.loads( res.text )  
                json.dump( result, f )

def batch_execute(file_path, output_base_path) : 
    with open(file_path, mode = 'r', encoding = 'utf-8') as f : 
        reader = csv.DictReader(f)
        for data in reader : 
            id = data['id']
            owner = data['owner']
            repo = data['name']

            output_path = Path( f'{output_base_path}/{id}')
            output_path.mkdir()

            download_issue(owner, repo, output_path = output_path)

if __name__ == '__main__' : 
    input_file_path = './gh_repo_list_with_PQT.csv'
    output_base_path = './repo_content/ISSUE'
    batch_execute(input_file_path, output_base_path)