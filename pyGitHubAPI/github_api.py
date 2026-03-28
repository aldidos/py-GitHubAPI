from pyGitHubAPI.config import base_url
import requests
from requests import Response, Session

class GitHubAPI : 

    def __init__(self, headers) : 
        self.base_url = base_url
        self.headers = headers        
    
    def get_repository_README(session : Session, owner, repo) : 
        url = f'{base_url}/repos/{owner}/{repo}/readme'
        return session.get(url) 
    
    def get_repository_contents(session : Session, owner, repo) : 
        uri = f'{base_url}/repos/{owner}/{repo}/contents'
        return session.get(uri) 

    def get_repository_content(session : Session, owner, repo, path) -> Response : 
        uri = f'{base_url}/repos/{owner}/{repo}/contents/{path}'
        return session.get(uri)
    
    def get_list_pull_requests(session : requests.Session, owner, repo, state = 'all', sort = 'created', per_page = 100, page = 1) -> Response : 
        url = f'{base_url}/repos/{owner}/{repo}/pulls'
        params = {
            'state' : state, 
            'sort' : sort,
            'per_page' : per_page, 
            'page' : page
        }
        return session.get(url, params = params )
    
    def get_list_commits(self, owner, repo, path, per_page = 100, page = 1) -> Response : 
        url = f'{self.base_url}/repos/{owner}/{repo}/commits'
        params = {
            'path' : path, 
            'per_page' : per_page, 
            'page' : page
        }
        return requests.get(url, params = params, headers = self.headers )
    
    def get_repository(session : requests.Session, owner, repo) -> Response : 
        uri = f'{base_url}/repos/{owner}/{repo}'
        return session.get(uri) 
    
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
    
    def get_contributors(session : Session, owner, repo, per_page = 100, page = 1, anon = True ) -> Response : 
        url = f'{base_url}/repos/{owner}/{repo}/contributors'
        params = {            
            'per_page' : per_page, 
            'page' : page,
            'anon' : anon
        }
        return session.get(url, params = params )

    def get_req(self, url, params = None) -> Response : 
        res = requests.get(url, params = params, headers = self.headers ) 
        return res
    
    def get_rate_limit(session : requests.Session) : 
        url = f'{base_url}/rate_limit'
        res = session.get(url)
        return res    

    def get_octocat(session : requests.Session) : 
        url = f'{base_url}/octocat'
        res = session.get(url)
        return res

def make_headers(token) : 
    return {
        'Accept' : 'application/vnd.github+json', 
        'Authorization' : f'Bearer {token}'    
    }

def create_GitHubAPI(token) -> GitHubAPI : 
    headers = make_headers(token)
    return GitHubAPI(headers)
