import asyncio
import logging
import re
from typing import List, Dict, Optional, Any
import aiohttp
from pyGitHubDataDownloader.token_manager import TokenManager

class GitHubPagedScraper:
    
    def __init__(self, tokens: List[str], max_concurrent_requests: int = 30):    
        self.token_manager = TokenManager(tokens)
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)        

    def _parse_link_headers(self, link_header) -> Dict[str, int]:
        """Link 헤더를 분석하여 last 페이지와 next 페이지 존재 여부를 파악합니다."""
        info = {"last": None, "has_next": False}

        if not link_header:
            return info
            
        if link_header.get('next'):
            info["has_next"] = True        

        last_link = link_header.get('last')
        if last_link : 
            info["last"] = int(last_link['url'].query.get('page'))
    
        return info

    async def _fetch_single_page(
        self, 
        session: aiohttp.ClientSession, 
        url: str, 
        params : dict,
        headers: dict
    ) -> Dict[str, Any]:
        page = params['page']
        per_page = params['per_page']
        
        async with self.semaphore:
            try:                
                async with session.get(url, headers=headers, timeout=15, params = params) as response:
                    token = headers["Authorization"].replace("Bearer ", "")
                    self.token_manager.update_status(token, response.headers.get("X-RateLimit-Remaining"), response.headers.get("X-RateLimit-Reset"))
                    
                    if response.status == 200:
                        data = await response.json()
                        link_header = response.links

                        link_info = self._parse_link_headers(link_header)                        
                        
                        return {
                            "page": page,
                            "data": data,
                            "has_next": link_info["has_next"],
                            "is_empty": len(data) == 0,
                            "last_page" : link_info['last'],
                            "is_partial": len(data) < per_page  # per_page=100보다 적게 왔다면 마지막 페이지임
                        }
                    else:
                        logging.error(f"❌ 페이지 {page} 실패 (Status: {response.status})")
                        return {"page": page, "data": [], "has_next": False, "is_empty": True, "is_partial": True}
            except Exception as e:
                logging.error(f"💥 페이지 {page} 예외: {e}")
                return {"page": page, "data": [], "has_next": False, "is_empty": True, "is_partial": True}

    async def fetch_all_pages(self, session: aiohttp.ClientSession, base_url: str, params : dict) -> List[Dict]:
        token = await self.token_manager.get_available_token()
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json", "User-Agent": "GitHub-Paged-Miner-v3"}

        # 1. 1페이지 우선 요청 및 분석
        params['page'] = 1 ####
        first_page_res = await self._fetch_single_page(session, base_url, params, headers)
        
        all_data = first_page_res["data"]
        
        # 1페이지만 보고도 끝나는 경우 (데이터가 없거나, 100개 미만이거나, 다음 페이지가 없는 경우)
        if first_page_res["is_empty"] or first_page_res["is_partial"] or not first_page_res["has_next"]:
            logging.info(f"📄 단일 페이지 수집 완료 (총 {len(all_data)}건)")
            return all_data

        last_page = first_page_res['last_page']
        if last_page  :             
            temp_data = await self._fetch_remainder_pages_with_last_page_info( session, base_url, headers, params, last_page )
            if temp_data : ####
                all_data.extend(temp_data)
        else : 
            temp_data = await self._fetch_remainder_pages_with_window_size( session, base_url, headers, params )
            all_data.extend(temp_data)

        return all_data
    
    async def _fetch_remainder_pages_with_last_page_info(self, session: aiohttp.ClientSession, url, headers, params, last_page : int) : 
        all_data = []
        if last_page == 1:
            return

        # 4. [핵심] 2페이지부터 마지막 페이지까지 태스크를 동시에 생성하여 병렬 처리!
        tasks = []
        for page in range(2, last_page + 1):
            # 매번 새로운 토큰을 획득하여 다른 페이지 요청들에 골고루 로테이션 적용
            params['page'] = page
            page_token = await self.token_manager.get_available_token()
            page_headers = headers.copy()
            page_headers["Authorization"] = f"Bearer {page_token}"
            
            tasks.append(self._fetch_single_page(session, url, params, page_headers))
        
        # 모든 페이지를 동시에 스크래핑
        paged_results = await asyncio.gather(*tasks)
        
        # 결과 병합
        for page_data in paged_results:
            if page_data:
                all_data.extend(page_data['data'])
                
        return all_data
    
    async def _fetch_remainder_pages_with_window_size(self, session: aiohttp.ClientSession, url, headers, params) : 
        # 3. [핵심] 'last' 정보가 없을 때의 '낙관적 청크 병렬 수집' 루프
        current_page = 2
        window_size = 10 # 한 번에 동시에 찌를 페이지 수 (조절 가능)
        all_data = []
        
        logging.info(f"🚀 마지막 페이지 정보가 없습니다. {window_size}개 단위 낙관적 병렬 수집을 시작합니다.")
        
        while True:
            tasks = []
            logging.info(f"➔ 페이지 {current_page}부터 {current_page + window_size - 1}까지 동시 요청 중...")
            
            for page in range(current_page, current_page + window_size):
                params['page'] = page
                page_token = await self.token_manager.get_available_token()
                page_headers = headers.copy()
                page_headers["Authorization"] = f"Bearer {page_token}"
                tasks.append(self._fetch_single_page(session, url, params, page_headers))
            
            # window_size만큼 동시에 요청 날림
            chunk_results = await asyncio.gather(*tasks)
            
            # 정렬 (순서 보장)
            chunk_results.sort(key=lambda x: x["page"])
            
            end_sign_detected = False
            last_valid_index = len(chunk_results)
            
            # 청크 결과를 순서대로 분석하면서 종료 지점 탐색
            for idx, res in enumerate(chunk_results):
                if res["is_empty"]:
                    end_sign_detected = True
                    last_valid_index = idx
                    break
                
                all_data.extend(res["data"])
                
                if res["is_partial"] or not res["has_next"]:
                    end_sign_detected = True
                    last_valid_index = idx + 1
                    break
            
            if end_sign_detected:
                logging.info(f"🏁 마지막 페이지 도달 확인. 수집을 종료합니다. (총 {len(all_data)}건)")
                break
                
            # 끝이 발견되지 않았다면 다음 청크로 이동
            current_page += window_size
        
        return all_data