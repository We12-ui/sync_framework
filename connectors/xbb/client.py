
# connectors/xbb/client.py — 销帮帮 HTTP 客户端
# 自动计算 SHA256 签名并注入请求头

from core.base_connector import BaseConnector
from config.settings import XBB, REQUEST_TIMEOUT, MAX_RETRY
from utils.crypto import sha256_sign


class XbbClient(BaseConnector):

    def __init__(self):
        super().__init__(
            base_url=XBB["base_url"],
            timeout=REQUEST_TIMEOUT,
            max_retry=MAX_RETRY,
        )
        self._token = XBB["token"]
        self._current_payload: dict = {}   # 每次请求前由 post() 注入

    def _build_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "sign": sha256_sign(self._current_payload, self._token),
        }

    def post(self, endpoint: str, payload: dict) -> dict:
        """覆盖父类 post，先保存 payload 用于签名计算"""
        self._current_payload = payload
        return super().post(endpoint, payload)
