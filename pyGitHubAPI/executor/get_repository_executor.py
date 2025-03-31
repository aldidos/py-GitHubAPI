import sys
sys.path.append('.')
from pyGitHubAPI.github_api import ghAPI
import json
import csv

class GetRepositoryExecutor : 

    def execute(owner, repo) : 
        res = ghAPI.get_repository(owner, repo)
        
        if res.status_code == 200 : 
            print(f'GET {owner}/{repo} -> {res.status_code}')
            repo = json.loads(res.text)
            return repo
        
        return None
    
    def execute_batch(list_dataset) : 
        list_repos = []
        for dataset in list_dataset : 
            owner = dataset['owner']
            repo = dataset['repo']

            repo_data = GetRepositoryExecutor.execute( owner, repo )

            if repo_data : 
                list_repos.append( repo_data )

        return list_repos

if __name__ == '__main__' : 
    dataset_path = '../py-github-data-analysis/data-GHS/sample_repo_list.csv'
    with open(dataset_path, mode = 'r', encoding='utf-8') as rf : 
        reader = csv.DictReader(rf)
        repos = GetRepositoryExecutor.execute_batch( reader )

        output_file_path = './get_repository_result.json'
        with open(output_file_path, mode = 'w', encoding='utf-8') as wf : 
            json.dump(repos, wf)
