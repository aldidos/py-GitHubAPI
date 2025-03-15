from pyGitHubAPI.github_api import ghAPI
from requests import Response

class Pagenator : 

    def __init__(self, res) : 
        self.cur_res = res

    def __iter__(self) :         
        return self
    
    def __next__(self) : 
        next = self.cur_res.links.get('next')
        if next : 
            url = next['url']
            self.cur_res = ghAPI.get_req(url)
            return self.cur_res
        else :
            raise StopIteration
