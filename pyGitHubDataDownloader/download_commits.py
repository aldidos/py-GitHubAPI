import sys
sys.path.append('.')
from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.pagenator import Pagenator
from pyGitHubAPI.util import delay
from pathlib import Path
import json
import multiprocessing

def download(repo_id, owner, name, path, output_base_path ) :
    url = f'{ghAPI.base_url}/repos/{owner}/{name}/commits'
    params = {
        'path' : path, 
        'per_page' : 100, 
        'page' : 1
    }

    output_path = f'{output_base_path}/{repo_id}'
    Path(output_path).mkdir(exist_ok=True)

    pagenator = Pagenator(url, params, ghAPI.headers)
    n_page = 1
    for res in pagenator :                 
        if res.status_code == 200 : 
            Path(f'{output_path}/{n_page}.json').write_text(res.text, encoding = 'utf-8')                        
        n_page += 1

def main() : 
    file_name = 'prt_repo_info.json'
    output_base_path = './repo_content/COMMITS'
    with open(f'./args/download_commits/{file_name}', encoding = 'utf-8') as f : 
        loader = json.load(f)
        dataset = [ ( data['repo_id'], data['owner'], data['name'], data['file_path'], output_base_path) for data in loader ]

        with multiprocessing.Pool() as pool : 
            pool.starmap(download, dataset)

if __name__ == '__main__' : 
    main()