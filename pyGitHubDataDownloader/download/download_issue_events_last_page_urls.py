import sys
sys.path.append('.')
from pyGitHubDataDownloader.util.data_file_rw import DataFileReader, DataFileWriter
from pyGitHubDataDownloader.executor.parallel_executor import ParallelExecutor
from pyGitHubAPI.gh_api_session_caller import GhAPISessionCaller
from requests import Session

def task_get_issue_timeline_event_last_page_urls(session : Session, headers, repo_id, owner, name) : 
    session.headers.update(headers)
    res = GhAPISessionCaller.get_issue_timeline_events( session, owner, name )    

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
    
    args = [ ( task_get_issue_timeline_event_last_page_urls, gh_tokens[order %n_tokens], (row['repo_id'], row['owner'], row['name']) ) for order, row in enumerate(dataset) ]
    executor = ParallelExecutor(50)
    return executor.run(args)

if __name__ == '__main__' :  
    in_args = DataFileReader.from_json(sys.argv[1])
    input_file_path = in_args['input_file_path']
    output_file_path = in_args['output_file_path']
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 

    dataset = DataFileReader.from_csv( input_file_path )
    
    res_list, results = download(dataset, gh_tokens)
    DataFileWriter.to_json(output_file_path, results)
    