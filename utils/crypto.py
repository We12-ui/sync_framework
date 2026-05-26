# utils/crypto.py — 签名 & 加密工具

import hashlib
import json


def sha256_sign(params: dict, token: str) -> str:
    """销帮帮接口签名：SHA256(JSON(params) + token)"""
    raw = json.dumps(params, separators=(',', ':'), ensure_ascii=False) + token
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()
