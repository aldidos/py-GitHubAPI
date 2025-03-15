import sys
sys.path.append('.')
from pyGitHubAPI.handler.get_pulls_executor import GetPullsExecutor

def test_execute() : 
    owner = 'sindresorhus'
    repo = 'awesome'

    executor = GetPullsExecutor(owner, repo, state='closed')
    result = executor.execute()

    print( len(result) )
    print(result)

test_execute()
