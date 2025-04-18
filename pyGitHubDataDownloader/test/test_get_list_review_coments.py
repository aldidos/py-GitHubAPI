import sys
sys.path.append('.')
from pyGitHubDataDownloader.executor.get_list_review_comments_executor import getListReviewCommentsExecotur

def test_get_list_review_comments() : 
    owner = 'node-red'
    repo = 'node-red'

    cur_page = 1

    res = getListReviewCommentsExecotur.execute(owner, repo, page = cur_page)

    if res : 
        next = res.links.get('next')
        if next :  
            cur_page += 1

            res = getListReviewCommentsExecotur.execute(owner, repo, page = cur_page)
            print(res.text)


test_get_list_review_comments()
