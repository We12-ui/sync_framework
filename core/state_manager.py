
# core/state_manager.py — 状态快照 & 增量 diff
# 通用逻辑，所有业务 Job 共用

import json
import os
from typing import Any
from utils.logger import get_logger

logger = get_logger("StateManager")

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)


class StateManager:
    """
    将上一轮数据快照持久化到 JSON 文件，
    提供 diff() 方法返回 (added, updated, deleted) 三个列表。

    参数
    ----
    job_name : str
        快照文件名前缀，每个 Job 独立隔离，互不干扰。
    key_field : str
        用于唯一标识一条记录的字段名（如 'dataId'、'Code'）。
    compare_fields : list[str]
        用于判断记录是否发生变更的字段列表。
    """

    # 改前
    # self._initialized = bool(self._last)

    # 改后
    # self._initialized = os.path.exists(self._file)

    def __init__(self, job_name: str, key_field: str, compare_fields: list[str]):
        self.key_field      = key_field
        self.compare_fields = compare_fields
        self._file          = os.path.join(DATA_DIR, f"{job_name}_state.json")
        self._last: list    = self._load()
        self._initialized = os.path.exists(self._file)  

    # ── 持久化 ──────────────────────────────
    def _load(self) -> list:
        try:
            with open(self._file, encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self, data: list):
        with open(self._file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self._last = data

    # ── 核心 diff ───────────────────────────
    def diff(self, current: list) -> tuple[list, list, list]:
        """
        返回 (added, updated, deleted)
        - added  : current 中有、last 中没有的记录
        - updated: 两边都有但 compare_fields 中任意一个字段值不同的记录
        - deleted: last 中有、current 中没有的记录
        """
        last_map    = {self._get_key(i): i for i in self._last}
        current_map = {self._get_key(i): i for i in current}

        added   = [i for k, i in current_map.items() if k not in last_map]
        deleted = [i for k, i in last_map.items()    if k not in current_map]
        updated = [
            i for k, i in current_map.items()
            if k in last_map and self._has_changed(last_map[k], i)
        ]
        return added, updated, deleted

    def is_first_run(self) -> bool:
        return not self._initialized

    # ── 内部工具 ────────────────────────────
    def _get_key(self, item: Any) -> str:
        """支持嵌套字段，如 'PartnerType.Name'（用点分隔）"""
        keys = self.key_field.split('.')
        val = item
        for k in keys:
            val = val.get(k, '') if isinstance(val, dict) else ''
        return str(val)

    def _has_changed(self, old: dict, new: dict) -> bool:
        for field in self.compare_fields:
            keys = field.split('.')
            old_v, new_v = old, new
            for k in keys:
                old_v = old_v.get(k, '') if isinstance(old_v, dict) else ''
                new_v = new_v.get(k, '') if isinstance(new_v, dict) else ''
            if old_v != new_v:
                return True
        return False
