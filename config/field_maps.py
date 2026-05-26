
# config/field_maps.py — 所有业务字段映射
# 新增业务只需在此文件追加新的 MAP 字典


# ── 客商业务 ─────────────────────────────────

# 销帮帮 text_21 分类ID → T+ 客商类型编码
XBB_TO_TPLUS_PARTNER_TYPE: dict[str, str] = {
    "9de9f282-66b2-b860-18b7-4073dd07ed3c": "01",  # 客户
    "f12c4ebd-ec86-55bc-b99e-e0d2e63d0690": "00",  # 供应商
}

# T+ PartnerType.Name → 销帮帮分类名
TPLUS_TO_XBB_PARTNER_TYPE: dict[str, str] = {
    "客户":  "客户",
    "供应商": "供应商",
}

# ── 后续业务在下方追加 ────────────────────────
# 示例：销售订单状态映射
# XBB_TO_TPLUS_ORDER_STATUS: dict[str, str] = {
#     "draft":     "10",  # 草稿
#     "confirmed": "20",  # 已确认
#     "closed":    "30",  # 已关闭
# }
