import sys
sys.path.append('.')
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader
from pyGitHubDataDownloader.executor.parallel_executor import ParallelExecutor
from pyGitHubAPI.gh_api_session_caller import GhAPISessionCaller
from pathlib import Path
from requests import Session

def task_get_pull_request_review_comments(session : Session, headers, repo_id, owner, name, page, output_base_path) :  
    session.headers.update(headers)

    output_path = Path(f'{output_base_path}/{repo_id}')
    output_path.mkdir(exist_ok = True)

    res = GhAPISessionCaller.get_list_review_comments(session, owner, repo=name, per_page = 100, page = page)
    if res.status_code == 200 : 
        output_file_path = f'{output_path}/{page}.json'
        Path(output_file_path).write_text(res.text, encoding = 'utf-8')        
        page += 1
        print(output_file_path)

    return res, None

def download(dataset, output_base_path, gh_tokens) : 
    n_tokens = len(gh_tokens)
    
    dataset = [(task_get_pull_request_review_comments, gh_tokens[order % n_tokens], (row['repo_id'], row['owner'], row['name'], int(row['page']), output_base_path) ) for order, row in enumerate(dataset) ]
    executor = ParallelExecutor(50)
    executor.run(dataset)

if __name__ == '__main__' : 
    in_args = DataFileReader.from_json(sys.argv[1])
    input_file_path = in_args['input_file_path']
    output_dir_path = in_args['output_dir_path']
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 

    dataset = DataFileReader.from_csv(input_file_path)
    download(dataset, output_dir_path, gh_tokens)
