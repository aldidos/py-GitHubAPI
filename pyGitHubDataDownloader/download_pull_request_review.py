import sys
sys.path.append('.')
from pyGitHubDataDownloader.executor.get_pull_request_review_executor import getPRReviewExecutor
from pathlib import Path
import json
import csv

error_log_prs = open('./error_logs/download_pull_request_review_pull_requests.txt', mode = 'w', encoding = 'utf-8')
error_log_repo = open('./error_logs/download_pull_request_review_repositories.txt', mode = 'w', encoding = 'utf-8')

def download(file_path, output_dir) :
    with open(file_path, mode = 'r') as f : 
        dataset = json.load(f)

        Path(output_dir).mkdir(exist_ok = True)

        for data in dataset : 
            pr_id = data['id']
            repo_id = data['base']['repo']['id']
            owner = data['base']['repo']['owner']['login']
            repo = data['base']['repo']['name']
            number = data['number']
            
            try : 
                list_review = getPRReviewExecutor.execute(owner, repo, number)

                with open(f'{output_dir}/{pr_id}.json', mode = 'w', encoding = 'utf-8') as wf : 
                    json.dump(list_review, wf)

                print( f'{repo_id}/{pr_id}' )
            except : 
                error_log_prs.write(f'{repo_id}\t{pr_id}\t{number}\n')

if __name__ == '__main__' :     
    input_file_path = './args/download_pull_request_reviews/list_repos.csv'
    output_base_dir = './repo_content/PULL_REQUEST_REVIEW'

    with open(input_file_path, encoding = 'utf-8-sig') as f : 
        reader = csv.DictReader(f)        
        
        for row in reader : 
            repo_id = row['repo_id']
            repo_dir = f'e:/research_pullreq_template/PULL_REQUEST/{repo_id}'
            repo_dir_path = Path(repo_dir)

            output_dir = Path(f'{output_base_dir}/{repo_id}')

            try :
                for file_path in repo_dir_path.iterdir() : 
                    download(file_path, output_dir)
            except : 
                error_log_repo.write(f'{repo_id}\n')

    error_log_prs.close()
    error_log_repo.close()
    ####         