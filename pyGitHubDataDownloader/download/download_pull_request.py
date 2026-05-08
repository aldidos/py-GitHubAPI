import sys
sys.path.append('.')
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader
from pyGitHubDataDownloader.executor.parallel_executor import ParallelExecutor
from pathlib import Path
from requests import Session
from pyGitHubAPI.gh_api_session_caller import GhAPISessionCaller

def task_get_pull_requests(session : Session, headers, repo_id, owner, name, pr_number, output_base_path) : 
    session.headers.update(headers)
    output_path = Path(f'{output_base_path}/{repo_id}') 
    output_path.mkdir(exist_ok = True)    

    try :         
        res = GhAPISessionCaller.get_pull_request(session, owner, name, pr_number)
        if res.status_code == 200 : 
            output_file_path = f'{output_path}/{pr_number}.json'
            Path(output_file_path).write_text(res.text, encoding = 'utf-8')
            print(f'get {output_file_path}')
        else :
            print(f'{repo_id} error code = {res.status_code}')
        
    except Exception as e: 
        print(f'{e}')
    
    return res, None

def download(dataset, output_base_path, gh_tokens) : 
    n_workers = 256
    n_tokens = len(gh_tokens)

    args = [ (task_get_pull_requests, gh_tokens[order % n_tokens], (row['repo_id'], row['owner'], row['name'], row['pr_number'], output_base_path) ) for order, row in enumerate(dataset) ]
    executor = ParallelExecutor(n_workers)
    executor.run(args)

if __name__ == '__main__' : 
    in_args = DataFileReader.from_json(sys.argv[1])
    input_file_path = in_args['input_file_path']
    output_base_dir_path = in_args['output_base_dir_path']
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 

    dataset = DataFileReader.from_json(input_file_path)    
    
    download(dataset, output_base_dir_path, gh_tokens)    