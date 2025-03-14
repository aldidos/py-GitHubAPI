from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.pagenator import pagenator
from requests import Response
import json

class GetRepositoryIssuesExecutor : 

    def __init__(self, owner, repo, state = 'all', sort = 'created', per_page = 100) : 
        self.owner = owner
        self.repo = repo
        self.state = state
        self.sort = sort
        self.per_page = per_page
        self.result = []

    def execute(self) : 
        res = ghAPI.get_list_repository_issues(self.owner, self.repo, self.state, self.sort, self.per_page)
        if res.status_code == 200 : 
            result = json.loads( res.text )
            self.result.extend( result )
        
        return res 
    
    def get_next_items(self, res : Response) : 
        next_url = pagenator.get_next_page_url(res)
        if next_url : 
            res = ghAPI.get_req(next_url)

            if res.status_code == 200 : 
                result = json.loads( res.text )
                self.result.extend( result )

            return res 