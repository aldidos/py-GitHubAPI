import sys
sys.path.append('.')
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader
from pathlib import Path
import json
from pyGitHubDataDownloader.executor.parallel_executor import ParallelExecutor
from requests import Session
from pyGitHubAPI.gh_api_session_caller import GhAPISessionCaller

def task_get_repository(session : Session, headers, owner, repo, output_dir) : 
    session.headers.update(headers)
    res = GhAPISessionCaller.get_repository(session, owner, repo)    
    if res.status_code == 200 :         
        repository = json.loads( res.text )
        repo_id = repository['id']       
        Path(f'{output_dir}/{repo_id}.json').write_text(res.text, encoding ='utf-8')
        print(f'{repo_id} downloaded')        

    return res, None

def download_repository(dataset, output_dir, gh_tokens) : 
    num_tokens = len(gh_tokens)

    args = [ (task_get_repository, gh_tokens[ order % num_tokens ], (row['owner'], row['name'], output_dir) ) for order, row in enumerate(dataset) ]    
    executor = ParallelExecutor(50)
    executor.run( args )
     
if __name__ == '__main__' :     
    in_args = DataFileReader.from_json( sys.argv[1] ) 
    input_file_path = in_args['in_file_path']
    output_dir = in_args['output_dir_path']
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 

    csv_data = DataFileReader.from_csv(input_file_path)
    download_repository(csv_data, output_dir, gh_tokens) 