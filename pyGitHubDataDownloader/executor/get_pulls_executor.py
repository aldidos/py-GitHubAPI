import sys
sys.path.append('.')
from pyGitHubAPI.github_api import ghAPI

class GetPullsExecutor : 

    def __init__(self, owner, repo, state = 'all', sort = 'created', per_page = 100) : 
        self.owner = owner
        self.repo = repo
        self.state = state
        self.sort = sort
        self.per_page = per_page

    def execute(self) : 
        res = ghAPI.get_list_pull_requests(self.owner, self.repo, self.state, self.sort, self.per_page)
        if res.status_code == 200 : 
            return res
        print(res.status_code)
        print(res.text)
        return None

