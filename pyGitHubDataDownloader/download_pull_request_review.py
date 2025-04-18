import sys
sys.path.append('.')
from pyGitHubDataDownloader.executor.get_pull_request_review_executor import getPRReviewExecutor
from pathlib import Path
import json

def download(file_path, output_dir) :
    with open(file_path, mode = 'r') as f : 
        dataset = json.load(f)

        for data in dataset : 
            pr_id = data['id']
            repo_id = data['base']['repo']['id']
            owner = data['base']['repo']['owner']['login']
            repo = data['base']['repo']['name']
            number = data['number']

            if Path(f'{output_dir}/{pr_id}.json').exists() : 
                continue

            try : 
                list_review = getPRReviewExecutor.execute(owner, repo, number)

                with open(f'{output_dir}/{pr_id}.json', mode = 'w', encoding = 'utf-8') as wf : 
                    json.dump(list_review, wf)

                print( f'{repo_id}/{pr_id}' )
            except : 
                pass 

if __name__ == '__main__' : 
    base_dir = 'e:/research_pullreq_template/PULL_REQUEST'
    base_dir_path = Path(base_dir)

    output_base_dir = './repo_content/PULL_REQUEST_REVIEW'
    for dir_path in base_dir_path.iterdir() : 
        print(dir_path.name)
        output_dir = Path(f'{output_base_dir}/{dir_path.name}')
        
        if not output_dir.exists() :             
            output_dir.mkdir()
            
        for file_path in dir_path.iterdir() : 
            download(file_path, output_dir)