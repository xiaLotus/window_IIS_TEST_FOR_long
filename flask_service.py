import sys
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
from threading import Thread
from waitress import serve
from main import app  # 匯入 Flask 應用

class FlaskService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FlaskAppService"
    _svc_display_name_ = "Flask App Service"
    _svc_description_ = "Flask 內網應用程式服務"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True

    def SvcStop(self):
        """停止服務"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STOPPED,
            (self._svc_name_, '')
        )

    def SvcDoRun(self):
        """運行服務"""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        # 在背景執行緒中啟動 Flask
        flask_thread = Thread(target=self.run_flask)
        flask_thread.daemon = True
        flask_thread.start()
        
        # 等待停止信號
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def run_flask(self):
        """運行 Flask 應用"""
        try:
            # 使用 Waitress 啟動 Flask (生產級 WSGI 服務器)
            serve(
                app, 
                host='0.0.0.0',  # 允許所有 IP 連接
                port=8080,       # 使用 8080 埠
                threads=6,       # 支援多執行緒
                cleanup_interval=30,  # 連線清理間隔
                channel_timeout=120   # 通道逾時時間
            )
        except Exception as e:
            servicemanager.LogErrorMsg(f"Flask 啟動失敗: {str(e)}")

if __name__ == '__main__':
    # 處理命令列參數
    if len(sys.argv) == 1:
        # 如果沒有參數，顯示使用說明
        print("Flask Windows 服務管理")
        print("使用方法:")
        print("  python flask_service.py install   # 安裝服務")
        print("  python flask_service.py start     # 啟動服務")
        print("  python flask_service.py stop      # 停止服務")
        print("  python flask_service.py restart   # 重啟服務")
        print("  python flask_service.py remove    # 移除服務")
        print("  python flask_service.py update    # 更新服務")
        print("  python flask_service.py debug     # 除錯模式")
        print()
        print("注意：安裝和移除服務需要系統管理員權限")
    elif len(sys.argv) == 2 and sys.argv[1] == 'update':
        # 自定義更新命令
        print("正在更新 Flask App Service...")
        try:
            # 停止服務
            print("1. 停止服務...")
            win32serviceutil.StopService(FlaskService._svc_name_)
            time.sleep(2)
            
            # 移除服務
            print("2. 移除舊服務...")
            win32serviceutil.RemoveService(FlaskService._svc_name_)
            time.sleep(1)
            
            # 重新安裝服務
            print("3. 安裝新服務...")
            win32serviceutil.InstallService(
                FlaskService._svc_reg_class_,
                FlaskService._svc_name_,
                FlaskService._svc_display_name_,
                description=FlaskService._svc_description_
            )
            
            # 啟動服務
            print("4. 啟動服務...")
            win32serviceutil.StartService(FlaskService._svc_name_)
            
            print("✅ 服務更新完成！")
            print("🌐 請瀏覽器開啟 http://localhost:8080 測試")
            
        except Exception as e:
            print(f"❌ 更新失敗: {str(e)}")
            print("請手動執行以下命令:")
            print("  python flask_service.py stop")
            print("  python flask_service.py remove") 
            print("  python flask_service.py install")
            print("  python flask_service.py start")
    else:
        win32serviceutil.HandleCommandLine(FlaskService)