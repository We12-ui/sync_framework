
# core/base_job.py — 同步任务基类
# 新增任何业务对接，只需继承此类并实现4个方法

from abc import ABC, abstractmethod
from utils.logger import get_logger
from core.state_manager import StateManager


class BaseJob(ABC):
    """
    业务同步任务基类。

    子类必须实现：
    - job_name()       : 任务唯一名称（用于日志和状态文件命名）
    - key_field()      : 记录唯一键字段名
    - compare_fields() : 变更检测字段列表
    - fetch_remote()   : 拉取远端最新数据，返回 list[dict]
    - on_add()         : 处理新增记录
    - on_update()      : 处理变更记录
    - on_delete()      : 处理删除记录

    子类可选覆盖：
    - before_sync()    : 同步前钩子（如：新增前自动清理占位数据）
    - after_sync()     : 同步后钩子（如：汇总统计、发送通知）
    """

    def __init__(self):
        self.logger = get_logger(self.job_name)
        self._state = StateManager(
            job_name=self.job_name,
            key_field=self.key_field,
            compare_fields=self.compare_fields,
        )

    # ── 子类必须声明的属性 ───────────────────
    @property
    @abstractmethod
    def job_name(self) -> str:
        """任务唯一名称，例如 'xbb_to_tplus_partner'"""

    @property
    @abstractmethod
    def key_field(self) -> str:
        """记录唯一键，例如 'dataId' 或 'Code'"""

    @property
    @abstractmethod
    def compare_fields(self) -> list[str]:
        """变更检测字段，例如 ['data.text_1', 'data.text_21']"""

    # ── 子类必须实现的方法 ───────────────────
    @abstractmethod
    def fetch_remote(self) -> list[dict]:
        """拉取远端平台的最新数据列表"""

    @abstractmethod
    def on_add(self, item: dict): ...

    @abstractmethod
    def on_update(self, item: dict): ...

    @abstractmethod
    def on_delete(self, item: dict): ...

    # ── 子类可选覆盖的钩子 ───────────────────
    def before_sync(self, added: list, updated: list, deleted: list):
        """同步前回调，默认空实现"""

    def after_sync(self, added: list, updated: list, deleted: list):
        """同步后回调，默认输出统计"""
        self.logger.info(
            f"本轮同步完成 — 新增:{len(added)} 修改:{len(updated)} 删除:{len(deleted)}"
        )

    # ── 框架调度入口（由 Scheduler 调用） ────
    def run(self):
        self.logger.info(f"[{self.job_name}] 开始同步...")
        try:
            current = self.fetch_remote()
        except Exception as e:
            self.logger.error(f"拉取数据失败，本轮跳过: {e}")
            return

        # 首次运行：仅建立基准快照，不触发任何操作
        if self._state.is_first_run():
            self._state.save(current)
            self.logger.info(f"首次初始化完成，已缓存 {len(current)} 条基准数据")
            return

        added, updated, deleted = self._state.diff(current)

        self.before_sync(added, updated, deleted)

        for item in added:
            self._safe_call(self.on_add, item, "ADD")

        for item in updated:
            self._safe_call(self.on_update, item, "UPDATE")

        for item in deleted:
            self._safe_call(self.on_delete, item, "DELETE")

        self._state.save(current)
        self.after_sync(added, updated, deleted)

    # ── 内部工具 ────────────────────────────
    def _safe_call(self, fn, item: dict, op: str):
        try:
            fn(item)
        except Exception as e:
            self.logger.error(f"{op} 操作异常: {e} | 数据: {item}")
