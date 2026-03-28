import sys
sys.path.append('.')
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader, DataFileWriter
from pyGitHubDataDownloader.executor.parallel_process_executor import ParallelProcessExecutor
from pyGitHubAPI.gh_api_session_caller import GhAPISessionCaller
from requests import Session

def task_get_pr_last_page_url(session : Session, headers, repo_id, owner, repo, state) : 
    print(f'{repo_id}/{owner}/{repo}')
    session.headers.update(headers)
          
    res = GhAPISessionCaller.get_list_pull_requests(session, owner, repo, state, per_page = 100, page = 1)    
    last_url = None

    if res.status_code == 200 :  
        last = res.links.get('last')
        if last :             
            last_url = last['url'] 

    return res, {
        'repo_id' : repo_id, 
        'owner' : owner, 
        'name' : repo,
        'last_page_url' : last_url
    }

def download(dataset, gh_tokens) : 
    n_tokens = len(gh_tokens)
    dataset = [ ( task_get_pr_last_page_url, gh_tokens[ order % n_tokens], row['repo_id'], row['owner'], row['name'], 'closed') for order, row in enumerate(dataset) ]
    executor = ParallelProcessExecutor()
    results = executor.run(dataset)
    return results

if __name__ == '__main__' : 
    in_args = DataFileReader.from_json(sys.argv[1])
    input_file_path = in_args['input_file_path']
    output_file_path = in_args['output_file_path']
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 

    dataset = DataFileReader.from_csv(input_file_path)

    results = download(dataset, gh_tokens)
    results = [ result for res, result in results if result is not None ]
    DataFileWriter.to_json(output_file_path, results)   
