from requests import Response

class Pagenator : 

    def get_next_page_url(self, res : Response) :
        next = res.links.get('next')
        if next : 
            url = next['url']
            return url
        return None  
    
pagenator = Pagenator()