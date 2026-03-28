import sys
sys.path.append('.')
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader
from pyGitHubDataDownloader.executor.parallel_executor import ParallelExecutor
from pyGitHubAPI.github_api import base_url
from pyGitHubAPI.pagenator import Pagenator
from pathlib import Path
from requests import Session

def task_get_commits(session : Session, headers, repo_id, order, num, url, output_dir_path ) :            
    session.headers.update(headers)    

    output_path = f'{output_dir_path}/{repo_id}'
    Path(output_path).mkdir(exist_ok=True)

    res = session.get(url)
    if res.status_code == 200 :   
        Path(f'{output_path}/{order}_{num}.json').write_text(res.text, encoding = 'utf-8') 

    return res, None

def download(args, output_dir_path, gh_tokens) :     
    n_tokens = len(gh_tokens)

    args = [ (task_get_commits, gh_tokens[ order % n_tokens ], (data['repo_id'], data['order'], data['num'], data['url'], output_dir_path)) for order, data in enumerate(args) ]
    executor = ParallelExecutor(50)
    executor.run( args )

if __name__ == '__main__' : 
    in_args = DataFileReader.from_json(sys.argv[1])
    input_file_path = in_args['input_file_path']
    output_dir_path = in_args['output_dir_path']
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 

    dataset = DataFileReader.from_json(input_file_path)

    download(dataset, output_dir_path, gh_tokens)