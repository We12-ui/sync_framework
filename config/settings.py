
# config/settings.py — 全局密钥 & 接口地址
# 所有业务共用，修改一处全局生效


# ── 销帮帮 ──────────────────────────────────
XBB = {
    "token":   "a82cd11c02a6025e2edede3aff384ea6",
    "corpid":  "xbb536ad11596694a85986625fb19236093",
    "user_id": "1780664738596",
    "form_id": 9816986,
    "base_url": "https://appapi.xbongbong.com/pro/v2/api",
    "endpoints": {
        # 客商
        "customer_list":   "/customer/list",
        "customer_add":    "/customer/add",
        "customer_edit":   "/customer/edit",
        "customer_delete": "/customer/del",
        # 后续新业务在此追加，例如：
        # "order_list": "/order/list",
        # "order_add":  "/order/add",
    },
}

# ── 用友 T+ ─────────────────────────────────
TPLUS = {
    "app_key":       "FRC31Oz8",
    "app_secret":    "F1CBAB6C3AC28B7830216E88B8943BD2",
    "refresh_token": "d350634cbe774bdbb890b6b6ed7b9999",
    # open_token 无需填写，TokenManager 启动时自动通过 refresh_token 获取
    "open_token": "",
    "base_url": "https://openapi.chanjet.com",
    "endpoints": {
        # 鉴权
        "refresh_token": "/auth/v2/refreshToken",
        # 客商
        "partner_query":  "/tplus/api/v2/partner/Query",
        "partner_create": "/tplus/api/v2/partner/Create",
        "partner_update": "/tplus/api/v2/partner/Update",
        "partner_delete": "/tplus/api/v2/partner/Delete",
        # 后续新业务在此追加，例如：
        # "order_query":  "/tplus/api/v2/order/Query",
        # "order_create": "/tplus/api/v2/order/Create",
    },
}

# ── 运行参数 ─────────────────────────────────
SYNC_INTERVAL_SEC  = 5       # 同步轮询间隔（秒）
TOKEN_REFRESH_DAYS = 5       # T+ Token 刷新间隔（天）
MAX_RETRY          = 1       # 操作失败最大重试次数
REQUEST_TIMEOUT    = 10      # HTTP 请求超时（秒）
XBB_PAGE_SIZE      = 100     # 销帮帮分页拉取每页条数

# ── 业务规则 ─────────────────────────────────
# 新增客商后自动清理 T+ 占位编码
AUTO_DELETE_CODES: list[str] = ["0001", "0002", "0003", "0004", "0005"]
