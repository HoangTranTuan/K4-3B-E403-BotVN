# -*- coding: utf-8 -*-
"""
StoryboardAI - Agent dựng kịch bản hình ảnh cho video bài giảng (Track C · Lesson Studio)
Nhóm: K4-3B-E403-BotVN (Phạm Đình Hải, Trần Tuấn Hoàng, Nguyễn Văn Đại)
Mục tiêu CP3: Lệnh gọi AI thật tại mắt xích quyết định trung tâm (Live LLM Call)
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
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Tải biến môi trường
load_dotenv()
if not os.environ.get('GEMINI_API_KEY'):
    alt_env = r'D:\VinAi\Chieu\day3\K4-Day03-PhamDinhHai-2A202602482\.env'
    if os.path.exists(alt_env):
        load_dotenv(alt_env)

try:
    from google import genai
    from google.genai import types
except ImportError:
    raise ImportError("Cần cài đặt thư viện 'google-genai' và 'python-dotenv'.")

DEFAULT_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-flash-lite-latest')

STYLEBOOK_SYSTEM_PROMPT = """Bạn là StoryboardAI - Chuyên gia AI phân cảnh và thiết kế kịch bản trực quan cho video bài giảng học thuật (Lesson Studio).
Nhiệm vụ của bạn là chuyển hóa văn bản kịch bản/bài giảng (Lecture Script/Audio Transcript) thành kịch bản phân cảnh hình ảnh (Visual Storyboard).

