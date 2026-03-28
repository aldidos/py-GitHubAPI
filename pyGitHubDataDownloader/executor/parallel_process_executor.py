from pyGitHubAPI.util import delay
from pyGitHubAPI.config import make_headers
from requests import Session
from requests.adapters import HTTPAdapter
import multiprocessing

class ParallelProcessExecutor:

    def __init__(self, pool_connections = 50, pool_maxsize = 50):
        # 2. 세션 멤버 변수화 및 커넥션 풀 최적화
        self.session = Session()
        # pool_maxsize를 쓰레드 개수에 맞춰서 병목 현상 방지
        adapter = HTTPAdapter(
            pool_connections = pool_connections, 
            pool_maxsize = pool_maxsize
        )
        self.session.mount('https://', adapter)

    def _execute(self, api_func, gh_token, *args) : 
        headers = make_headers(gh_token)
        while True:              
            response = None
            try:                
                # 콜백 함수에 토큰과 멤버 변수인 self.session을 함께 전달
                response, results = api_func(self.session, headers, *args)
                
                if response.status_code in [403, 429] : 
                    print(f"⚠️ 토큰 제한 감지: {gh_token}")
                    delay(response)
                    continue 
                
                return (response, results)
                
            except Exception as e: 
                print(f"❌ 실행 에러: {e}")
                return (response, None)

    def run(self, api_task_items): 
        with multiprocessing.Pool() as pool : 
            results = pool.starmap( self._execute, api_task_items ) 
            return results  