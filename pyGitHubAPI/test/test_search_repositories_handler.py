import sys
sys.path.append('.')
from pyGitHubAPI.handler.search_repositories_handler import SearchRepositoriesHandler, SearchResult

def test_get_repositories() : 
    q = 'deep learning in:readme'

    srh = SearchRepositoriesHandler(q)
    srh.get_repositories()

    sResult = srh.get_search_result()
    print( sResult.get_items() )

def test_write_to_file() : 
    q = 'deep learning in:readme'

    srh = SearchRepositoriesHandler(q)
    srh.get_repositories()

    sResult = srh.get_search_result()

    path = './temp_search_result.json'
    sResult.write_to_file(path)

# test_get_repositories()
# test_write_to_file()