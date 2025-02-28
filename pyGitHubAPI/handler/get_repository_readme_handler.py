from pyGitHubAPI.github_api import ghAPI
import json

class GetRepoREADMEHandler : 

    def download_raw_readme(self, owner, repo) : 
        res = ghAPI.get_repository_README(owner, repo)
        
        if res.status_code == 200 : 
            result = json.loads( res.text )
            download_url = result['download_url']

            res = ghAPI.get_req(download_url) 
            if res.status_code == 200 : 
                return res.text
            
    def download_raw_readme_from_repository(self, repository : dict) : 
        owner = repository['owner']['login']
        repo = repository['name']

        return self.download_raw_readme(owner, repo)
        
getRepoREADMEHander = GetRepoREADMEHandler()