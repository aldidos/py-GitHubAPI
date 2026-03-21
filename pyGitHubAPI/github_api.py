from pyGitHubAPI.config import base_url
import requests
from requests import Response

class GitHubAPI : 

    def __init__(self, headers) : 
        self.base_url = base_url
        self.headers = headers        
    
    def get_repository_README(self, owner, repo) : 
        uri = f'{self.base_url}/repos/{owner}/{repo}/readme'
        return requests.get(uri, headers = self.headers)        
    
    def get_search_repositories(self, q, sort = 'starts', order = 'desc', per_page = 100 ) -> Response : 
        params = {
            'q' : q, 
            'sort' : sort, 
            'order' : order, 
            'per_page' : per_page
        }
        url = f'{self.base_url}/search/repositories'
        return requests.get(url, params = params, headers = self.headers )
    
    def get_repository_contents(self, owner, repo) : 
        uri = f'{self.base_url}/repos/{owner}/{repo}/contents'
        return requests.get(uri, headers = self.headers)        

    def get_repository_content(self, owner, repo, path) : 
        uri = f'{self.base_url}/repos/{owner}/{repo}/contents/{path}'
        return requests.get(uri, headers = self.headers)
    
    def get_list_repository_issues(self, owner, repo, state = 'all', sort = 'created', per_page = 100) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/issues'
        params = {
            'state' : state, 
            'sort' : sort, 
            'per_page' : per_page
        }
        return requests.get(url, params = params, headers = self.headers )
    
    def get_list_pull_requests(self, owner, repo, state = 'all', sort = 'created', per_page = 100, page = 1) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/pulls'
        params = {
            'state' : state, 
            'sort' : sort,
            'per_page' : per_page, 
            'page' : page
        }
        return requests.get(url, params = params, headers = self.headers )
    
    def get_list_commits(self, owner, repo, path, per_page = 100, page = 1) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/commits'
        params = {
            'path' : path, 
            'per_page' : per_page, 
            'page' : page
        }
        return requests.get(url, params = params, headers = self.headers )

    def get_a_commit(self, owner, repo, ref) : 
        url = f'{self.base_url}/repos/{owner}/{repo}/commits/{ref}'
        return requests.get(url, headers = self.headers)        
    
    def get_repository(self, owner, repo) : 
        uri = f'{self.base_url}/repos/{owner}/{repo}'
        return requests.get(uri, headers = self.headers)        
    
    def get_issue_events(self, owner, repo, number) : 
        url = f'{self.base_url}/repos/{owner}/{repo}/issues/{number}/events'
        return requests.get(url, headers = self.headers)        
    
    def get_issue_comments(self, owner, repo, number) : 
        url = f'{self.base_url}/repos/{owner}/{repo}/issues/{number}/comments'
        return requests.get(url, headers = self.headers)        
    
    def get_pull_request_reviews(self, owner, repo, number) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/pulls/{number}/reviews'
        params = {
            'per_page' : 100, 
            'page' : 1
        }
        return requests.get(url, params = params, headers = self.headers )        
    
    def get_pull_request_review_comments(self, owner, repo, number) : 
        url = f'{self.base_url}/repos/{owner}/{repo}/pulls/{number}/comments'
        return requests.get(url, headers = self.headers)        
    
    def get_list_review_comments(self, owner, repo, *, since = None, per_page = 100, page = 1) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/pulls/comments'
        params = {
            'per_page' : per_page, 
            'page' : page, 
            'since' : since
        }
        return requests.get(url, params = params, headers = self.headers )        
    
    def get_repository_collaborators(self, owner, repo, *, affiliation = 'all', per_page = 100, page = 1) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/collaborators'
        params = {
            'affiliation' : affiliation, 
            'per_page' : per_page, 
            'page' : page
        }
        return requests.get(url, params = params, headers = self.headers )        
    
    def get_issue_timeline_events(self, owner, repo, issue_number, per_page = 100, page = 1) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/timeline'
        params = {            
            'per_page' : per_page, 
            'page' : page
        }
        return requests.get(url, params = params, headers = self.headers )    
    
    def get_issue_events(self, owner, repo, issue_number, per_page = 100, page = 1) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/events'
        params = {            
            'per_page' : per_page, 
            'page' : page
        }
        return requests.get(url, params = params, headers = self.headers ) 
    
    def get_contributors(self, owner, repo, per_page = 100, page = 1, anon = True ) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/contributors'
        params = {            
            'per_page' : per_page, 
            'page' : page,
            'anon' : anon
        }
        return requests.get(url, params = params, headers = self.headers )

    def get_req(self, url, params = None) -> Response : 
        res = requests.get(url, params = params, headers = self.headers ) 
        return res
    
    def get_rate_limit(self) : 
        url = f'{self.base_url}/rate_limit'
        res = requests.get(url, headers = self.headers)
        return res    

    def get_octocat(self) : 
        uri = f'{self.base_url}/octocat'
        res = requests.get(uri, headers = self.headers)
        return res

def make_headers(token) : 
    return {
        'Accept' : 'application/vnd.github+json', 
        'Authorization' : f'Bearer {token}'    
    }

def create_GitHubAPI(token) -> GitHubAPI : 
    headers = make_headers(token)
    return GitHubAPI(headers)
