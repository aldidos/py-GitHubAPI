import sys
sys.path.append('.')
import csv
from pyGitHubDataDownloader.gh_content_explorer import GHContentExplorer
import multiprocessing
import json

def explorer_pull_request_template_markdown_file(repo_id, owner, name) : 
    print(repo_id)
    output_dir_path = './repo_content/REPO_MD_CONTENTS'
    contents = []
    
    result = GHContentExplorer.find_content_with(owner, name, '')
    contents.extend( result )

    result = GHContentExplorer.find_content_with(owner, name, '.github')
    contents.extend( result )

    result = GHContentExplorer.find_content_with(owner, name, '.github/PULL_REQUEST_TEMPLATE') ####
    contents.extend( result )
    
    with open(f'{output_dir_path}/{repo_id}.json', mode = 'w', encoding = 'utf-8') as f : 
        json.dump(contents, f)

if __name__ == '__main__' : 
    input_file_path = 'e:/research_pullreq_template_checklist/data/download_markdown_content.csv'
    
    with open(input_file_path, mode = 'r', encoding = 'utf-8-sig') as f : 
        reader = csv.DictReader(f)
        repo_list = [ ( row['repo_id'], row['owner'], row['name'] ) for row in reader  ]        
        
        with multiprocessing.Pool() as pool : 
            pool.starmap( explorer_pull_request_template_markdown_file,  repo_list )