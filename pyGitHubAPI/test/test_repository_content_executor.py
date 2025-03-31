import sys
sys.path.append('.')
from pyGitHubAPI.executor.repository_content_executor import RepositoryContentExecutor

def test_download_repository_content() : 
    owner = 'rethinkdb'
    repo = 'rethinkdb'
    path = '.github/PULL_REQUEST_TEMPLATE'    

    repositoryCenterHandler = RepositoryContentExecutor()

    content = repositoryCenterHandler.download_repository_content(owner, repo, path)
    print(content)

if __name__ == '__main__' : 
    test_download_repository_content()