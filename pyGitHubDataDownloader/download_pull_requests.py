import sys
sys.path.append('.')
from pyGitHubAPI.config import base_url
from pyGitHubAPI.pagenator import Pagenator
from requests import Response
from pathlib import Path
import csv
import time

def waiting(res : Response) : 
    ratelimit_remaining = res.headers.get('x-ratelimit-remaining')
    ratelimit_remaining = int(ratelimit_remaining)
    if ratelimit_remaining < 5 : ####
        time.sleep(30 * 60)

def download_pull_requests(owner, repo, state = 'closed', *, output_path) : 
    url = uri = f'{base_url}/repos/{owner}/{repo}/pulls'
    page = 1
    params = {
        'state' : state, 
        'per_page' : 100, 
        'page' : page
    }
    pagenator = Pagenator(url, params)

    for res in pagenator : 
        if res.status_code == 200 : 
            output_file_path = f'{output_path}/{page}.json'
            with open(output_file_path, mode = 'w', encoding = 'utf-8') as wf : 
                wf.write(res.text)
            page += 1
        else : 
            break

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