
# connectors/tplus/client.py — T+ HTTP 客户端
# 自动携带鉴权头，openToken 由 TokenManager 维护

from core.base_connector import BaseConnector
from config.settings import TPLUS, REQUEST_TIMEOUT, MAX_RETRY
from connectors.tplus.token_manager import TokenManager


class TplusClient(BaseConnector):

    def __init__(self):
        super().__init__(
            base_url=TPLUS["base_url"],
            timeout=REQUEST_TIMEOUT,
            max_retry=MAX_RETRY,
        )
        self._token_mgr = TokenManager()

    def _build_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "appKey":    TPLUS["app_key"],
            "appSecret": TPLUS["app_secret"],
            "openToken": self._token_mgr.open_token,
        }
