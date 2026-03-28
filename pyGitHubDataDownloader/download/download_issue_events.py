import sys
sys.path.append('.')
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader
from pyGitHubDataDownloader.executor.parallel_executor import ParallelExecutor
from pyGitHubAPI.config import base_url
from pyGitHubAPI.gh_api_session_caller import GhAPISessionCaller
from pyGitHubAPI.pagenator import Pagenator
from pathlib import Path
from requests import Session

def task_get_issue_timeline_events(session : Session, headers, repo_id, owner, name, page, output_base_dir_path) : 
    session.headers.update(headers)
    res = GhAPISessionCaller.get_issue_timeline_events( session, owner, name, page = page ) 

    output_dir = f'{output_base_dir_path}/{repo_id}'
    Path(output_dir).mkdir(exist_ok = True)

    if res.status_code == 200 : 
        output_file_name = f'{output_dir}/{page}.json'
        Path(f'{output_dir}/{output_file_name}').write_text(res.text, encoding = 'utf-8')

    return res, None

def download(dataset, output_base_dir_path, gh_tokens) : 
    n_tokens = len(gh_tokens)
    
    args = [ ( task_get_issue_timeline_events, gh_tokens[order %n_tokens], (row['repo_id'], row['owner'], row['name'], row['page'], output_base_dir_path) ) for order, row in enumerate(dataset) ]
    executor = ParallelExecutor(50)
    executor.run(args)

if __name__ == '__main__' :  
    in_args = DataFileReader.from_json(sys.argv[1])
    input_file_path = in_args['input_file_path']
    output_base_dir_path = in_args['output_base_dir_path']
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 

    dataset = DataFileReader.from_csv( input_file_path )
    
    download(dataset, output_base_dir_path, gh_tokens)
    