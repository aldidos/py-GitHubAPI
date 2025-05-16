import requests

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
            self.cur_res = requests.get(url = self.url, params = self.params, headers = self.headers)
            return self.cur_res

        next = self.cur_res.links.get('next')
        if next : 
            url = next['url']
            print(f'GET {url}')
            self.cur_res = requests.get(url, headers = self.headers) 
            return self.cur_res
            
        else :
            raise StopIteration
