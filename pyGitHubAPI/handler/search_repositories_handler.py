from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.pagenator import pagenator
from requests import Response
import json

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
            
        return res

    def get_next_items(self, res : Response) :
        next_url = pagenator.get_next_page_url(res)
        if next_url :                     
            res = ghAPI.get_req(next_url)
            print(f'get repositories from {next_url}')

            if res.status_code == 200 : 
                result = json.loads( res.text )
                self.results( result['items'] )

                self.get_next_items( res )
