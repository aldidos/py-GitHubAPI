import sys
sys.path.append('.')
from pyGitHubDataDownloader.gh_data_collector import ghDataCollector
import multiprocessing
import csv

def main() : 
    file_name = 'repo_pr_review_list.csv'
    in_file_path = f'./args/download_pull_request_reviews/{file_name}'
    output_base_dir = './repo_content/PULL_REQUEST_REVIEW'
    with open(in_file_path, encoding = 'utf-8-sig') as f : 
        reader = csv.DictReader(f)
        dataset = [ ( row['repo_id'], row['pull_request_url'], row['pull_request_review_id'], output_base_dir) for row in reader ]    
        
        with multiprocessing.Pool() as pool :
            pool.starmap(ghDataCollector.get_pull_request_review, dataset)

if __name__ == '__main__' : 
    main()