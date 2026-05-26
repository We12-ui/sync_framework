# T+ ↔ 销帮帮 双向同步框架

## 项目结构

```
sync_framework/
├── config/
│   ├── settings.py          # 全局密钥、接口地址、运行参数
│   └── field_maps.py        # 所有业务的字段映射表（统一维护）
│
├── core/
│   ├── base_connector.py    # 连接器基类（所有平台连接器继承此类）
│   ├── base_job.py          # 同步任务基类（所有业务Job继承此类）
│   ├── state_manager.py     # 状态快照管理（增/改/删 diff 通用逻辑）
│   └── scheduler.py         # 任务调度器（统一管理所有Job的轮询）
│
├── connectors/
│   ├── tplus/
│   │   ├── client.py        # T+ HTTP 客户端（封装鉴权、重试）
│   │   ├── token_manager.py # T+ openToken 自动刷新
│   │   └── partner_api.py   # T+ 客商 CRUD（可按业务继续扩展）
│   └── xbb/
│       ├── client.py        # 销帮帮 HTTP 客户端（封装签名、重试）
│       └── customer_api.py  # 销帮帮 客户 CRUD（可按业务继续扩展）
│
├── jobs/
│   ├── xbb_to_tplus_partner.py  # 业务Job：销帮帮→T+ 客商同步
│   └── tplus_to_xbb_partner.py  # 业务Job：T+→销帮帮 客商同步
│   # 后续新业务只需在这里新增一个 Job 文件 ↑
│
├── utils/
│   ├── logger.py            # 统一日志
│   └── crypto.py            # SHA256 签名等加密工具
│
├── data/                    # 运行时状态快照（自动生成，勿手动修改）
├── logs/                    # 运行日志（自动生成）
├── main.py                  # 启动入口
└── requirements.txt
```

## 快速上手

```bash
pip install -r requirements.txt
python main.py
```

## 新增一个业务对接（例如：T+ 销售订单 → 销帮帮）

1. **扩展 API 层**（如需要）
   - `connectors/tplus/order_api.py` — 封装 T+ 订单查询接口
   - `connectors/xbb/order_api.py`  — 封装销帮帮订单写入接口

2. **添加字段映射**
   - 在 `config/field_maps.py` 中新增 `ORDER_FIELD_MAP`

3. **新建 Job**
   - 在 `jobs/` 下新建 `tplus_to_xbb_order.py`
   - 继承 `BaseJob`，实现 `fetch_remote()` 和三个 handler

4. **注册到调度器**
   - 在 `main.py` 中 `scheduler.register(TplusToXbbOrderJob())`

完成，无需修改框架任何其他代码。