CÁC NGUYÊN TẮC BẮT BUỘC TRONG STYLEBOOK:
1. [RÀNG BUỘC KÝ TỰ] 'on_screen_text' (chữ hiển thị trên khung hình) TUYỆT ĐỐI KHÔNG QUÁ 40 KÝ TỰ (len <= 40). Chữ ngắn gọn, súc tích, tránh gây quá tải nhận thức cho học viên.
2. [VÙNG AN TOÀN - SAFE ZONE] Tọa độ hiển thị 'safe_zone': X nằm trong khoảng [80, 1840], Y nằm trong khoảng [250, 960] (để trống HUD bài giảng phía trên y < 250 và phụ đề bên dưới y > 960).
3. [NGHIÊM CẤM ẢO GIÁC - GROUNDING] Tuyệt đối KHÔNG tự sáng tác số liệu, phần trăm, ngày tháng hay dữ kiện nếu kịch bản gốc không đề cập. Nếu kịch bản chỉ nói định tính (ví dụ: 'tốc độ tăng đáng kể'), KHÔNG ĐƯỢC biến thành 'tăng 80%' hay 'tăng 3x'.
4. [CHUẨN HÓA BIỂU TƯỢNG - VISUAL SYMBOLISM]:
   - Database / Cơ sở dữ liệu: Hình trụ xếp chồng 3 tầng màu xanh dương.
   - Server / Máy chủ: Khối chữ nhật màu xanh đậm với đèn LED tín hiệu.
   - Cache / Bộ nhớ đệm: Khối chip bộ nhớ phát sáng ánh vàng.
   - Luồng dữ liệu / Truy vấn: Mũi tên neon chuyển động tuần tự.
   - Khái niệm trừu tượng (văn hóa, tư duy, thuật toán): Phải dùng ẩn dụ trực quan rõ ràng, không vẽ hình chung chung.

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC:
Trả về DUY NHẤT một JSON hợp lệ theo schema sau:
{
  "scene_title": "Tiêu đề tổng thể của phân đoạn bài giảng",
  "core_concept": "Khái niệm cốt lõi",
  "frames": [
    {
      "frame_number": 1,
      "duration_seconds": 6,
      "script_anchor": "Câu trích dẫn ngắn trong kịch bản làm điểm neo",
      "visual_description": "Mô tả chi tiết hình ảnh, đạo cụ, đồ họa hiển thị",
      "visual_symbol": "Tên biểu tượng chuẩn hóa sử dụng (Database cylinder, Server rack, etc.)",
      "on_screen_text": "Chữ tối đa 40 ký tự xuất hiện trên màn hình",
      "safe_zone": {
        "x": 960,
        "y": 540,
        "width": 800,
        "height": 400,
        "compliant": true
      },
      "camera_motion": "static | pan_right | zoom_in | cut",
      "cognitive_load": "low | medium"
    }
  ],
  "compliance_check": {
    "text_length_max": 40,
    "hallucination_detected": false,
    "domain_symbol_matched": true
  }
}
"""

class StoryboardAgent:
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Không tìm thấy GEMINI_API_KEY trong biến môi trường.")
        self.model_name = model_name or DEFAULT_MODEL
        self.client = genai.Client(api_key=self.api_key)

    def generate(self, script_text: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Lệnh gọi AI thật: Nhận kịch bản và phân tích thành Storyboard JSON
        """
        user_prompt = f"""Kịch bản bài giảng cần dựng phân cảnh trực quan:
\"\"\"
{script_text}
\"\"\""""
        if context:
            user_prompt += f"\n\nNgữ cảnh bổ sung / Yêu cầu đặc biệt:\n{context}"
        
        user_prompt += "\nHãy phân tích và trả về cấu trúc JSON phân cảnh tuân thủ tuyệt đối Stylebook."

        start_time = time.time()
        raw_response_text = ""
        parsed_json = None
        error_msg = None

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=STYLEBOOK_SYSTEM_PROMPT,
                    temperature=0.2,
                    response_mime_type="application/json"
                )
            )
            raw_response_text = response.text or ""
            latency_ms = int((time.time() - start_time) * 1000)

            clean_text = raw_response_text.strip()
            if clean_text.startswith('```json'):
                clean_text = clean_text[7:]
            if clean_text.startswith('```'):
                clean_text = clean_text[3:]
            if clean_text.endswith('```'):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()

            parsed_json = json.loads(clean_text)

        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            error_msg = str(e)

        return {
            "success": parsed_json is not None,
            "latency_ms": latency_ms,
            "model": self.model_name,
            "raw_prompt": user_prompt,
            "raw_response": raw_response_text,
            "storyboard": parsed_json,
            "error": error_msg
        }

    def validate_storyboard(self, result_data: Dict[str, Any], raw_script: str) -> Dict[str, Any]:
        """
        Hàm hậu kiểm (Deterministic Verification) đánh giá các tiêu chí kỹ thuật:
        1. Text length <= 40 chars
        2. Safe zone bounding check (X: 80-1840, Y: 250-960)
        3. Non-hallucination check (phát hiện số liệu bịa đặt không có trong raw_script)
        4. Structured valid JSON check
        """
        report = {
            "text_length_pass": True,
            "safe_zone_pass": True,
            "hallucination_pass": True,
            "symbol_pass": True,
            "max_text_len": 0,
            "violations": [],
            "overall_pass": False
        }

        if not result_data.get("success") or not result_data.get("storyboard"):
            report["overall_pass"] = False
            report["violations"].append(f"AI call failed or invalid JSON: {result_data.get('error')}")
            return report

        sb = result_data["storyboard"]
        frames = sb.get("frames", [])
        if not frames:
            report["overall_pass"] = False
            report["violations"].append("Không có frame nào được sinh ra.")
            return report

        for idx, f in enumerate(frames):
            frame_num = f.get("frame_number", idx + 1)
            on_text = f.get("on_screen_text", "")
            text_len = len(on_text)
            if text_len > report["max_text_len"]:
                report["max_text_len"] = text_len

            # 1. Check text length <= 40
            if text_len > 40:
                report["text_length_pass"] = False
                report["violations"].append(f"Frame {frame_num}: on_screen_text dài {text_len} ký tự (> 40): '{on_text}'")

            # 2. Check safe zone
            sz = f.get("safe_zone", {})
            x = sz.get("x", 960)
            y = sz.get("y", 540)
            if not (80 <= x <= 1840 and 250 <= y <= 960):
                report["safe_zone_pass"] = False
                report["violations"].append(f"Frame {frame_num}: Vị trí ({x}, {y}) nằm ngoài Safe Zone [80..1840, 250..960]")

            # 3. Check Non-hallucination: Kiểm tra các số liệu hoặc tỷ lệ % xuất hiện trong on_screen_text mà không có trong raw_script
            numbers_in_text = re.findall(r'\d+(?:\.\d+)?%?', on_text)
            for num in numbers_in_text:
                if num not in raw_script:
                    report["hallucination_pass"] = False
                    report["violations"].append(f"Frame {frame_num}: Nghi vấn hallucination số liệu '{num}' không có trong kịch bản gốc")

        report["overall_pass"] = (
            report["text_length_pass"] and
            report["safe_zone_pass"] and
            report["hallucination_pass"]
        )
        return report

if __name__ == '__main__':
    agent = StoryboardAgent()
    sample_script = """Khi người dùng gửi yêu cầu, Web Server sẽ tiếp nhận và chuyển tiếp đến Application Server. Nếu dữ liệu đã có trong Cache, hệ thống sẽ trả về ngay lập tức mà không cần truy vấn Database."""
    print("--- Dang gui kich ban mau toi StoryboardAI (Live Gemini Model) ---")
    res = agent.generate(sample_script)
    print(f"Trang thai: {'Thanh cong' if res['success'] else 'That bai'}")
    print(f"Thoi gian phan hoi: {res['latency_ms']} ms")
    if res['success']:
        print("Storyboard ket qua:")
        print(json.dumps(res['storyboard'], indent=2, ensure_ascii=False))
        v = agent.validate_storyboard(res, sample_script)
        print("\n--- Ket qua kiem thu chuan Stylebook ---")
        print(json.dumps(v, indent=2, ensure_ascii=False))
