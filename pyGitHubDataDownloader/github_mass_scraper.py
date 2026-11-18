from pyGitHubDataDownloader.token_manager import TokenManager
import asyncio
import logging
from typing import List, Dict, Callable, Any, Awaitable
import aiohttp
from pyGitHubDataDownloader.response_callbacks import default_response_callback

class GitHubMassScraper:
    def __init__(self, tokens: List[str], max_concurrent_requests: int = 30):
        self.token_manager = TokenManager(tokens)
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)      
        
    async def _execute_task(
        self, 
        session: aiohttp.ClientSession, 
        api_strategy: Callable[[aiohttp.ClientSession, Any, Dict[str, str]], Awaitable[Dict]],
        response_callback, 
        api_args, 
        response_args, 
        item_name: Any, 
        retries: int = 3
    ) -> Dict:
        """외부에서 주입된 api_strategy 함수를 토큰/세마포어 제어 하에 실행합니다."""
        for attempt in range(retries):
            token = await self.token_manager.get_available_token()
            
            # 공통 헤더 구성 (외부 함수에 전달용)
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Universal-GitHub-Miner-v3"
            }
            
            async with self.semaphore:
                try:
                    async with api_strategy(session, headers, *api_args) as response: 
                        remaining = response.headers.get("X-RateLimit-Remaining")
                        reset_time = response.headers.get("X-RateLimit-Reset")
                        self.token_manager.update_status(token, remaining, reset_time)
                        
                        if response.status == 200:
                            data = await response_callback(response, *response_args)
                            logging.info(f"[성공] {item_name} 처리 완료 (토큰 잔여: {remaining})")
                            return {"target" : item_name, "status": "success", "data": data}
                            
                        elif response.status == 404:
                            logging.warning(f"[없음] {item_name} - 404 Not Found")
                            return {"target" : item_name, "status": "not_found", "data": None}
                            
                        elif response.status in [403, 429]:
                            logging.warning(f"[제한] {item_name} 접근 중 차단(Status: {response.status}). 재시도.")
                            if attempt < retries - 1:
                                await asyncio.sleep(2 ** attempt)
                                continue
                        else:
                            logging.error(f"[에러] {item_name} - Status: {response.status}")
                            
                except Exception as e:
                    logging.error(f"[예외 발생] {item_name}: {str(e)}")
                    
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    
        return {"status": "failed", "data": None}
    
    async def _execute(self, session, api_strategy, response_callback, chunk) : 
        tasks = [self._execute_task(session, api_strategy, response_callback, args[0], args[1], order ) for order, args in enumerate(chunk)]
        temp_results = await asyncio.gather(*tasks, return_exceptions=True)  
        valid_results = [r['data'] for r in temp_results if isinstance(r, dict)]

        return valid_results

    async def run_by_chunks(
        self, 
        target_list: List[Any], 
        api_strategy: Callable[[aiohttp.ClientSession, Any, Dict[str, str]], Awaitable[Dict]],
        response_callback = default_response_callback,
        storage_callback: Callable[[List[Dict]], Awaitable[None]] = None, 
        chunk_size: int = 1000
    ) :
        connector = aiohttp.TCPConnector(limit=100, ttl_dns_cache=300)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            for i in range(0, len(target_list), chunk_size):
                chunk = target_list[i:i + chunk_size]
                logging.info(f"--- [청크 시작] {i}번째부터 {i + chunk_size}번째 아이템 수집 중 ---")

                valid_results = await self._execute(session, api_strategy, response_callback, chunk) 
                
                # [핵심] 저장소 콜백 함수도 비동기로 호출합니다.
                if storage_callback is not None : 
                    await storage_callback(valid_results)
                
                logging.info(f"--- [청크 완료] {len(valid_results)}개 처리 및 저장 완료 ---") 

    async def run(
        self, 
        chunk: List[Any], 
        api_strategy: Callable[[aiohttp.ClientSession, Any, Dict[str, str]], Awaitable[Dict]],
        response_callback = default_response_callback
    ) : 
        connector = aiohttp.TCPConnector(limit=100, ttl_dns_cache=300)
        results = []
        
        async with aiohttp.ClientSession(connector=connector) as session: 
                temp_results = await self._execute(session, api_strategy, response_callback, chunk)
                results.extend( temp_results )

        return results 
                