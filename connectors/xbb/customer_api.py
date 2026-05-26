
# connectors/xbb/customer_api.py — 销帮帮 客户 CRUD
# 后续新业务（订单、库存等）参照此文件新建对应 api.py

from config.settings import XBB, XBB_PAGE_SIZE
from connectors.xbb.client import XbbClient
from utils.logger import get_logger

logger = get_logger("XbbCustomerAPI")
_ep = XBB["endpoints"]
_base = {"corpid": XBB["corpid"], "userId": XBB["user_id"], "formId": XBB["form_id"]}


class XbbCustomerAPI:

    def __init__(self):
        self._client = XbbClient()

    def query_all(self) -> list[dict]:
        """分页拉取全量客户列表"""
        all_records, page = [], 1
        while True:
            payload = {**_base, "page": page, "pageSize": XBB_PAGE_SIZE}
            data = self._client.post(_ep["customer_list"], payload)
            records = data.get("result", {}).get("list", [])
            if not records:
                break
            all_records.extend(records)
            page += 1
        logger.debug(f"销帮帮客户拉取完成，共 {len(all_records)} 条")
        return all_records

    def create(self, name: str, type_name: str) -> dict:
        payload = {**_base, "dataList": {
            "text_1":  name,
            "text_16": XBB["user_id"],
            "text_21": type_name,
        }}
        return self._client.post(_ep["customer_add"], payload)

    def update(self, data_id: int, name: str, type_name: str) -> dict:
        payload = {**_base, "dataId": data_id, "dataList": {
            "text_1":  name,
            "text_16": XBB["user_id"],
            "text_21": type_name,
        }}
        return self._client.post(_ep["customer_edit"], payload)

    def delete(self, data_id: int) -> dict:
        payload = {**_base, "dataId": data_id}
        return self._client.post(_ep["customer_delete"], payload)
