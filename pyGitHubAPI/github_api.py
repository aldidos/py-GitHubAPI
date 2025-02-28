from pyGitHubAPI.config import base_url, headers, token
import json
import requests

class GitHubAPI : 

    def __init__(self, base_url, headers) : 
        self.base_url = base_url
        self.headers = headers
        self.access_token = token
    
    def get_access_token(self) : 
        return json.dumps( { 'access_token' : self.access_token } )
    
    def get_repository_README(self, owner, repo) : 
        uri = f'{self.base_url}/repos/{owner}/{repo}/readme'
        res = requests.get(uri, headers = headers)
        return res 
    
    def get_search_repositories(self, q, sort = 'starts', order = 'desc', per_page = 100 ) : 
        params = {
            'q' : q, 
            'sort' : sort, 
            'order' : order, 
            'per_page' : per_page
        }
        uri = f'{self.base_url}/search/repositories'
        res = requests.get(uri, params = params, headers = self.headers)
        return res
    
    def get_repository_content(self, owner, repo, path) : 
        uri = f'{self.base_url}/repos/{owner}/{repo}/contents/{path}'        
        res = requests.get(uri, headers = headers)
        return res 

    def get_req(self, uri) : 
        res = requests.get(uri, headers = self.headers ) 
        return res

    def get_octocat(self) : 
        uri = f'{self.base_url}/octocat'
        res = requests.get(uri, headers = self.headers)
        return res

ghAPI = GitHubAPI(base_url, headers)