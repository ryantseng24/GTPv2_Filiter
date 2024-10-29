from flask import Flask, request, jsonify
import logging
from datetime import datetime
import os

# 初始化Flask
app = Flask(__name__)

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s|%(levelname)s|%(message)s',
    handlers=[
        logging.FileHandler('gtp_validation.log'),
        logging.StreamHandler()
    ]
)

@app.route('/validate-gtp', methods=['POST'])
def validate_gtp():
    try:
        # 獲取當前時間
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 獲取請求數據
        data = request.get_json()
        
        # 提取字段
        msisdn = data.get('msisdn', '')
        imsi = data.get('imsi', '')
        mei = data.get('mei', '')
        apn = data.get('apn', '')
        cell_id = data.get('cell_id', '')
        
        # 記錄請求
        log_message = f"{timestamp}|{msisdn}|{imsi}|{mei}|{apn}|{cell_id}"
        logging.info(f"Received request: {log_message}")
        
        # 返回成功響應
        response = {
            "status": "success",
            "message": "Request recorded successfully"
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        # 記錄錯誤
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # 確保日誌目錄存在
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 啟動服務器
    app.run(host='0.0.0.0', port=80)
