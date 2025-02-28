import sys
sys.path.append('.')
from pyGitHubAPI.handler.get_repository_readme_handler import getRepoREADMEHander
import json

def test_download_raw_readme() : 
    owner = 'sindresorhus'
    repo = 'awesome'

    readme_text = getRepoREADMEHander.download_raw_readme(owner, repo)
    print(readme_text)

def test_download_raw_readme_from_repository() : 
    file_path = './temp_search_result.json'
    with open(file_path, mode = 'r', encoding = 'utf-8') as f :
        list_repos = json.load(f)
        repository_data = list_repos[0]

        readme_text = getRepoREADMEHander.download_raw_readme_from_repository( repository_data )
        print(readme_text)

test_download_raw_readme()
# test_download_raw_readme_from_repository()