import sys
sys.path.append('.')
import requests
from pathlib import Path
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader
from pyGitHubDataDownloader.executor.parallel_executor import ParallelExecutor

def task_get_repo_contents(session : requests.Session, headers, repo_id, path, dl_url, base_output_dir_path ) : 
    session.headers.update(headers)
    print(dl_url)    
    output_dir_path = f'{base_output_dir_path}/{repo_id}' ##

    res = session.get(dl_url)
    if res.status_code == 200 : 
        p = Path(f'{output_dir_path}/{path}')        
        Path(p.parents[0]).mkdir( parents = True, exist_ok = True) 
        p.write_text(res.text, encoding = 'utf-8')

    return res, None

def download_repo_contents( gh_tokens, dataset, base_output_dir_path) : 
    n_tokens = len(gh_tokens)
    
    args = [ ( task_get_repo_contents, gh_tokens[ order % n_tokens ], (row['repo_id'], row['path'], row['download_url'], base_output_dir_path) ) for order, row in enumerate(dataset) ]
    executor = ParallelExecutor(50)
    executor.run( args )

if __name__ == '__main__' : 
    in_args = DataFileReader.from_json( sys.argv[1] )
    in_csv_file_path = in_args['input_file_path']
    base_output_dir_path = in_args['output_dir_path']
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 

    dataset = DataFileReader.from_csv(in_csv_file_path)
    download_repo_contents(gh_tokens, dataset, base_output_dir_path)