import requests
from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.util import delay

class Pagenator : 

    def __init__(self, url, params = None, headers = None) : 
        self.url = url
        self.cur_res = None
        self.params = params
        self.headers = headers

    def __iter__(self) :
        return self
    
    def __next__(self) : 
        if not self.cur_res : 
            res = ghAPI.get_rate_limit()
            delay(res)
            self.cur_res = requests.get(url = self.url, params = self.params, headers = self.headers)
            print(f'GET {self.url}')
            return self.cur_res

        next = self.cur_res.links.get('next')
        if next : 
            res = ghAPI.get_rate_limit()
            delay(res)
            url = next['url']
            print(f'GET {url}')
            self.cur_res = requests.get(url, headers = self.headers) 
            return self.cur_res
            
        else :
            raise StopIteration