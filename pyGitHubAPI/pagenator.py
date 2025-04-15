from pyGitHubAPI.github_api import ghAPI

class Pagenator : 

    def __init__(self, url, params = None) : 
        self.url = url
        self.cur_res = None
        self.params = params        

    def __iter__(self) :
        return self
    
    def __next__(self) : 
        if not self.cur_res : 
            self.cur_res = ghAPI.get_req(self.url, self.params)
            return self.cur_res

        next = self.cur_res.links.get('next')
        if next : 
            url = next['url']
            print(f'GET {url}')
            self.cur_res = ghAPI.get_req(url)            
            return self.cur_res
            
        else :
            raise StopIteration
