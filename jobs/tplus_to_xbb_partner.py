
# 业务 Job：T+ → 销帮帮 客商同步
from core.base_job import BaseJob
from connectors.tplus import TplusPartnerAPI
from connectors.xbb import XbbCustomerAPI
from config.field_maps import TPLUS_TO_XBB_PARTNER_TYPE
from utils.logger import get_logger

logger = get_logger("TplusToXbbPartner")


class TplusToXbbPartnerJob(BaseJob):

    # ── 基类必填属性 ────────────────────────
    job_name       = "tplus_to_xbb_partner"
    key_field      = "Code"
    compare_fields = ["Name", "PartnerType.Name"]   # 名称、客商性质

    def __init__(self):
        super().__init__()
        self._tplus = TplusPartnerAPI()
        self._xbb   = XbbCustomerAPI()

    # ── 数据拉取 ────────────────────────────
    def fetch_remote(self) -> list[dict]:
        return self._tplus.query_all()

    # ── 增 ──────────────────────────────────
    def on_add(self, item: dict):
        type_name = TPLUS_TO_XBB_PARTNER_TYPE.get(
            item.get("PartnerType", {}).get("Name", ""), "客户"
        )
        result = self._xbb.create(
            name=item.get("Name", ""),
            type_name=type_name,
        )
        logger.info(f"[ADD] 销帮帮 新增客户 | Code={item['Code']} name={item['Name']} | {result}")

    # ── 改 ──────────────────────────────────
    def on_update(self, item: dict):
        type_name = TPLUS_TO_XBB_PARTNER_TYPE.get(
            item.get("PartnerType", {}).get("Name", ""), "客户"
        )
        result = self._xbb.update(
            data_id=int(item["Code"]),
            name=item.get("Name", ""),
            type_name=type_name,
        )
        logger.info(f"[UPDATE] 销帮帮 修改客户 | Code={item['Code']} name={item['Name']} | {result}")

    # ── 删 ──────────────────────────────────
    def on_delete(self, item: dict):
        result = self._xbb.delete(data_id=int(item["Code"]))
        logger.info(f"[DELETE] 销帮帮 删除客户 | Code={item['Code']} name={item['Name']} | {result}")
