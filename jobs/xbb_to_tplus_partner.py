
# 业务 Job：销帮帮 → T+ 客商同步
from core.base_job import BaseJob
from connectors.xbb import XbbCustomerAPI
from connectors.tplus import TplusPartnerAPI
from config.field_maps import XBB_TO_TPLUS_PARTNER_TYPE
from config.settings import AUTO_DELETE_CODES
from utils.logger import get_logger

logger = get_logger("XbbToTplusPartner")


class XbbToTplusPartnerJob(BaseJob):

    # ── 基类必填属性 ────────────────────────
    job_name       = "xbb_to_tplus_partner"
    key_field      = "dataId"
    compare_fields = ["data.text_1", "data.text_21"]   # 名称、分类

    def __init__(self):
        super().__init__()
        self._xbb   = XbbCustomerAPI()
        self._tplus = TplusPartnerAPI()

    # ── 数据拉取 ────────────────────────────
    def fetch_remote(self) -> list[dict]:
        return self._xbb.query_all()

    # ── 钩子：新增前自动清理 T+ 占位数据 ────
    def before_sync(self, added, updated, deleted):
        if added:
            logger.info(f"检测到 {len(added)} 条新增，触发 T+ 占位数据清理...")
            for code in AUTO_DELETE_CODES:
                try:
                    self._tplus.delete(code)
                    logger.info(f"T+ 占位数据已清理: {code}")
                except Exception as e:
                    logger.warning(f"清理占位数据失败 {code}: {e}")

    # ── 增 ──────────────────────────────────
    def on_add(self, item: dict):
        d = item.get("data", {})
        type_code = XBB_TO_TPLUS_PARTNER_TYPE.get(d.get("text_21", ""), "01")
        result = self._tplus.create(
            code=str(item["dataId"]),
            name=d.get("text_1", ""),
            type_code=type_code,
            contact=d.get("text_15", ""),
        )
        logger.info(f"[ADD] T+ 新增客商 | dataId={item['dataId']} name={d.get('text_1')} | {result}")

    # ── 改 ──────────────────────────────────
    def on_update(self, item: dict):
        d = item.get("data", {})
        type_code = XBB_TO_TPLUS_PARTNER_TYPE.get(d.get("text_21", ""), "01")
        result = self._tplus.update(
            code=str(item["dataId"]),
            name=d.get("text_1", ""),
            type_code=type_code,
        )
        logger.info(f"[UPDATE] T+ 修改客商 | dataId={item['dataId']} name={d.get('text_1')} | {result}")

    # ── 删 ──────────────────────────────────
    def on_delete(self, item: dict):
        result = self._tplus.delete(str(item["dataId"]))
        logger.info(f"[DELETE] T+ 删除客商 | dataId={item['dataId']} name={item.get('data',{}).get('text_1')} | {result}")
