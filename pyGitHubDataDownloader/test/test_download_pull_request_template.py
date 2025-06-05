import sys
sys.path.append('.')
import csv
from pyGitHubDataDownloader.prt_downloader import PRTDownloader

def test_download_pull_request_template(repo_id, repo_owner, repo_name, path) :
    downloader = PRTDownloader('./repo_content/PULL_REQUEST_TEMPLATE', './error_logs/log_download_pull_request_template.txt')
    downloader.download_pull_request_template(repo_id, repo_owner, repo_name, path)
    downloader.close()

if __name__ == '__main__' : 
    repo_id = 100057683
    repo_owner = 'britecharts'
    repo_name = 'britecharts-react'
    path = '.github'
    
    test_download_pull_request_template(repo_id, repo_owner, repo_name, path)    