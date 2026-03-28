import sys
sys.path.append('.')
from pyGitHubAPI.gh_api_session_caller import GhAPISessionCaller
from requests import Session
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader, DataFileWriter
from pyGitHubDataDownloader.executor.parallel_executor import ParallelExecutor

def download_pr_review_comment_last_page_url(session : Session, headers, repo_id, owner, name) : 
    session.headers.update(headers)    
    res = GhAPISessionCaller.get_list_review_comments(session, owner, name, per_page = 100, page = 1)
    print(f'{repo_id}/{owner}/{name}')
    last_url = None
    if res.status_code == 200 :             
        last = res.links.get('last')
        if last : 
            last_url = last['url'] 
    
    return res, {
        'repo_id' : repo_id,
        'owner' : owner, 
        'name' : name,
        'last_page_url' : last_url
    }

def download(dataset, gh_tokens) : 
    n_tokens = len(gh_tokens)
    args = [ ( download_pr_review_comment_last_page_url, gh_tokens[order % n_tokens], ( row['repo_id'], row['owner'], row['name'] ) ) for order, row in enumerate(dataset) ]

    executor = ParallelExecutor(50)
    results = executor.run( args )

    return results

if __name__ == '__main__' : 
    in_args = DataFileReader.from_json(sys.argv[1])
    input_file_path = in_args['input_file_path']
    output_file_path = in_args['output_file_path']
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 

    csv_dataset = DataFileReader.from_csv(input_file_path)
    results = download(csv_dataset, gh_tokens)
    results = [ result for res, result in results ]
    DataFileWriter.to_json(output_file_path, results) 