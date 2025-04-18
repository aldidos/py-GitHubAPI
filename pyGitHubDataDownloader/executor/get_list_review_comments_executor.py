from pyGitHubAPI.github_api import ghAPI

class GetListReviewComments : 

    def execute(self, owner, repo, page) : 
        res = ghAPI.get_list_review_comments(owner, repo, page = page)
        if res.status_code == 200 : 
            return res
        return None
    
getListReviewCommentsExecotur = GetListReviewComments()