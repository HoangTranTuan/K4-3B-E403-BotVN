# -*- coding: utf-8 -*-
"""
StoryboardAI - Local Web Application Server (Track C · Lesson Studio · Đề C4)
Phục vụ GUI Web & Kết nối Live AI (Dynamic SVG & Granular Edit)
Nhóm: K4-3B-E403-BotVN (Phạm Đình Hải, Trần Tuấn Hoàng, Nguyễn Văn Đại)
"""

import os
import sys

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

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from codebase.storyboard_agent import StoryboardAgent

PORT = 8501
agent = None

try:
    agent = StoryboardAgent()
except Exception as e:
    print(f"[CẢNH BÁO] Chưa khởi tạo được StoryboardAgent: {e}")

class StoryboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
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
                "features": ["Dynamic SVG", "Granular Edit", "Safe Zone Audit", "3 Edge Cases Lab"]
            }
            self.wfile.write(json.dumps(status_data, ensure_ascii=False).encode("utf-8"))
            return
        return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        if self.path == "/api/generate":
            try:
                payload = json.loads(post_data)
                script_text = payload.get("script", "").strip()

                if not script_text:
                    self.send_error_response(400, "Vui lòng nhập nội dung kịch bản bài giảng!")
                    return

                if not agent:
                    self.send_error_response(500, "StoryboardAgent chưa sẵn sàng (thiếu GEMINI_API_KEY).")
                    return

                print(f"\n[API /generate] Đang xử lý kịch bản: \"{script_text[:60]}...\"")
                start_t = time.time()
                res = agent.generate(script_text)
                val = agent.validate_storyboard(res, script_text)
                duration_ms = int((time.time() - start_t) * 1000)

                response_payload = {
                    "success": res.get("success", False),
                    "latency_ms": duration_ms,
                    "storyboard": res.get("storyboard"),
                    "validation": val,
                    "error": res.get("error")
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(response_payload, ensure_ascii=False).encode("utf-8"))
                print(f"[API /generate] Xong trong {duration_ms}ms! Frames: {len(res['storyboard']['frames']) if res.get('storyboard') else 0}")

            except Exception as e:
                self.send_error_response(500, f"Lỗi server: {str(e)}")
            return

        elif self.path == "/api/edit_frame":
            try:
                payload = json.loads(post_data)
                frame_data = payload.get("frame_data", {})
                feedback = payload.get("feedback", "").strip()
                full_script = payload.get("full_script", "")

                if not feedback:
                    self.send_error_response(400, "Vui lòng nhập nội dung góp ý cần sửa!")
                    return

                print(f"\n[API /edit_frame] Đang sửa Cảnh #{frame_data.get('frame_number')}: \"{feedback[:50]}...\"")
                start_t = time.time()
                edit_res = agent.edit_single_frame(frame_data, feedback, full_script=full_script)
                duration_ms = int((time.time() - start_t) * 1000)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(edit_res, ensure_ascii=False).encode("utf-8"))
                print(f"[API /edit_frame] Đã cập nhật xong Cảnh #{frame_data.get('frame_number')} trong {duration_ms}ms!")

            except Exception as e:
                self.send_error_response(500, f"Lỗi khi sửa cảnh: {str(e)}")
            return

        self.send_error_response(404, "Endpoint không tồn tại")

    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"success": False, "error": message}, ensure_ascii=False).encode("utf-8"))

def open_browser():
    time.sleep(1.2)
    url = f"http://localhost:{PORT}"
    print(f"\n🚀 Đang tự động mở trình duyệt: {url}")
    webbrowser.open(url)

def start_server():
    server_address = ('', PORT)
    httpd = ThreadingHTTPServer(server_address, StoryboardHandler)
    print("=" * 65)
    print("   🎬 STORYBOARD AI — DYNAMIC LIVE PROTOTYPE SERVER")
    print(f"   Địa chỉ: http://localhost:{PORT}")
    print("   Tính năng: Dynamic SVG 100% · Live Granular Edit · 3 Edge Cases Lab")
    print("   Nhóm: K4-3B-E403-BotVN (Phạm Đình Hải, Trần Tuấn Hoàng, Nguyễn Văn Đại)")
    print("=" * 65)
    print("💡 Nhấn Ctrl+C để dừng server.\n")

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Đang dừng StoryboardAI Server...")
        httpd.server_close()

if __name__ == "__main__":
    start_server()
