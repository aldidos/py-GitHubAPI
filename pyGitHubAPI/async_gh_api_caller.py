import aiohttp

class AsyncGHApiCaller : 

    def get_repositories(session : aiohttp.ClientSession, headers, repo_name ) : 
        url = f'https://api.github.com/repos/{repo_name}'
        return session.get(url, headers=headers, timeout=15)
    
    def get_contributors(session : aiohttp.ClientSession, headers, repo_name, per_page = 100, page = 1, anon = 'true' ) :
        url = f'https://api.github.com/repos/{repo_name}/contributors'
        params = {            
            'per_page' : per_page, 
            'page' : page,
            'anon' : anon
        }
        return session.get(url, headers = headers,  params = params, timeout=15 ) 
    
    def get_repository_README(session : aiohttp.ClientSession, headers, repo_name) : 
        url = f'https://api.github.com/repos/{repo_name}/readme'
        return session.get(url, headers = headers, timeout=15)
    
    def get_repository_contents(session : aiohttp.ClientSession, headers, repo_name) : 
        url = f'https://api.github.com/repos/{repo_name}/contents'
        return session.get(url, headers = headers, timeout=15) 

    def get_repository_content(session : aiohttp.ClientSession, headers, repo_name, path) : 
        url = f'https://api.github.com/repos/{repo_name}/contents/{path}'
        return session.get(url, headers = headers, timeout=15)
    
    def get_pull_requests(session : aiohttp.ClientSession, headers, repo_name, state = 'all', per_page = 100, page = 1) : 
        url = f'https://api.github.com/repos/{repo_name}/pulls'
        params = {
            'state' : state, 
            'per_page' : per_page, 
            'page' : page
        }
        return session.get(url, headers = headers, timeout=15, params = params )
    
    def get_an_pull_request(session : aiohttp.ClientSession, headers, repo_name, pull_number)  :         
        url = f'https://api.github.com/repos/{repo_name}/pulls/{pull_number}'
        return session.get(url, headers = headers, timeout=15)
    
    def get_issues(session : aiohttp.ClientSession, headers, repo_name, state = 'all', per_page = 100, page = 1) : 
        url = f'https://api.github.com/repos/{repo_name}/issues'
        params = {
            'state' : state, 
            'per_page' : per_page, 
            'page' : page
        }
        return session.get(url, headers = headers, timeout=15, params = params )
    
    def get_an_issue(session : aiohttp.ClientSession, headers, repo_name, issue_number)  : 
        url = f'https://api.github.com/repos/{repo_name}/issues/{issue_number}'
        return session.get(url, headers = headers, timeout=15)

    def get_commits(session : aiohttp.ClientSession, headers, repo_name, params)  : 
        url = f'https://api.github.com/repos/{repo_name}/commits'
        return session.get(url, headers = headers, params = params, timeout=15)
    
    def get_url(session : aiohttp.ClientSession, headers, url) : 
        return session.get(url, headers = headers, timeout=15)