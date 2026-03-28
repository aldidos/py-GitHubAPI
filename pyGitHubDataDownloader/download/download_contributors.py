import sys
sys.path.append('.')
from pyGitHubAPI.github_api import base_url
from pyGitHubAPI.pagenator import Pagenator
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader
from pathlib import Path
from pyGitHubDataDownloader.executor.parallel_executor import ParallelExecutor
from requests import Session

def task_get_contributors(session : Session, headers, repo_id, owner, name, output_dir) : 
    url = f'{base_url}/repos/{owner}/{name}/contributors' 
    params = {
        'per_page' : 100, 
        'page' : 1,
        'anon' : True
    }
    print(url)

    output_path = f'{output_dir}/{repo_id}'
    Path(output_path).mkdir(exist_ok = True)

    n_page = 1
    def success_func(res) : 
        nonlocal n_page
        Path(f'{output_path}/{n_page}.json').write_text(res.text, encoding = 'utf-8')
        n_page += 1 

    pagenator = Pagenator(session, url, params, headers = headers)
    res = pagenator.paging( success_func )

    return res, None    

def download_contributors(file_paths, output_dir, gh_tokens) : 
    n_tokens = len(gh_tokens)
    args = []

    order = 0 
    for file_path in file_paths : 
        repo_data = DataFileReader.from_json(file_path)
        repo_id = repo_data['id']
        name = repo_data['name']
        owner = repo_data['owner']['login']        

        args.append( (task_get_contributors, gh_tokens[order % n_tokens], (repo_id, name, owner, output_dir) ) ) 
        order += 1

    executor = ParallelExecutor(50)
    executor.run( args )

if __name__ == '__main__' :     
    in_args = DataFileReader.from_json(sys.argv[1])
    input_file_path = in_args['input_file_path']
    output_dir = in_args['output_dir']
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 

    file_paths = DataFileReader.find_files(input_file_path, 'json')
    download_contributors(file_paths, output_dir, gh_tokens)