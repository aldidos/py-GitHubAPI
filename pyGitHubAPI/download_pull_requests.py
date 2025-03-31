import sys
sys.path.append('.')
from pyGitHubAPI.executor.get_pulls_executor import GetPullsExecutor
from pyGitHubAPI.pagenator import Pagenator
from requests import Response
from pathlib import Path
import json
import csv
import time

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

            time.sleep(3) 
            waiting(res)

def batch_download(input_file_path, output_base_path) : 
    with open(input_file_path, mode = 'r', encoding = 'utf-8') as f : 
        reader = csv.DictReader(f)
        for data in reader : 
            id = data['id']
            owner = data['owner']
            repo = data['name']            
            
            output_path = Path(f'{output_base_path}/{id}')
            if output_path.exists() : 
                print(f'skip {id}')
                continue
            output_path.mkdir()

            print(f'start {id}')
            download_pull_requests(owner, repo, output_path = output_path)
            print(f'end {id}')

if __name__ == '__main__' : 
    input_file_path = sys.argv[1]
    output_base_path = sys.argv[2]
    batch_download(input_file_path, output_base_path)