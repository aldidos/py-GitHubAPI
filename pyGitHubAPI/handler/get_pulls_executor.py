import sys
sys.path.append('.')
from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.pagenator import Pagenator
from requests import Response
from pathlib import Path
import json
import csv
import time

class GetPullsExecutor : 

    def __init__(self, owner, repo, state = 'all', sort = 'created', per_page = 100) : 
        self.owner = owner
        self.repo = repo
        self.state = state
        self.sort = sort
        self.per_page = per_page

    def execute(self) : 
        res = ghAPI.get_list_pull_requests(self.owner, self.repo, self.state, self.sort, self.per_page)
        if res.status_code == 200 : 
            return res
        print(res.status_code)
        print(res.text)
        return None

def waiting(res : Response) : 
    ratelimit_remaining = res.headers.get('x-ratelimit-remaining')
    ratelimit_remaining = int(ratelimit_remaining)
    if ratelimit_remaining < 5 : ####
        time.sleep(30 * 60)

def download_pull_requests(owner, repo, state = 'closed', *, output_path) : 
    get_pull_executor = GetPullsExecutor(owner, repo, state)
    res = get_pull_executor.execute()
    waiting(res)

    if res : 
        result = json.loads( res.text )
        num = 1
        output_file_path = f'{output_path}/{num}.json'
        with open(output_file_path, mode = 'w', encoding = 'utf-8') as wf : 
            json.dump(result, wf)
        
        num += 1
        pagenator = Pagenator(res)
        for next_res in pagenator : 
            result = json.loads( next_res.text )

            output_file_path = f'{output_path}/{num}.json'
            with open(output_file_path, mode = 'w', encoding = 'utf-8') as wf : 
                json.dump(result, wf)
            num += 1
            waiting(res)

def batch_download(input_file_path, output_base_path) : 
    with open(input_file_path, mode = 'r', encoding = 'utf-8') as f : 
        reader = csv.DictReader(f)
        for data in reader : 
            id = data['id']
            owner = data['owner']
            repo = data['name']
            
            output_path = Path(f'{output_base_path}/{id}')
            output_path.mkdir()

            download_pull_requests(owner, repo, output_path = output_path)
            print(id)

if __name__ == '__main__' : 
    input_file_path = './gh_repo_list_with_PQT.csv'
    output_base_path = './repo_content/PULL_REQUEST'
    batch_download(input_file_path, output_base_path)