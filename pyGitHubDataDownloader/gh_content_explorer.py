from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.util import delay
import json

class GHContentExplorer : 

    def find_content_with(repo_owner, repo_name, path) : 
        contents = []

        res = ghAPI.get_rate_limit()
        delay(res)

        res = ghAPI.get_repository_content(repo_owner, repo_name, path)
        if res.status_code == 200 : 
            temp_contents = json.loads( res.text ) 
            contents.extend( temp_contents )
       
        return contents