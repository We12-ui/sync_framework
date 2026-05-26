
# connectors/tplus/token_manager.py
# T+ openToken 自动刷新，全局单例

import json
import os
import threading
import time
import requests
from utils.logger import get_logger
from config.settings import TPLUS, TOKEN_REFRESH_DAYS

logger = get_logger("TplusTokenManager")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), '../../data/tplus_token.json')


class TokenManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self):
        self._open_token    = TPLUS["open_token"]   # 兜底，立即会被刷新覆盖
        self._refresh_token = TPLUS["refresh_token"]
        self._token_lock    = threading.Lock()
        # 启动时立即刷新一次，之后定时续期
        self.refresh()
        self._start_auto_refresh()

    # ── 供连接器读取 ────────────────────────
    @property
    def open_token(self) -> str:
        with self._token_lock:
            return self._open_token

    # ── 刷新逻辑 ────────────────────────────
    def refresh(self):
        cfg = TPLUS
        try:
            logger.info("正在刷新 T+ openToken...")
            resp = requests.get(
                cfg["base_url"] + cfg["endpoints"]["refresh_token"],
                headers={
                    "Content-Type": "application/json",
                    "appKey":    cfg["app_key"],
                    "appSecret": cfg["app_secret"],
                },
                params={
                    "grantType":    "refresh_token",
                    "refreshToken": self._refresh_token,
                },
                timeout=10
            )
            data = resp.json()
            if str(data.get("code")) == "200":
                result = data["result"]
                with self._token_lock:
                    self._open_token    = result["access_token"]
                    self._refresh_token = result["refresh_token"]
                self._persist(result)
                logger.info(f"Token 刷新成功，有效期 {result['expires_in']}s")
            else:
                logger.error(f"Token 刷新失败: {data}")
        except Exception as e:
            logger.error(f"Token 刷新异常: {e}")

    def _persist(self, result: dict):
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        info = {
            "open_token":    result["access_token"],
            "refresh_token": result["refresh_token"],
            "expires_in":    result["expires_in"],
        }
        with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)

    def _start_auto_refresh(self):
        interval = TOKEN_REFRESH_DAYS * 24 * 3600

        def _loop():
            while True:
                time.sleep(interval)
                self.refresh()

        t = threading.Thread(target=_loop, name="TokenRefresher", daemon=True)
        t.start()
        logger.info(f"Token 自动刷新已启动，间隔 {TOKEN_REFRESH_DAYS} 天")
