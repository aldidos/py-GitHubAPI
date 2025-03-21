import sys
sys.path.append('.')
from pyGitHubAPI.handler.repository_content_handler import RepositoryContentHandler

def test_download_repository_content() : 
    owner = 'rethinkdb'
    repo = 'rethinkdb'
    path = '.github/PULL_REQUEST_TEMPLATE'    

    repositoryCenterHandler = RepositoryContentHandler()

    content = repositoryCenterHandler.download_repository_content(owner, repo, path)
    print(content)

if __name__ == '__main__' : 
    test_download_repository_content()