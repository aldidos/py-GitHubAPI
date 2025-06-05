from pyGitHubAPI.github_api import ghAPI
from pyGitHubAPI.pagenator import Pagenator
import json

class GetPRReviewExecutor : 

    def execute(self, owner, repo, pr_number) : 
        pagenator = ghAPI.get_pull_request_reviews(owner, repo, pr_number)

        result = []
        for res in pagenator : 
            if res.status_code == 200 : 
                data = json.loads(res.text)
                result.extend(data)
            else : 
                print(res.status_code)
                raise Exception
            
        return result
    
getPRReviewExecutor = GetPRReviewExecutor()