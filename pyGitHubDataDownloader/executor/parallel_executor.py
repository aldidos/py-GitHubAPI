import concurrent.futures
from pyGitHubAPI.util import delay
from pyGitHubAPI.config import make_headers
from requests import Session
from requests.adapters import HTTPAdapter

class ParallelExecutor:

    def __init__(self, max_workers=10):
        self.max_workers = max_workers
        self.session = None
                
        # 2. 세션 멤버 변수화 및 커넥션 풀 최적화
        self.session = Session()
        # pool_maxsize를 쓰레드 개수에 맞춰서 병목 현상 방지
        adapter = HTTPAdapter(
            pool_connections=self.max_workers, 
            pool_maxsize=self.max_workers
        )
        self.session.mount('https://', adapter)        

    def _execute(self, task_func, token, *args) : 
        headers = make_headers(token)
        response = None
        while True:
            try:                
                # 콜백 함수에 토큰과 멤버 변수인 self.session을 함께 전달
                response, results = task_func(self.session, headers, *args)
                
                # if response.status_code == 403 or response.status_code == 429:
                if response.status_code in [403, 429] :
                    # reset_at = int(response.headers.get('x-ratelimit-reset', time.time() + 3600))                    
                    print(f"⚠️ 토큰 제한 감지: {token}")
                    delay(response)
                    continue 
                
                return (response, results)
                
            except Exception as e:  
                print(f"❌ 실행 에러: {e}")
                return response, None

    def run(self, items): 
        # results = {} 
        responses = []
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 1. 아까 배운 딕셔너리 컴프리헨션으로 작업 등록
            # future_to_item = {
            #     executor.submit(task_func, *item, *args, **kwargs): item[0] 
            #     for item in items
            # }
            futures = [ executor.submit(self._execute, task_func, token, *args) for task_func, token, args in items ]

            # 2. 완료되는 순서대로 결과 수집
            # for future in concurrent.futures.as_completed(future_to_item):
            for future in concurrent.futures.as_completed(futures):
                # item_id = future_to_item[future]
                try:
                    res, result = future.result()
                    responses.append(res)
                    results.append(result)
                    # results[item_id] = result
                except Exception as e:
                    # results[item_id] = f"Error: {e}"
                    results.append( f"Error: {e}" )
        
        return responses, results
    