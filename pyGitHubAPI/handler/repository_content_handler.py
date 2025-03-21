import sys
sys.path.append('.')
from pyGitHubAPI.github_api import ghAPI
import json
import csv
from pathlib import Path

class RepositoryContentHandler : 

    def get_repository_content(self, owner, repo, path) :   
        res = ghAPI.get_repository_content(owner, repo, path)
        
        if res.status_code == 200 : 
            repo_content = json.loads(res.text)
            return repo_content
                
        return None
    
    def get_repository_contents(self, repos) : 
        repo_contents = []
        for repo in repos : 
            owner = repo['owner']
            name = repo['name']            
            path = repo['path']
            repo_content = self.get_repository_content(owner, name, path)
            if repo_content : 
                repo_contents.append( repo_content )

        return repo_contents
    
    def download_repository_content(self, owner, repo, path) : 
        repo_content = self.get_repository_content(owner, repo, path)

        if repo_content : 
            res = ghAPI.get_req( repo_content['download_url'] )
            return res.text

if __name__ == '__main__' : 
    input_file_path = './list_repo_pull_request_template_path.csv'

    executor = RepositoryContentHandler()

    with open(input_file_path, mode = 'r', encoding = 'utf-8') as f : 
        reader = csv.DictReader(f)
        for row in reader : 
             id = row['id']
             owner = row['owner'] 
             name = row['name']
             content_paths = row['pull_request_template paths']

             path = Path(f'./repo_content/PULL_REQUEST_TEMPLATE/{id}')
             if not path.exists() :
                path.mkdir()

             paths = content_paths.split(';')
             num = 1
            
             for p in paths :                  
                 content = executor.download_repository_content(owner, name, p)
                 output_path = f'./repo_content/PULL_REQUEST_TEMPLATE/{id}/{num}.md'
                 with open(output_path, mode = 'w', encoding = 'utf-8') as f : 
                    f.write( content )
                 num += 1
