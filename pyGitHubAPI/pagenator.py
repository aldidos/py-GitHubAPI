from pyGitHubAPI.github_api import ghAPI

class Pagenator : 

    def __init__(self, res) : 
        self.cur_res = res

    def __iter__(self) :         
        return self
    
    def __next__(self) : 
        next = self.cur_res.links.get('next')
        if next : 
            url = next['url']
            print(f'GET {url}')
            self.cur_res = ghAPI.get_req(url)
            if self.cur_res.status_code != 200 : 
                print(self.cur_res.status_code)
                print(self.cur_res.text)
            return self.cur_res
            
        else :
            raise StopIteration
