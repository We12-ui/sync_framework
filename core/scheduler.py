
# core/scheduler.py — 统一任务调度器
# 注册所有 Job，统一管理轮询间隔

import time
import threading
from core.base_job import BaseJob
from utils.logger import get_logger

logger = get_logger("Scheduler")


class Scheduler:
    """
    管理多个 Job 的周期性执行。
    每个 Job 在独立线程中运行，互不阻塞。

    用法
    ----
    scheduler = Scheduler(interval_sec=5)
    scheduler.register(XbbToTplusPartnerJob())
    scheduler.register(TplusToXbbPartnerJob())
    scheduler.start()          # 阻塞运行（Ctrl+C 退出）
    """

    def __init__(self, interval_sec: int = 5):
        self.interval = interval_sec
        self._jobs: list[BaseJob] = []

    def register(self, job: BaseJob):
        self._jobs.append(job)
        logger.info(f"已注册任务: {job.job_name}")

    def start(self):
        if not self._jobs:
            logger.warning("没有任何已注册的任务，调度器退出")
            return

        logger.info(f"调度器启动，共 {len(self._jobs)} 个任务，间隔 {self.interval}s")

        # 首轮：各 Job 立即执行一次
        self._run_all()

        try:
            while True:
                time.sleep(self.interval)
                self._run_all()
        except KeyboardInterrupt:
            logger.info("收到停止信号，调度器已退出")

    def _run_all(self):
        threads = [
            threading.Thread(target=job.run, name=job.job_name, daemon=True)
            for job in self._jobs
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
