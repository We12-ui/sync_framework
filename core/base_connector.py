
# core/base_connector.py — 平台连接器基类
# 所有平台（T+、销帮帮）的 HTTP 客户端继承此类

import time
import requests
from abc import ABC
from utils.logger import get_logger


class BaseConnector(ABC):
    """
    封装统一的 HTTP 请求 + 自动重试逻辑。
    子类只需提供 base_url 和 _build_headers()，
    然后调用 get() / post() 即可。
    """

    def __init__(self, base_url: str, timeout: int = 10, max_retry: int = 1):
        self.base_url  = base_url.rstrip('/')
        self.timeout   = timeout
        self.max_retry = max_retry
        self.logger    = get_logger(self.__class__.__name__)

    def _build_headers(self) -> dict:
        """子类覆盖：返回该平台所需的请求头（鉴权信息等）"""
        return {"Content-Type": "application/json"}

    def post(self, endpoint: str, payload: dict) -> dict:
        url = self.base_url + endpoint
        for attempt in range(1, self.max_retry + 2):   # +2 保证至少执行1次
            try:
                resp = requests.post(
                    url,
                    json=payload,
                    headers=self._build_headers(),
                    timeout=self.timeout
                )
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as e:
                self.logger.warning(f"POST {url} 第{attempt}次失败: {e}")
                if attempt <= self.max_retry:
                    time.sleep(2)
                else:
                    self.logger.error(f"POST {url} 已达最大重试次数，放弃")
                    raise
        return {}

    def get(self, endpoint: str, params: dict = None) -> dict:
        url = self.base_url + endpoint
        for attempt in range(1, self.max_retry + 2):
            try:
                resp = requests.get(
                    url,
                    params=params,
                    headers=self._build_headers(),
                    timeout=self.timeout
                )
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as e:
                self.logger.warning(f"GET {url} 第{attempt}次失败: {e}")
                if attempt <= self.max_retry:
                    time.sleep(2)
                else:
                    self.logger.error(f"GET {url} 已达最大重试次数，放弃")
                    raise
        return {}
