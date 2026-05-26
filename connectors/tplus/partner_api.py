
# connectors/tplus/partner_api.py — T+ 客商 CRUD
# 后续新业务（订单、库存等）参照此文件新建对应 api.py

from config.settings import TPLUS
from connectors.tplus.client import TplusClient
from utils.logger import get_logger

logger = get_logger("TplusPartnerAPI")
_ep = TPLUS["endpoints"]


class TplusPartnerAPI:

    def __init__(self):
        self._client = TplusClient()

    # def query_all(self, page_size: int = 100) -> list[dict]:
    #
    #     """分页拉取全量客商，返回平铺列表"""
    #     all_records, page = [], 1
    #     while True:
    #         data = self._client.post(_ep["partner_query"], {
    #             "param": {"pageIndex": page, "pageSize": page_size}
    #         })
    #         records = data if isinstance(data, list) else []
    #         if not records:
    #             break
    #         all_records.extend(records)
    #         page += 1
    #     logger.debug(f"T+ 客商拉取完成，共 {len(all_records)} 条")
    #     return all_records

    def query_all(self, page_size: int = 100) -> list[dict]:
        all_records, page = [], 1
        while True:
            data = self._client.post(_ep["partner_query"], {
                "param": {"pageIndex": page, "pageSize": page_size}
            })
            records = data if isinstance(data, list) else []
            all_records.extend(records)
            if len(records) < page_size:  # 不足一页即为最后一页
                break
            page += 1
        logger.debug(f"T+ 客商拉取完成，共 {len(all_records)} 条")
        return all_records


    def create(self, code: str, name: str, type_code: str, contact: str = "") -> dict:
        return self._client.post(_ep["partner_create"], {"dto": {
            "Code": code,
            "Name": name,
            "PartnerType": {"Code": type_code},
            "PartnerAddresDTOs": [{"Contact": contact}],
        }})

    def update(self, code: str, name: str, type_code: str) -> dict:
        return self._client.post(_ep["partner_update"], {"dto": {
            "Code": code,
            "Name": name,
            "PartnerType": {"Code": type_code},
        }})

    def delete(self, code: str) -> dict:
        return self._client.post(_ep["partner_delete"], {"dto": {"Code": code}})

