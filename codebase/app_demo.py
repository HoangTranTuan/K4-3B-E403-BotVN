# -*- coding: utf-8 -*-
"""
StoryboardAI - Giao diện Demo trực tiếp phục vụ Video 30s (Checkpoint 3)
Chạy trực tiếp trên Terminal với định dạng trực quan hoặc mở chế độ Live Interactive.
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import json
import time
from pathlib import Path

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from codebase.storyboard_agent import StoryboardAgent

DEMO_PRESETS = [
    {
        "title": "1. Kiến trúc Web Caching (Cơ sở hạ tầng)",
        "script": "Khi người dùng gửi yêu cầu, Web Server sẽ tiếp nhận và chuyển tiếp đến Application Server. Nếu dữ liệu đã có trong Cache, hệ thống sẽ trả về ngay lập tức mà không cần truy vấn Database."
    },
    {
        "title": "2. Khái niệm Con trỏ RAM (C/C++ Pointers)",
        "script": "Con trỏ trong C++ bản chất là một biến lưu trữ địa chỉ của một ô nhớ khác trong thanh RAM máy tính."
    },
    {
        "title": "3. Hệ thống Microservices với Apache Kafka",
        "script": "Các dịch vụ thanh toán sẽ đẩy thông điệp giao dịch vào hàng đợi Apache Kafka để các worker xử lý bất đồng bộ."
    }
]

def print_banner():
    print("=" * 65)
    print("   🎬 STORYBOARD AI — LIVE PROTOTYPE (TRACK C · LESSON STUDIO)")
    print("   Nhóm: K4-3B-E403-BotVN (Phạm Đình Hải, Trần Tuấn Hoàng, Nguyễn Văn Đại)")
    print("   Model: gemini-flash-lite-latest | Checkpoint 3 (CP3)")
    print("=" * 65)

def run_demo():
    print_banner()
    agent = StoryboardAgent()

    print("\nChọn kịch bản mẫu để demo (hoặc nhấn 0 để tự nhập kịch bản):")
    for idx, p in enumerate(DEMO_PRESETS, 1):
        print(f" [{idx}] {p['title']}")
    print(" [0] Tự gõ kịch bản mới bất kỳ")

    choice = input("\n👉 Nhập lựa chọn (1/2/3/0) [Mặc định: 1]: ").strip()
    if choice == "2":
        script = DEMO_PRESETS[1]["script"]
    elif choice == "3":
        script = DEMO_PRESETS[2]["script"]
    elif choice == "0":
        script = input("\n📝 Nhập kịch bản bài giảng: ").strip()
        if not script:
            script = DEMO_PRESETS[0]["script"]
    else:
        script = DEMO_PRESETS[0]["script"]

    print("\n" + "-" * 65)
    print(f"📄 KỊCH BẢN ĐẦU VÀO:\n\"{script}\"")
    print("-" * 65)
    print("⚡ Đang gửi yêu cầu đến Gemini AI Model...")
    
    start_t = time.time()
    res = agent.generate(script)
    duration = time.time() - start_t

    if not res.get("success"):
        print(f"\n❌ LỖI: {res.get('error')}")
        return

    sb = res.get("storyboard", {})
    print(f"\n✨ KẾT QUẢ PHÂN CẢNH THÀNH CÔNG TRONG {duration:.2f} GIÂY!")
    print(f"📌 Tiêu đề phân cảnh: {sb.get('scene_title', 'Chưa có')}")
    print(f"💡 Khái niệm cốt lõi: {sb.get('core_concept', 'Chưa có')}")
    print("-" * 65)

    frames = sb.get("frames", [])
    for f in frames:
        f_num = f.get("frame_number", 1)
        dur = f.get("duration_seconds", 5)
        txt = f.get("on_screen_text", "")
        sym = f.get("visual_symbol", "")
        desc = f.get("visual_description", "")
        sz = f.get("safe_zone", {})
        pos = f"X: {sz.get('x', 960)}, Y: {sz.get('y', 540)}"

        print(f"\n🖼️  [FRAME #{f_num}] ({dur}s) — Safe Zone: {pos}")
        print(f"   ├─ 🔤 Chữ hiển thị (on_screen_text): \"{txt}\" ({len(txt)}/40 ký tự)")
        print(f"   ├─ 🏷️ Biểu tượng chuẩn (visual_symbol): {sym}")
        print(f"   └─ 🎨 Mô tả trực quan: {desc}")

    print("\n" + "=" * 65)
    # Hậu kiểm tự động
    val = agent.validate_storyboard(res, script)
    pass_icon = "✅ ĐẠT CHUẨN" if val["overall_pass"] else "⚠️ CẢNH BÁO"
    print(f"🔍 ĐÁNH GIÁ STYLEBOOK: {pass_icon}")
    print(f"   • Ràng buộc chữ on-screen (<= 40 ký tự): {'ĐẠT' if val['text_length_pass'] else 'VI PHẠM'}")
    print(f"   • Vùng hiển thị Safe Zone ([80..1840, 250..960]): {'ĐẠT' if val['safe_zone_pass'] else 'VI PHẠM'}")
    print(f"   • Kiểm tra ảo giác số liệu (Non-hallucination): {'ĐẠT' if val['hallucination_pass'] else 'VI PHẠM'}")
    if val["violations"]:
        print(f"   • Chi tiết lỗi: {'; '.join(val['violations'])}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_demo()
