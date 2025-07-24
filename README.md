# Flask Windows 服務解決方案

## 🎯 專案目標

解決 IIS 應用程式池回收導致的 Flask 後台斷線問題，提供穩定的後端 API 服務。

## 📋 解決方案架構

```
前端 (IIS 站台) → 後台 API (Flask Windows 服務 - 埠 8080)
     ↑                           ↑
  保持原有網站架構              穩定不斷線的服務
```

## 🌟 專案特色

- ✅ **解決斷線問題**：Flask 後台獨立運行，不受 IIS 應用程式池影響
- ✅ **保持現有架構**：前端 IIS 站台不需要大幅修改
- ✅ **穩定運行**：使用 Windows 服務，支援自動重啟
- ✅ **完整 CRUD**：包含新增、查詢、更新、刪除功能
- ✅ **生產就緒**：使用 Waitress WSGI 服務器
- ✅ **跨域支援**：解決前後端分離的 CORS 問題

## 📁 檔案結構

```
flask-backend-service/
├── README.md           # 專案說明文件
├── requirements.txt    # Python 套件清單
├── main.py            # Flask 後端 API 服務
├── flask_service.py   # Windows 服務管理腳本
├── templates/
│   └── index.html     # 前端測試頁面 (可選)
└── data.json          # 資料檔案 (自動建立)
```

## 🚀 快速安裝

### 1. 環境準備
- Python 3.7+
- pip 套件管理工具

### 2. 安裝套件
```cmd
pip install -r requirements.txt
```

### 3. 測試開發環境
```cmd
python main.py
```
瀏覽器開啟 `http://localhost:5000` 測試 API

### 4. 部署為 Windows 服務
**以系統管理員身分執行：**
```cmd
python flask_service.py install
python flask_service.py start
```

### 5. 驗證服務
瀏覽器開啟 `http://localhost:8080/health` 檢查服務狀態

## 🔧 服務管理命令

```cmd
python flask_service.py install    # 安裝服務
python flask_service.py start      # 啟動服務
python flask_service.py stop       # 停止服務
python flask_service.py restart    # 重啟服務
python flask_service.py update     # 更新服務 (停止→移除→安裝→啟動)
python flask_service.py remove     # 移除服務
python flask_service.py debug      # 除錯模式 (不作為服務運行)
```

## 🌐 API 端點說明

### 基礎 URL
```
http://localhost:8080
```

### 端點列表

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/health` | 健康檢查 |
| GET | `/api/items` | 取得所有項目 |
| POST | `/api/items` | 新增項目 |
| PUT | `/api/items/<id>` | 更新項目 |
| DELETE | `/api/items/<id>` | 刪除項目 |
| GET | `/` | 前端測試頁面 |

### API 使用範例

**取得所有項目：**
```javascript
fetch('http://localhost:8080/api/items')
  .then(response => response.json())
  .then(data => console.log(data));
```

**新增項目：**
```javascript
fetch('http://localhost:8080/api/items', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: '項目名稱',
    description: '項目描述'
  })
});
```

**更新項目：**
```javascript
fetch('http://localhost:8080/api/items/1', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: '更新的名稱',
    description: '更新的描述'
  })
});
```

**刪除項目：**
```javascript
fetch('http://localhost:8080/api/items/1', {
  method: 'DELETE'
});
```

## 🔗 前端整合方式

### 修改現有 IIS 站台

在你的前端 JavaScript 中，將 API 呼叫指向 Flask 服務：

```javascript
// 設定 API 基礎路徑
const API_BASE = 'http://localhost:8080';

