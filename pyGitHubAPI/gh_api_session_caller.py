from pyGitHubAPI.config import base_url
from requests import Response, Session

class GhAPISessionCaller : 
    def get_repository_README(session : Session, owner, repo) : 
        url = f'{base_url}/repos/{owner}/{repo}/readme'
        return session.get(url) 
    
    def get_repository_contents(session : Session, owner, repo) : 
        uri = f'{base_url}/repos/{owner}/{repo}/contents'
        return session.get(uri) 

    def get_repository_content(session : Session, owner, repo, path) -> Response : 
        uri = f'{base_url}/repos/{owner}/{repo}/contents/{path}'
        return session.get(uri)
    
    def get_list_pull_requests(session : Session, owner, repo, state = 'all', sort = 'created', per_page = 100, page = 1) -> Response : 
        url = f'{base_url}/repos/{owner}/{repo}/pulls'
        params = {
            'state' : state, 
            'sort' : sort,
            'per_page' : per_page, 
            'page' : page
        }
        return session.get(url, params = params )
    
    def get_repository(session : Session, owner, repo) -> Response : 
        uri = f'{base_url}/repos/{owner}/{repo}'
        return session.get(uri) 
    
    def get_contributors(session : Session, owner, repo, per_page = 100, page = 1, anon = True ) -> Response : 
        url = f'{base_url}/repos/{owner}/{repo}/contributors'
        params = {            
            'per_page' : per_page, 
            'page' : page,
            'anon' : anon
        }
        return session.get(url, params = params )    

    def get_list_review_comments(session : Session, owner, repo, *, since = None, per_page = 100, page = 1) -> Response : 
        url = f'{base_url}/repos/{owner}/{repo}/pulls/comments'
        params = {
            'per_page' : per_page, 
            'page' : page, 
            'since' : since
        }
        return session.get(url, params = params ) 

    def get_issue_timeline_events(session : Session, owner, repo, per_page = 100, page = 1) -> Response : 
        url = f'{base_url}/repos/{owner}/{repo}/issues/events'
        params = {            
            'per_page' : per_page, 
            'page' : page
        }
        return session.get(url, params = params)    
    
    def get_rate_limit(session : Session) : 
        url = f'{base_url}/rate_limit'
        res = session.get(url)
        return res    

    def get_octocat(session : Session) : 
        url = f'{base_url}/octocat'
        res = session.get(url)
        return res