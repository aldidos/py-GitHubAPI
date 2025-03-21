from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.pagenator import Pagenator
from requests import Response
import json
import time

class SearchRepositoriesHandler : 

    def __init__(self, q, sort = 'starts', order = 'desc', per_page = 100) : 
        self.q = q
        self.sort = sort
        self.order = order
        self.per_page = per_page
        self.results = []

    def get_repositories(self) : 
        print(f'GET search/repositories with query : {self.q}')
        res = ghAPI.get_search_repositories(self.q, self.sort, self.order, self.per_page)
        if res.status_code == 200 :
            result = json.loads( res.text )
            self.results.extend( result['items'] )

            pagenator = Pagenator(res)
            for next_res in pagenator : 
                result = json.loads( next_res.text )
                self.results.extend( result['items'] )
                time.sleep(10) 
            
        return self.results    
