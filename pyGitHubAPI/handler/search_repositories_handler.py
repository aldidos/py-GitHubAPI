from pyGitHubAPI.github_api import ghAPI
from requests import Response
import json

class SearchResult : 

    def __init__(self) : 
        self.items = []

    def add_items(self, items) : 
        self.items.extend(items)

    def get_items(self) : 
        return self.items
    
    def write_to_file(self, path) : 
        with open(path, mode = 'w', encoding = 'utf-8') as f : 
            json.dump(self.items, f)


class SearchRepositoriesHandler : 

    def __init__(self, q, sort = 'starts', order = 'desc', per_page = 100) : 
        self.q = q
        self.sort = sort
        self.order = order
        self.per_page = per_page
        self.searchResult = SearchResult()

    def get_repositories(self) : 
        print(f'GET search/repositories with query : {self.q}')
        res = ghAPI.get_search_repositories(self.q, self.sort, self.order, self.per_page)
        if res.status_code == 200 :
            result = json.loads( res.text )
            self.searchResult.add_items( result['items'] )

            self.get_repositories_from_next_page( res )

    def get_repositories_from_next_page(self, res : Response) :
        next = res.links.get('next')
        if next : 
            url = next['url']
            res = ghAPI.get_req(url)
            print(f'get repositories from {url}')

            if res.status_code == 200 : 
                result = json.loads( res.text )
                self.searchResult.add_items( result['items'] )

                self.get_repositories_from_next_page( res )            

    def get_search_result(self) -> SearchResult : 
        return self.searchResult

