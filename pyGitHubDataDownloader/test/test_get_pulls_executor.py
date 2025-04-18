import sys
sys.path.append('.')
from pyGitHubDataDownloader.executor.get_pulls_executor import GetPullsExecutor
from datetime import date

def test_execute() : 
    owner = 'sindresorhus'
    repo = 'awesome'

    executor = GetPullsExecutor(owner, repo, state='closed')
    res = executor.execute() 

    print(res.text)
    
test_execute()