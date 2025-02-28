from pyGitHubAPI.github_api import ghAPI
import json

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
