import sys
sys.path.append('.')
from pyGitHubAPI.gh_api_session_caller import GhAPISessionCaller
from pyGitHubDataDownloader.util.data_file_rw import DataFileWriter, DataFileReader
from pyGitHubDataDownloader.executor.parallel_executor import ParallelExecutor
from requests import Session
import json

def get_dir_contents(session : Session, owner, name, path = '') : 
    contents = []

    res = GhAPISessionCaller.get_repository_content(session, owner, name, path)
    if res.status_code == 200 : 
        temp_contents = json.loads( res.text ) 
        contents.extend( temp_contents )

        for temp_content in temp_contents : 
            if temp_content['type'] == 'dir' : 
                content_path = temp_content['path']
                res, t_contents = get_dir_contents(session, owner, name, content_path)
                if res.status_code == 200 : 
                    contents.extend( t_contents ) 
    
    return res, contents

def task_explorer_pull_request_template_markdown_file(session : Session, headers, repo_id, owner, name, output_dir) : 
    session.headers.update(headers)    
    res, contents = get_dir_contents(session, owner, name)

    if res.status_code == 200 : 
        DataFileWriter.to_json(f'{output_dir}/{repo_id}.json', contents)

    return res, None

def download( dataset, output_dir, gh_tokens ) : 
    num_works = 128
    n_tokens = len(gh_tokens)

    args = [ (  task_explorer_pull_request_template_markdown_file, gh_tokens[order % n_tokens], (row['repo_id'], row['owner'], row['name'], output_dir)) for order, row in enumerate(dataset) ]
    executor = ParallelExecutor(num_works)
    executor.run( args )

if __name__ == '__main__' : 
    in_args =  DataFileReader.from_json(sys.argv[1])
    input_file_path = in_args['input_file_path']
    output_dir = in_args['output_dir_path']
    gh_tokens = DataFileReader.from_json( in_args['gh_token_file_path'] ) 

    dataset = DataFileReader.from_csv(input_file_path)

    download(dataset, output_dir, gh_tokens) 
    