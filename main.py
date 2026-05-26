"""
main.py — 启动入口
==================
新增业务对接时，只需：
  1. 在 jobs/ 下新建 Job 文件
  2. 在下方 register 一行
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core.scheduler import Scheduler
from connectors.tplus.token_manager import TokenManager
from jobs.xbb_to_tplus_partner import XbbToTplusPartnerJob
from jobs.tplus_to_xbb_partner import TplusToXbbPartnerJob
from config.settings import SYNC_INTERVAL_SEC
from utils.logger import get_logger

logger = get_logger("Main")


def main():
    logger.info("=" * 50)
    logger.info("  T+ ↔ 销帮帮 同步框架启动")
    logger.info("=" * 50)

    TokenManager()

    scheduler = Scheduler(interval_sec=SYNC_INTERVAL_SEC)
    scheduler.register(XbbToTplusPartnerJob())
    scheduler.register(TplusToXbbPartnerJob())

    scheduler.start()

if __name__ == "__main__":
    main()
