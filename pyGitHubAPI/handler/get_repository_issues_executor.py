from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.pagenator import Pagenator
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

            pagenator = Pagenator(res)
            for next_res in pagenator : 
                result = json.loads( next_res.text )
                self.result.extend( result )
        
        return self.result
    