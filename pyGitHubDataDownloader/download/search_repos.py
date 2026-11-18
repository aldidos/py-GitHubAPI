import asyncio
import aiohttp
from requests import Response, Session
from requests.utils import parse_header_links
from pathlib import Path
import json
from dotenv import load_dotenv
import os
load_dotenv()

async def req_get(url, session, headers, params) : 
    result = { 'data' : None, 'last_page' : None }
    async with session.get(url, headers=headers, timeout=15, params = params) as response : 
        if response.status == 200 :
            res_data = await response.json()
            result['data'] = res_data
            link_header = response.links
            last_link = link_header.get('last')
            if last_link : 
                last_page = int(last_link['url'].query.get('page')) 
                result['last_page'] = last_page
    return result

async def main() : 
    query = 'deep learning in:readme'
    token = os.getenv('GITHUB_TOKEN')
    params = {
        'q' : query, 
        'per_page' : 100, 
        'page' : 1
    }
    headers = {"Accept": "application/vnd.github+json", "Authorization" : f"Bearer {token}"}
    url = 'https://api.github.com/search/repositories' ####

    result = []

    connector = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=connector) as session: 
        print(url)
        res_result = await req_get(url, session, headers, params)
        result.extend(res_result['data']['items']) ####

        last_page = res_result['last_page']
        if last_page : 
            paged_requests = []
            
            for page in range(2, last_page + 1) : 
                print(page)
                params['page'] = page
                paged_requests.append( req_get(url, session, headers, params) )

             # 모든 페이지를 동시에 스크래핑
            paged_results = await asyncio.gather(*paged_requests)
            
            # 결과 병합
            for page_data in paged_results:
                if page_data:
                    result.extend(page_data['data']['items'])

    Path('./searched_repos.json').write_text(json.dumps(result), 'utf-8') ####

if __name__ == '__main__' : 
    asyncio.run(main())