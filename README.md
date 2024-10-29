
# GTPv2 Traffic Validation System

## 項目概述
此項目實現了一個基於F5 BIG-IP iRule的GTPv2流量驗證系統。它可以攔截並分析GTP流量，提取關鍵資訊（MSISDN、IMSI、MEI、APN、Cell ID），並通過API進行驗證。

## 系統架構
- **F5 BIG-IP iRule**: 
  - 攔截GTPv2流量
  - 提取關鍵資訊
  - 發送API請求進行驗證
  - 根據驗證結果決定流量處理方式
- **驗證API服務器**:
  - 接收驗證請求
  - 記錄請求資訊
  - 提供驗證結果
  - 支援未來擴展的資料庫整合

## 功能特點
- GTPv2協議支援
- 即時流量驗證
- 詳細日誌記錄
- 可配置的API重試機制
- 靈活的錯誤處理
- 支援未來擴展

## 快速開始

### 1. iRule部署

1. 登入F5 BIG-IP管理界面
2. 導航至Local Traffic > iRules
3. 點擊Create
4. 複製並貼上`GTPv2_irule.txt`中的代碼
5. 保存並應用到相應的Virtual Server (Virtual Server Profile記得選 GTP)
6. 此irule 有另外呼叫二個irule 來發送api request,請參考以下連結。
    https://clouddocs.f5.com/api/irules/HTTP-Super-SIDEBAND-Requestor-Client-Handles-Redirects-Cookies-Chunked-Transfer-APM-Access-etc.html

第六步驟的延伸
1. HSSR.tcl放進F5 irule
2. HSSR_reporter.tcl 放進F5 iruleˇ
3. 使用注意事項，請參考HSSR_注意事項.png

### 2. API服務器設置

#### 前置需求
```bash
# 更新系統包
sudo apt-get update

# 安裝Python3和pip3
sudo apt-get install -y python3 python3-pip
```

#### 安裝步驟
1. 創建項目目錄：
```bash
mkdir gtp_validation
cd gtp_validation
```

2. 創建API服務器文件：
```bash
# 將api_server.py的內容保存到文件
vim api_server.py
```

3. 安裝依賴：
```bash
sudo pip3 install flask
```

4. 運行服務器：
```bash
sudo python3 api_server.py
```

## 配置說明

### iRule配置參數
```tcl
# API端點配置
set static::api_host "10.8.52.101"
set static::api_uri "/validate-gtp"

# API調用設置
set static::api_timeout 10000    # 超時時間（毫秒）
set static::api_retries 2        # 重試次數
set static::retry_delay 1000     # 重試延遲（毫秒）
```

### API服務器配置
```python
# 服務器設置
host = '0.0.0.0'    # 監聽所有接口
port = 80           # 監聽端口

# 日誌配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s|%(levelname)s|%(message)s'
)
```

## API接口文檔

### 驗證請求
- **端點**: `/validate-gtp`
- **方法**: POST
- **內容類型**: application/json
- **請求體格式**:
```json
{
    "msisdn": "string",
    "imsi": "string",
    "mei": "string",
    "apn": "string",
    "cell_id": "string"
}
```
- **響應格式**:
```json
{
    "status": "success",
    "message": "string"
}
```

## 測試

1. 測試API服務器：
```bash
curl -X POST http://localhost/validate-gtp \
     -H "Content-Type: application/json" \
     -d '{"msisdn":"601123610212","imsi":"502121574062062","mei":"8603640554218778","apn":"unet.mnc012.mcc502.gprs","cell_id":"86276072"}'
```

2. 查看日誌：
```bash
tail -f gtp_validation.
```

3. 使用gtp_traffic 測試封包打向F5

可以使用tcprewrite 及tcpreplay 的工具修改封包後打向F5 , 測試irule 運作。

## 未來擴展
- 資料庫整合
- 高級驗證規則
- Web管理界面
- 監控和告警功能
- 負載均衡支援

## 注意事項
- API服務器需要root權限才能監聽80端口
- 生產環境部署時建議添加安全措施（SSL/TLS、認證等）
- 建議使用正確的Web服務器（如nginx）做反向代理
- 定期檢查和備份日誌文件

## 問題排查

### 常見問題
1. API連接超時
   - 檢查網絡連接
   - 確認API服務器運行狀態
   - 調整超時設置

2. iRule部署問題
   - 確認語法正確
   - 檢查Virtual Server配置
   - 查看F5設備日誌

### 日誌說明
- iRule日誌格式：
```
timestamp|msisdn|imsi|mei|apn|cell_id|api_status|error_message
```

- API服務器日誌格式：
```
timestamp|levelname|message
```

## 貢獻指南
歡迎提交Issue和Pull Request。請確保：
1. 代碼符合現有風格
2. 添加適當的測試
3. 更新相關文檔

## 許可證
[MIT License](LICENSE)
