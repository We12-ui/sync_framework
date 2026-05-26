import requests
from connectors.tplus.token_manager import TokenManager

tm = TokenManager()
resp = requests.post(
    "https://openapi.chanjet.com/tplus/api/v2/partner/Query",
    json={"param": {"pageIndex": 1, "pageSize": 10}},
    headers={
        "Content-Type": "application/json",
        "appKey": "FRC31Oz8",
        "appSecret": "F1CBAB6C3AC28B7830216E88B8943BD2",
        "openToken": tm.open_token,
    },
    timeout=10
)
print(resp.status_code, resp.text)