import requests
from pyGitHubAPI.util import delay

class Pagenator : 

    def __init__(self, session : requests.Session, url, params = None, headers = None) : 
        self.session = session
        self.url = url
        self.cur_res = None
        self.params = params
        self.headers = headers

    def __iter__(self) :
        return self
    
    def __next__(self) : 
        if not self.cur_res : 
            temp_res = self.session.get(url = self.url, params = self.params, headers = self.headers)
            if temp_res.status_code != 200 : 
                return temp_res 
            self.cur_res = temp_res
            print(f'GET {self.url}')
            return self.cur_res

        next = self.cur_res.links.get('next')
        if next :             
            url = next['url']
            print(f'GET {url}')
            temp_res = self.session.get(url = url, headers = self.headers)
            if temp_res.status_code != 200 : 
                return temp_res                
            self.cur_res = temp_res
            return self.cur_res
            
        else :
            raise StopIteration
        
    def paging(self, success_proc) : 
        res = None
        for res in self :  
            if res.status_code == 200 : 
                success_proc(res) 
            if res.status_code in [403, 429] : 
                delay(res)
            else : 
                break 
        return res