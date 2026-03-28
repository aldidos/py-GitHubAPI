from requests.adapters import HTTPAdapter
from requests import Session

class GHSession :
    def __init__(self, pool_connections, pool_maxsize) : 
        self.session = None
                
        # 2. 세션 멤버 변수화 및 커넥션 풀 최적화
        self.session = Session()
        # pool_maxsize를 쓰레드 개수에 맞춰서 병목 현상 방지
        adapter = HTTPAdapter(
            pool_connections = pool_connections, 
            pool_maxsize = pool_maxsize
        )
        self.session.mount('https://', adapter)

    def get_session(self) : 
        return self.session