from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 啟用跨域支援，解決前後端分離問題

# 模擬資料庫 - 使用 JSON 檔案
DATA_FILE = 'data.json'

def load_data():
    """載入資料"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    """儲存資料"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """首頁"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """健康檢查端點"""
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}, 200

@app.route('/api/items', methods=['GET'])
def get_items():
    """取得所有項目"""
    data = load_data()
    return jsonify(data)

@app.route('/api/items', methods=['POST'])
def add_item():
    """新增項目"""
    try:
        item_data = request.get_json()
        
        # 驗證資料
        if not item_data or 'name' not in item_data:
            return jsonify({'error': '缺少必要欄位'}), 400
        
        # 載入現有資料
        data = load_data()
        
        # 建立新項目
        new_item = {
            'id': len(data) + 1,
            'name': item_data['name'],
            'description': item_data.get('description', ''),
            'created_at': datetime.now().isoformat()
        }
        
        data.append(new_item)
        save_data(data)
        
        return jsonify(new_item), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """刪除項目"""
    try:
        data = load_data()
        data = [item for item in data if item['id'] != item_id]
        save_data(data)
        
        return jsonify({'message': '項目已刪除'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """更新項目"""
    try:
        item_data = request.get_json()
        data = load_data()
        
        for item in data:
            if item['id'] == item_id:
                item['name'] = item_data.get('name', item['name'])
                item['description'] = item_data.get('description', item['description'])
                item['updated_at'] = datetime.now().isoformat()
                break
        else:
            return jsonify({'error': '項目不存在'}), 404
        
        save_data(data)
        return jsonify({'message': '項目已更新'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 確保 templates 資料夾存在
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 開發模式運行
    app.run(debug=True, host='0.0.0.0', port=5000)