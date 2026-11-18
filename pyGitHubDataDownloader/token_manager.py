import asyncio
from typing import List, Dict, Optional, Callable, Any, Awaitable
import time
import logging
from requests import Session
from pyGitHubAPI.gh_api_session_caller import GhAPISessionCaller

class TokenManager:
    def __init__(self, tokens: List[str]):
        self.tokens_status = self.init_tokens_status(tokens)
        self.lock = asyncio.Lock()

    def init_tokens_status(self, tokens : List[str]) : 
        tokens_status = {}
        with Session() as session : 
            for token in tokens : 
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "Universal-GitHub-Miner-v3"
                }
                session.headers.update( headers )
                res = GhAPISessionCaller.get_rate_limit(session)

                remaining = res.headers.get("X-RateLimit-Remaining")
                reset_time = res.headers.get("X-RateLimit-Reset")

                tokens_status[token] = {"remaining": int(remaining), "reset_time": float(reset_time)}

        return tokens_status

    async def get_available_token(self) -> str:
        async with self.lock:
            while True:
                now = time.time()
                for token, status in self.tokens_status.items():
                    if status["remaining"] > 0:
                        status["remaining"] -= 1
                        return token
                
                earliest_reset = min(status["reset_time"] for status in self.tokens_status.values())
                sleep_duration = max(earliest_reset - now + 5, 10)
                logging.warning(f"⚠️ 모든 토큰 고갈. {int(sleep_duration)}초 대기...")
                await asyncio.sleep(sleep_duration)

    def update_status(self, token: str, remaining: Optional[str], reset_time: Optional[str]):
        if remaining is not None and reset_time is not None:
            self.tokens_status[token] = {"remaining": int(remaining), "reset_time": float(reset_time)}