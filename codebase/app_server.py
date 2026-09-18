# -*- coding: utf-8 -*-
"""
StoryboardAI - Local Web Application Server
Phục vụ Giao diện Người Dùng Trực Quan (GUI) & Tích hợp Live Gemini AI API
Tác giả: Nhóm K4-3B-E403-BotVN (Phạm Đình Hải, Trần Tuấn Hoàng, Nguyễn Văn Đại)
"""

import os
import sys

# Đảm bảo UTF-8 cho stdout trên Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import json
import time
import webbrowser
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# Thêm đường dẫn project
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from codebase.storyboard_agent import StoryboardAgent

PORT = 8501
agent = None

try:
    agent = StoryboardAgent()
except Exception as e:
    print(f"[CẢNH BÁO] Không thể khởi tạo StoryboardAgent: {e}")

class StoryboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Đặt thư mục phục vụ file tĩnh là codebase/
        super().__init__(*args, directory=str(current_dir), **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.path = "/index.html"
            return super().do_GET()
        elif self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            status_data = {
                "status": "ready" if agent else "error",
                "model": agent.model_name if agent else "none",
                "project": "StoryboardAI - Lesson Studio (Track C)",
                "team": "K4-3B-E403-BotVN (Hai - Hoang - Dai)"
            }
            self.wfile.write(json.dumps(status_data, ensure_ascii=False).encode("utf-8"))
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/generate":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                payload = json.loads(post_data)
                script_text = payload.get("script", "").strip()
                context = payload.get("context", "")

                if not script_text:
                    self.send_error_response(400, "Vui lòng nhập kịch bản bài giảng!")
                    return

                if not agent:
                    self.send_error_response(500, "StoryboardAgent chưa được nạp khóa API hợp lệ!")
                    return

                print(f"\n[API] Đang xử lý Live AI Generate cho kịch bản: \"{script_text[:60]}...\"")
                start_t = time.time()
                result = agent.generate(script_text, context=context)
                val = agent.validate_storyboard(result, script_text)
                duration_ms = int((time.time() - start_t) * 1000)

                response_payload = {
                    "success": result.get("success", False),
                    "latency_ms": duration_ms,
                    "storyboard": result.get("storyboard"),
                    "validation": val,
                    "error": result.get("error")
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(response_payload, ensure_ascii=False).encode("utf-8"))
                print(f"[API] Hoàn tất trong {duration_ms}ms! Overall Pass: {val.get('overall_pass')}")

            except Exception as e:
                self.send_error_response(500, f"Lỗi nội bộ server: {str(e)}")
            return

        self.send_error_response(404, "Endpoint không tồn tại")

    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        err = {"success": False, "error": message}
        self.wfile.write(json.dumps(err, ensure_ascii=False).encode("utf-8"))

def open_browser():
    time.sleep(1.2)
    url = f"http://localhost:{PORT}"
    print(f"\n🚀 Đang tự động mở trình duyệt: {url}")
    webbrowser.open(url)

def start_server():
    server_address = ('', PORT)
    httpd = ThreadingHTTPServer(server_address, StoryboardHandler)
    print("=" * 65)
    print("   🎬 STORYBOARD AI — LIVE GRAPHICAL USER INTERFACE (GUI)")
    print(f"   Địa chỉ truy cập: http://localhost:{PORT}")
    print("   Mô hình AI: Google Gemini (gemini-flash-lite-latest)")
    print("   Nhóm: K4-3B-E403-BotVN (Phạm Đình Hải, Trần Tuấn Hoàng, Nguyễn Văn Đại)")
    print("=" * 65)
    print("💡 Nhấn Ctrl+C trên cửa sổ này nếu muốn dừng máy chủ.\n")

    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Đang dừng StoryboardAI Server...")
        httpd.server_close()

if __name__ == "__main__":
    start_server()
