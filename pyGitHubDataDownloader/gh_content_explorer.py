from pyGitHubAPI.github_api import ghAPI, delay
import json
import re
import time

def is_pull_request_template(file_name : str) : 
    str = file_name.lower()
    mat = re.match('pull_request_template.md', str)
    if mat : 
        return True
    return False

class GHContentExplorer : 

    def find_content_with(repo_owner, repo_name, path, file_extension) : 
        contents = []
        res = ghAPI.get_repository_content(repo_owner, repo_name, path)
        if res.status_code == 200 : 
            temp_contents = json.loads( res.text ) 

            for content in temp_contents : 
                if content['name'].endswith(file_extension) : 
                    contents.append( content )
        
        delay(res)
        return contents
    
