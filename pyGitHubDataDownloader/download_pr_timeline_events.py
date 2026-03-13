import sys
sys.path.append('.')
from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.config import headers, base_url
from pyGitHubAPI.pagenator import Pagenator
from pathlib import Path
import csv
import multiprocessing
import json

def download(repo_id, pr_id, owner, repo, pr_number) : 
    page = 1

    url = f'{base_url}/repos/{owner}/{repo}/issues/{pr_number}/timeline'
    params = {            
        'per_page' : 100, 
        'page' : page
    }

    output_base_dir = './repo_content/ISSUE_TIMELINE_EVENTS'
    output_dir = f'{output_base_dir}/{repo_id}'
    Path(output_dir).mkdir(exist_ok = True)

    pagenator = Pagenator(url, params, headers)
    for res in pagenator :         
        if res.status_code == 200 : 
            output_file_name = f'{pr_id}_{pr_number}_{page}.json'
            Path(f'{output_dir}/{output_file_name}').write_text(res.text, encoding = 'utf-8')
            page += 1

def test() : 
    repo_id = 1111
    pr_id = 142213284
    owner = 'ethereum'
    repo = 'eth-keys'
    pr_number = 2
    page = 1

    download(repo_id, pr_id, owner, repo, pr_number)

def main() :     
    pr_list_file_path = 'e:/research_pullreq_template_checklist/data/repo_pr_list.csv'
    
    with open(pr_list_file_path, mode = 'r', encoding = 'utf-8-sig') as f :
        reader = csv.DictReader(f)

        dataset = [ ( row['repo_id'], row['pr_id'], row['owner'], row['repo'], row['pr_number'] ) for row in reader ]

        with multiprocessing.Pool() as pool : 
            pool.starmap( download, dataset )

if __name__ == '__main__' :     
    main()
    print('end')