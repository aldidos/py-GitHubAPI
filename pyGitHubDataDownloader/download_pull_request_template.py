import sys
sys.path.append('.')
import csv
from pyGitHubDataDownloader.gh_content_downloader import GHContentDownloader

if __name__ == '__main__' : 
    downloader = GHContentDownloader('./repo_content/PULL_REQUEST_TEMPLATE', './error_logs/log_download_pull_request_templates.txt')
    repo_list_file_path = 'args_download_markdown_contents.csv'

    with open(repo_list_file_path, encoding = 'utf-8-sig') as f : 
        reader = csv.DictReader(f)

        for row in reader : 
            repo_id = row['repo_id']
            repo_owner = row['repo_owner']
            repo_name = row['repo_name']
            file_name = row['file_name']
            file_path = row['file_path']
            download_url = row['download_url']            

            try : 
                downloader.download( repo_id, repo_owner, repo_name, file_name, file_path, download_url )
            except : 
                downloader.log_message(f'{repo_id}\t{repo_owner}\t{repo_name}\t{file_path}\t{download_url}\tEXCEPT_ERROR\n')
    
    downloader.close()