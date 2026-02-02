from pyGitHubAPI.config import base_url, headers, token
from pyGitHubAPI.pagenator import Pagenator
import json
import requests
from requests import Response

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
    
    def get_search_repositories(self, q, sort = 'starts', order = 'desc', per_page = 100 ) -> Response : 
        params = {
            'q' : q, 
            'sort' : sort, 
            'order' : order, 
            'per_page' : per_page
        }
        url = f'{self.base_url}/search/repositories'
        return self.get_req(url, params)
    
    def get_repository_contents(self, owner, repo) : 
        uri = f'{self.base_url}/repos/{owner}/{repo}/contents'
        res = requests.get(uri, headers = headers)
        return res 

    def get_repository_content(self, owner, repo, path) : 
        uri = f'{self.base_url}/repos/{owner}/{repo}/contents/{path}'
        res = requests.get(uri, headers = headers)
        return res 
    
    def get_list_repository_issues(self, owner, repo, state = 'all', sort = 'created', per_page = 100) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/issues'
        params = {
            'state' : state, 
            'sort' : sort, 
            'per_page' : per_page
        }
        return self.get_req(url, params)
    
    def get_list_pull_requests(self, owner, repo, state = 'all', sort = 'created', per_page = 100, page = 1) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/pulls'
        params = {
            'state' : state, 
            'sort' : sort,
            'per_page' : per_page, 
            'page' : page
        }
        return self.get_req(url, params)
    
    def get_list_commits(self, owner, repo, path, per_page = 100, page = 1) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/commits'
        params = {
            'path' : path, 
            'per_page' : per_page, 
            'page' : page
        }
        return self.get_req(url, params)

    def get_a_commit(self, owner, repo, ref) : 
        url = f'{self.base_url}/repos/{owner}/{repo}/commits/{ref}'
        res = requests.get(url, headers = headers)
        return res
    
    def get_repository(self, owner, repo) : 
        uri = f'{self.base_url}/repos/{owner}/{repo}'
        res = requests.get(uri, headers = headers)
        return res
    
    def get_issue_events(self, owner, repo, number) : 
        url = f'{self.base_url}/repos/{owner}/{repo}/issues/{number}/events'
        res = requests.get(url, headers = headers)
        return res
    
    def get_issue_comments(self, owner, repo, number) : 
        url = f'{self.base_url}/repos/{owner}/{repo}/issues/{number}/comments'
        res = requests.get(url, headers = headers)
        return res
    
    def get_pull_request_reviews(self, owner, repo, number) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/pulls/{number}/reviews'
        params = {
            'per_page' : 100, 
            'page' : 1
        }
        return self.get_req(url, params)
    
    def get_pull_request_review_comments(self, owner, repo, number) : 
        url = f'{self.base_url}/repos/{owner}/{repo}/pulls/{number}/comments'
        res = requests.get(url, headers = headers)
        return res
    
    def get_list_review_comments(self, owner, repo, *, since = None, per_page = 100, page = 1) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/pulls/comments'
        qParams = {
            'per_page' : per_page, 
            'page' : page, 
            'since' : since
        }
        return self.get_req(url, qParams)
    
    def get_repository_contributors(self, owner, repo, *, anon = 'true', per_page = 100, page = 1) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/contributors'
        qParams = {
            'anon' : anon, 
            'per_page' : per_page, 
            'page' : page
        }
        return self.get_req(url, qParams)

    def get_req(self, url, params = None) : 
        res = requests.get(url, params = params, headers = self.headers ) 
        return res
    
    def get_rate_limit(self) : 
        url = f'{self.base_url}/rate_limit'
        res = requests.get(url, headers = headers)
        return res    

    def get_octocat(self) : 
        uri = f'{self.base_url}/octocat'
        res = requests.get(uri, headers = self.headers)
        return res

ghAPI = GitHubAPI(base_url, headers)