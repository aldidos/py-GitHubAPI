import sys
sys.path.append('.')
import csv
from pyGitHubDataDownloader.prt_downloader import PRTDownloader

if __name__ == '__main__' : 
    downloader = PRTDownloader('./repo_content/PULL_REQUEST_TEMPLATE', './error_logs/log_download_pull_request_templates.txt')
    repo_list_file_path = './args/download_PRT/repo_list.csv'

    with open(repo_list_file_path, encoding = 'utf-8-sig') as f : 
        reader = csv.DictReader(f)

        for row in reader : 
            repo_id = row['repo_id']
            owner = row['owner']
            name = row['name']
            path = '.github'

            try : 
                downloader.download_pull_request_template(repo_id, owner, name, path)
            except : 
                downloader.log_message(f'{repo_id}\t{owner}\t{name}\t{path}\tEXCEPT_ERROR\n')
    
    downloader.close()