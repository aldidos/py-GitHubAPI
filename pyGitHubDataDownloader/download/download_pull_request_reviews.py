import sys
sys.path.append('.')
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader
from pyGitHubDataDownloader.executor.parallel_executor import ParallelExecutor
from pathlib import Path
from requests import Session

def task_get_pull_request_review(session : Session, headers, repo_id, pull_request_url, pull_request_review_id, output_base_path) : 
    session.headers.update(headers)    

    output_path = Path(f'{output_base_path}/{repo_id}')
    output_path.mkdir(exist_ok = True)
    
    url = f'{pull_request_url}/reviews/{pull_request_review_id}'
    print(url)
    
    res = session.get(url)               
    if res.status_code == 200 : 
        output_file_path = f'{output_path}/{pull_request_review_id}.json'
        Path(output_file_path).write_text(res.text, encoding = 'utf-8')

    return res, None

def download(dataset, output_base_dir_path, gh_tokens) : 
    n_tokens = len(gh_tokens)
    
    dataset = [ ( task_get_pull_request_review, gh_tokens[ order % n_tokens], (row['repo_id'], row['pull_request_url'], row['pull_request_review_id'], output_base_dir_path) ) for order, row in enumerate(dataset) ]    
    executor = ParallelExecutor(50)
    executor.run(dataset)    

if __name__ == '__main__' : 
    input_file_path = sys.argv[1]
    output_base_dir_path = sys.argv[2]
    gh_token = sys.argv[3]

    dataset = DataFileReader.from_csv(input_file_path)
    download(dataset, output_base_dir_path, gh_token)