// 使用範例
async function loadData() {
    try {
        const response = await fetch(`${API_BASE}/api/items`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API 呼叫失敗:', error);
    }
}

// 新增資料
async function addItem(itemData) {
    try {
        const response = await fetch(`${API_BASE}/api/items`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(itemData)
        });
        return await response.json();
    } catch (error) {
        console.error('新增失敗:', error);
    }
}
```

## 🔒 內網存取設定

### 開放防火牆埠號
```cmd
netsh advfirewall firewall add rule name="Flask API Service" dir=in action=allow protocol=TCP localport=8080
```

### 內網存取
其他電腦可透過以下方式存取：
```
http://你的伺服器IP:8080/api/items
```

查詢伺服器 IP：
```cmd
ipconfig
```

## ⚙️ 自動啟動設定

1. 開啟服務管理員：`Win + R` → 輸入 `services.msc`
2. 找到 **"Flask App Service"**
3. 右鍵 → **內容**
4. **啟動類型** → 選擇 **「自動」**
5. 點擊 **套用**

設定後，系統重開機會自動啟動服務。

## 🛠️ 故障排除

### 服務無法啟動

1. **檢查 Windows 事件檢視器**：
   - `Win + R` → `eventvwr.msc`
   - Windows 日誌 → 應用程式
   - 搜尋 "Flask App Service"

2. **檢查埠號是否被佔用**：
   ```cmd
   netstat -ano | findstr :8080
   ```

3. **確認套件安裝**：
   ```cmd
   pip list | findstr -i "flask waitress pywin32"
   ```

### API 呼叫失敗

1. **檢查服務狀態**：
   ```cmd
   python flask_service.py
   ```

2. **測試 API 連通性**：
   ```cmd
   curl http://localhost:8080/health
   ```

3. **檢查 CORS 設定**：
   如果前端和後端在不同網域，確認已啟用 CORS

### 前端無法連接後端

1. **確認 API 基礎路徑正確**
2. **檢查瀏覽器開發者工具的網路面板**
3. **確認防火牆設定**

## 🔧 進階設定

### 修改服務埠號
在 `flask_service.py` 中修改：
```python
serve(app, host='0.0.0.0', port=8080)  # 改成其他埠號
```

### 調整效能參數
```python
serve(
    app, 
    host='0.0.0.0', 
    port=8080, 
    threads=8,              # 執行緒數量
    cleanup_interval=30,    # 連線清理間隔 (秒)
    channel_timeout=120     # 通道逾時時間 (秒)
)
```

### 啟用日誌記錄
在 `main.py` 中加入：
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## 📊 資料儲存

- 使用 **JSON 檔案** (`data.json`) 作為簡易資料庫
- 適合中小型內網應用
- 支援 UTF-8 編碼，可處理中文資料
- 建議定期備份 `data.json` 檔案

### 資料格式範例
```json
[
  {
    "id": 1,
    "name": "範例項目",
    "description": "這是一個範例描述",
    "created_at": "2025-07-24T10:30:00.123456",
    "updated_at": "2025-07-24T11:15:00.654321"
  }
]
```

## 🔄 更新流程

### 程式碼更新 (main.py, templates)
```cmd
python flask_service.py restart
```

### 服務配置更新 (flask_service.py)
```cmd
python flask_service.py update
```

### 套件更新
```cmd
pip install -r requirements.txt --upgrade
python flask_service.py restart
```

## 📝 系統需求

- **作業系統**：Windows 10/11 或 Windows Server 2016+
- **Python**：3.7 或更高版本
- **記憶體**：建議 1GB 以上可用記憶體
- **儲存空間**：100MB+
- **網路**：內網環境，需開放 8080 埠

## 🆘 技術支援

### 常見問題檢查清單

- [ ] Python 版本：`python --version`
- [ ] 套件安裝：`pip list`
- [ ] 服務狀態：檢查 Windows 服務管理員
- [ ] 埠號檢查：`netstat -ano | findstr :8080`
- [ ] 防火牆設定：確認 8080 埠已開放
- [ ] 事件日誌：檢查 Windows 事件檢視器

### 效能優化建議

1. **增加執行緒數量**：適用於高併發情況
2. **定期清理資料**：避免 JSON 檔案過大
3. **設定資料備份**：定期備份重要資料
4. **監控系統資源**：確保記憶體和 CPU 使用正常

## 📄 授權與免責聲明

本專案僅供學習和內部使用。請遵守相關法律法規，作者不承擔任何使用風險。

---

**專案版本**：v1.0  
**更新日期**：2025年7月24日  
**適用環境**：Windows 內網環境  
**技術棧**：Flask + Waitress + PyWin32 + Windows Service