# -*- coding: utf-8 -*-
"""
StoryboardAI - Agent dựng kịch bản hình ảnh cho video bài giảng (Track C · Lesson Studio · Đề C4)
Nhóm: K4-3B-E403-BotVN (Phạm Đình Hải, Trần Tuấn Hoàng, Nguyễn Văn Đại)
Trách nhiệm Hải: Data & Edge Cases (Ca trừu tượng, Ca nhồi nhét, Ca chống bịa số liệu)
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

STYLEBOOK_SYSTEM_PROMPT = """Bạn là StoryboardAI - Chuyên gia AI phân cảnh và thiết kế kịch bản trực quan cho video bài giảng học thuật (Lesson Studio - Đề C4).
Nhiệm vụ của bạn là chuyển hóa kịch bản bài giảng thành kịch bản phân cảnh hình ảnh (Visual Storyboard) TÙY BIẾN ĐỘNG 100% theo nội dung bài học.

QUY TẮC BẮT BUỘC TRONG STYLEBOOK:
1. [RÀNG BUỘC KÝ TỰ] 'on_screen_text' (chữ xuất hiện trên khung hình) TUYỆT ĐỐI KHÔNG QUÁ 40 KÝ TỰ (len <= 40). Chữ phải ngắn gọn, súc tích, tránh gây quá tải nhận thức cho học viên.
2. [VÙNG AN TOÀN - SAFE ZONE] Tọa độ 'safe_zone': X nằm trong khoảng [80, 1840], Y nằm trong khoảng [250, 960] (chừa dải trên HUD y < 250 và dải dưới phụ đề y > 960).
3. [NGHIÊM CẤM ẢO GIÁC - GROUNDING (Ca khó 13 của Hải)]: Tuyệt đối KHÔNG tự sáng tác số liệu, tỷ lệ % nếu kịch bản gốc chỉ có tính định tính.
4. [KHÁI NIỆM TRỪU TƯỢNG (Ca khó 29 của Hải)]: Phải quy đổi thành ẩn dụ trực quan (Visual Metaphor) rõ ràng.
5. [CÂU NHỒI NHÉT Ý (Ca khó 31 của Hải)]: Phải tự động chia nhỏ thành các cảnh tuần tự.
6. [TẠO ĐỒ HỌA SVG ĐỘNG 100%]: Đối với mỗi cảnh, bạn PHẢI TỰ VẼ một đoạn mã SVG hợp lệ (viewBox="0 0 320 180") mô tả trực quan chính xác nội dung câu đó:
   - Dùng các thẻ: <rect>, <circle>, <path>, <polygon>, <line>, <text>.
   - Bảng màu: Nền đen (#020617 / #0b0f19), Xanh dương (#3b82f6 / #1e3a8a), Vàng cam (#f59e0b), Xanh lá (#10b981), Tím/Đỏ (#a855f7 / #ef4444).
   - Tuyệt đối không để trống mã SVG.

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC:
Trả về DUY NHẤT một JSON hợp lệ theo schema sau (không thêm văn bản ngoài):
{
  "scene_title": "Tiêu đề tổng quan của bài giảng",
  "core_concept": "Ý niệm sư phạm cốt lõi",
  "frames": [
    {
      "frame_number": 1,
      "duration_seconds": 6,
      "timeline": "00:00.000 - 00:06.000",
      "script_anchor": "Trích dẫn câu lời đọc ứng với cảnh",
      "trigger_word": "Từ then chốt kích hoạt hình ảnh xuất hiện",
      "visual_description": "Mô tả chi tiết ý sư phạm cần thấy",
      "visual_symbol": "Tên biểu tượng chính",
      "on_screen_text": "Chữ tối đa 40 ký tự xuất hiện trên màn hình",
      "svg_code": "<svg viewBox=\\"0 0 320 180\\" class=\\"w-full h-full bg-slate-950\\">...</svg>",
      "safe_zone": { "x": 960, "y": 540, "width": 800, "height": 400, "compliant": true }
    }
  ],
  "compliance_summary": {
    "all_text_under_40": true,
    "safe_zone_compliant": true,
    "no_hallucination": true
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
        Lệnh gọi AI thật: Chuyển hóa kịch bản bài giảng thành Storyboard động 100%
        """
        user_prompt = f"""Kịch bản bài giảng cần dựng phân cảnh trực quan:
\"\"\"
{script_text}
\"\"\""""
        if context:
            user_prompt += f"\n\nNgữ cảnh / Yêu cầu đặc biệt:\n{context}"
        
        user_prompt += "\nHãy phân tích, chia tách từng cảnh sư phạm, tạo mã SVG đồ họa minh họa độc bản cho từng cảnh và trả về cấu trúc JSON đúng chuẩn Stylebook."

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

    def edit_single_frame(self, frame_data: Dict[str, Any], feedback: str, full_script: str = "") -> Dict[str, Any]:
        """
        Lát cắt cam kết Canvas CP1: Sửa một câu thì CHỈ ĐÚNG ảnh phác thảo của câu đó được cập nhật bằng AI
        """
        prompt = f"""Bạn là StoryboardAI. Người dùng muốn chỉnh sửa DUY NHẤT một cảnh trong kịch bản bài giảng.

THÔNG TIN CẢNH HIỆN TẠI (CẢNH #{frame_data.get('frame_number', 1)}):
- Lời đọc: "{frame_data.get('script_anchor', '')}"
- Chữ màn hình cũ: "{frame_data.get('on_screen_text', '')}"
- Ý trực quan cũ: "{frame_data.get('visual_description', '')}"

YÊU CẦU GÓP Ý CỦA NGƯỜI DUYỆT:
\"\"\"
{feedback}
\"\"\"

YÊU CẦU:
1. Giữ nguyên ngữ cảnh bài giảng, chỉ tái thiết kế và vẽ lại DUY NHẤT cảnh này.
2. Ràng buộc: 'on_screen_text' tối đa 40 ký tự (len <= 40).
3. Sinh lại mã 'svg_code' động (viewBox="0 0 320 180") thể hiện đúng góp ý của người duyệt.
4. Trả về DUY NHẤT JSON của frame này theo cấu trúc:
{{
  "frame_number": {frame_data.get('frame_number', 1)},
  "duration_seconds": {frame_data.get('duration_seconds', 6)},
  "timeline": "{frame_data.get('timeline', '00:00.000 - 00:06.000')}",
  "script_anchor": "{frame_data.get('script_anchor', '')}",
  "trigger_word": "{frame_data.get('trigger_word', 'Key')}",
  "visual_description": "Mô tả mới đã chỉnh sửa theo góp ý",
  "visual_symbol": "Tên biểu tượng mới",
  "on_screen_text": "Chữ màn hình mới <= 40 ký tự",
  "svg_code": "<svg viewBox=\\"0 0 320 180\\" class=\\"w-full h-full bg-slate-950\\">...</svg>",
  "safe_zone": {{ "x": 960, "y": 540, "width": 800, "height": 400, "compliant": true }}
}}
"""
        start_time = time.time()
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=STYLEBOOK_SYSTEM_PROMPT,
                    temperature=0.2,
                    response_mime_type="application/json"
                )
            )
            raw_text = response.text or ""
            clean_text = raw_text.strip()
            if clean_text.startswith('```json'):
                clean_text = clean_text[7:]
            if clean_text.startswith('```'):
                clean_text = clean_text[3:]
            if clean_text.endswith('```'):
                clean_text = clean_text[:-3]
            parsed = json.loads(clean_text.strip())
            return {
                "success": True,
                "latency_ms": int((time.time() - start_time) * 1000),
                "updated_frame": parsed
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "latency_ms": int((time.time() - start_time) * 1000)
            }

    def validate_storyboard(self, result_data: Dict[str, Any], raw_script: str) -> Dict[str, Any]:
        """
        Hậu kiểm tự động (Deterministic Verification)
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
            report["violations"].append(f"AI call failed: {result_data.get('error')}")
            return report

        sb = result_data["storyboard"]
        frames = sb.get("frames", [])
        if not frames:
            report["overall_pass"] = False
            report["violations"].append("Không có frame nào được tạo ra.")
            return report

        for idx, f in enumerate(frames):
            frame_num = f.get("frame_number", idx + 1)
            on_text = f.get("on_screen_text", "")
            text_len = len(on_text)
            if text_len > report["max_text_len"]:
                report["max_text_len"] = text_len

            # 1. Text <= 40
            if text_len > 40:
                report["text_length_pass"] = False
                report["violations"].append(f"Cảnh {frame_num}: on_screen_text dài {text_len} ký tự (> 40): '{on_text}'")

            # 2. Safe zone
            sz = f.get("safe_zone", {})
            x = sz.get("x", 960)
            y = sz.get("y", 540)
            if not (80 <= x <= 1840 and 250 <= y <= 960):
                report["safe_zone_pass"] = False
                report["violations"].append(f"Cảnh {frame_num}: Tọa độ ({x}, {y}) vi phạm Safe Zone [80..1840, 250..960]")

            # 3. Non-hallucination check
            numbers_in_text = re.findall(r'\d+(?:\.\d+)?%?', on_text)
            for num in numbers_in_text:
                if num not in raw_script:
                    report["hallucination_pass"] = False
                    report["violations"].append(f"Cảnh {frame_num}: Nghi vấn bịa số liệu '{num}' không có trong kịch bản gốc")

        report["overall_pass"] = (
            report["text_length_pass"] and
            report["safe_zone_pass"] and
            report["hallucination_pass"]
        )
        return report

if __name__ == '__main__':
    agent = StoryboardAgent()
    sample = "Hai lỗ đen sáp nhập trong không-thời gian tạo ra sóng hấp dẫn lan truyền khắp vũ trụ."
    print("--- Test Live Dynamic SVG Generation ---")
    res = agent.generate(sample)
    if res['success']:
        print("Tiêu đề:", res['storyboard'].get('scene_title'))
        frames = res['storyboard'].get('frames', [])
        for f in frames:
            print(f"Cảnh #{f.get('frame_number')}: Text='{f.get('on_screen_text')}' ({len(f.get('on_screen_text',''))} chars)")
            print(f"SVG Preview: {f.get('svg_code')[:80]}...")
    else:
        print("Lỗi:", res.get('error'))
