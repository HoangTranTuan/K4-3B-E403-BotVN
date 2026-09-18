# -*- coding: utf-8 -*-
"""
StoryboardAI - Agent dựng kịch bản hình ảnh cho video bài giảng (Track C · Lesson Studio · Đề C4)
Nhóm: K4-3B-E403-BotVN (Phạm Đình Hải, Trần Tuấn Hoàng, Nguyễn Văn Đại)
Trách nhiệm Hải: Data & Edge Cases (Ca trừu tượng, Ca nhồi nhét, Ca chống bịa số liệu)
Nâng cấp: Senior Storyboard Art Direction Framework (Đồ họa thực tế, giàu chi tiết, 3 lớp chiều sâu)
"""

import os
import sys

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
    alt_env = r'D:\VinAi\Chieu\minihackathon\K4-3B-E403-BotVN\.env'
    if os.path.exists(alt_env):
        load_dotenv(alt_env)

try:
    from google import genai
    from google.genai import types
except ImportError:
    raise ImportError("Cần cài đặt thư viện 'google-genai' và 'python-dotenv'.")

DEFAULT_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-flash-lite-latest')

STYLEBOOK_SYSTEM_PROMPT = """Bạn là Chuyên gia Đồ họa Storyboard điện ảnh & video bài giảng cao cấp (Senior Storyboard Artist & Art Director tại Lesson Studio).
Nhiệm vụ của bạn là chuyển hóa kịch bản bài giảng thành kịch bản phân cảnh hình ảnh (Visual Storyboard) CHÂN THỰC, SỐNG ĐỘNG, ĐẬM CHẤT ĐIỆN ẢNH VÀ SƯ PHẠM.

TUYỆT ĐỐI NGHIÊM CẤM (ANTI-PATTERNS):
- NGHIÊM CẤM vẽ các khối hình học trừu tượng lười biếng như hình tam giác, hình tròn, hình chữ nhật thô sơ xếp lại như đồ chơi trẻ em!
- NGHIÊM CẤM chèn chữ ghi chú tiếng Việt vào bên trong thuộc tính d="..." hoặc points="..." của thẻ SVG vì sẽ làm hỏng cú pháp XML!

QUY CHUẨN MỸ THUẬT STORYBOARD THỰC TẾ (SENIOR ART DIRECTION):
Mỗi khung hình bắt buộc phải có mã SVG tỉ lệ 16:9 (viewBox="0 0 320 180") có CHIỀU SÂU 3 LỚP (Layered Depth Composition):
1. [LỚP 1 - BACKGROUND]:
   - Bầu trời, kiến trúc bối cảnh xa, ánh sáng chuyển sắc bằng <defs><linearGradient> hoặc <radialGradient>.
2. [LỚP 2 - MIDGROUND (CHỦ THỂ CHÍNH - FOCAL SUBJECT)]:
   - Phải vẽ đối tượng thực tế bằng các đường cong <path d="..."> tinh xảo, có bóng đổ và độ tương phản cao:
     * Nếu là lịch sử (như Ba Đình 1945): Vẽ lễ đài bằng gỗ, bục phát biểu, micro cổ điển thập niên 40, cuộn văn kiện mở ra phát sáng ánh vàng kim, lá cờ đỏ sao vàng uốn lượn kiêu hãnh.
     * Nếu là hệ thống mạng / công nghệ: Vẽ cụm máy chủ rack với đèn LED, chip xử lý kim loại, các luồng dữ liệu neon chuyển động tuần tự.
     * Nếu là khoa học / thiên văn: Vẽ hành tinh, hố đen với đĩa bồi tụ xoắn ốc phát sáng, tấm lưới không-thời gian cong võng.
     * Nếu là kinh tế / xã hội: Vẽ mô hình thị trường, đồ thị tăng trưởng có phối cảnh, biểu tượng nhà máy hoặc sàn giao dịch.
3. [LỚP 3 - FOREGROUND]:
   - Chi tiết bóng đổ tiền cảnh (silhouette con người, đám đông quần chúng, bàn tay chỉ dẫn, khung viền đạo diễn...).
4. [RÀNG BUỘC KỸ THUẬT BẮT BUỘC]:
   - 'on_screen_text' TUYỆT ĐỐI KHÔNG QUÁ 40 KÝ TỰ (len <= 40). Chữ cô đọng, súc tích.
   - Vùng hiển thị chính phải nằm trong Safe Zone (tọa độ tương đối trong khung 320x180: x từ 20 đến 300, y từ 30 đến 160).
   - Tuyệt đối không tự ý bịa số liệu % hoặc thống kê nếu kịch bản chỉ nói định tính.

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC:
Trả về DUY NHẤT một JSON hợp lệ theo schema sau:
{
  "scene_title": "Tiêu đề tổng quan phân cảnh",
  "core_concept": "Ý niệm sư phạm cốt lõi",
  "frames": [
    {
      "frame_number": 1,
      "duration_seconds": 6,
      "timeline": "00:00.000 - 00:06.000",
      "script_anchor": "Câu trích dẫn trong bài giảng",
      "trigger_word": "Từ then chốt kích hoạt hình ảnh",
      "visual_description": "Mô tả chi tiết phối cảnh, ánh sáng, chuyển động điện ảnh",
      "visual_symbol": "Tên chủ thể chính",
      "on_screen_text": "Chữ cô đọng tối đa 40 ký tự",
      "svg_code": "<svg xmlns=\\"http://www.w3.org/2000/svg\\" viewBox=\\"0 0 320 180\\" class=\\"w-full h-full bg-slate-950\\">...</svg>",
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
        user_prompt = f"""Kịch bản bài giảng cần thiết kế phân cảnh hình ảnh thực tế:
\"\"\"
{script_text}
\"\"\""""
        if context:
            user_prompt += f"\n\nYêu cầu nghệ thuật / Ngữ cảnh:\n{context}"
        
        user_prompt += "\nHãy phân tích và lập trình mã SVG chân thực, có chiều sâu 3 lớp (Background, Midground chủ thể, Foreground silhouette) cho từng cảnh theo đúng Senior Storyboard Art Direction."

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
                    temperature=0.3,
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

            # Kiểm tra làm sạch SVG code nếu có comment lỗi cú pháp
            if parsed_json and "frames" in parsed_json:
                for f in parsed_json["frames"]:
                    if "svg_code" in f:
                        f["svg_code"] = self._clean_svg(f["svg_code"])

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
        prompt = f"""Bạn là Senior Storyboard Artist. Người dùng yêu cầu chỉnh sửa DUY NHẤT một cảnh phân cảnh.

THÔNG TIN CẢNH #{frame_data.get('frame_number', 1)}:
- Lời đọc: "{frame_data.get('script_anchor', '')}"
- Chữ màn hình cũ: "{frame_data.get('on_screen_text', '')}"
- Ý trực quan cũ: "{frame_data.get('visual_description', '')}"

GÓP Ý CỦA NGƯỜI DUYỆT:
\"\"\"
{feedback}
\"\"\"

YÊU CẦU NGHỆ THUẬT:
1. Vẽ lại mã SVG (viewBox="0 0 320 180") chân thực, sắc nét, có chiều sâu 3 lớp theo đúng góp ý.
2. TUYỆT ĐỐI KHÔNG vẽ các khối tam giác/hình tròn thô sơ!
3. 'on_screen_text' tối đa 40 ký tự (len <= 40).
4. Trả về DUY NHẤT JSON hợp lệ:
{{
  "frame_number": {frame_data.get('frame_number', 1)},
  "duration_seconds": {frame_data.get('duration_seconds', 6)},
  "timeline": "{frame_data.get('timeline', '00:00.000 - 00:06.000')}",
  "script_anchor": "{frame_data.get('script_anchor', '')}",
  "trigger_word": "{frame_data.get('trigger_word', 'Key')}",
  "visual_description": "Mô tả chi tiết hình ảnh mới sinh động",
  "visual_symbol": "Tên chủ thể mới",
  "on_screen_text": "Chữ màn hình mới <= 40 ký tự",
  "svg_code": "<svg xmlns=\\"http://www.w3.org/2000/svg\\" viewBox=\\"0 0 320 180\\" class=\\"w-full h-full bg-slate-950\\">...</svg>",
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
                    temperature=0.3,
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
            if "svg_code" in parsed:
                parsed["svg_code"] = self._clean_svg(parsed["svg_code"])
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

    def _clean_svg(self, svg_str: str) -> str:
        """Làm sạch các comment lạc vào bên trong path d="..." hoặc cú pháp lỗi"""
        # Loại bỏ các chuỗi text trong ngoặc đơn nằm trong thuộc tính d="..."
        cleaned = re.sub(r'(\bd\s*=\s*"[^"]*?)\([^)]*?\)([^"]*?")', r'\1\2', svg_str)
        return cleaned

    def validate_storyboard(self, result_data: Dict[str, Any], raw_script: str) -> Dict[str, Any]:
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

            if text_len > 40:
                report["text_length_pass"] = False
                report["violations"].append(f"Cảnh {frame_num}: on_screen_text dài {text_len} ký tự (> 40): '{on_text}'")

            sz = f.get("safe_zone", {})
            x = sz.get("x", 960)
            y = sz.get("y", 540)
            if not (80 <= x <= 1840 and 250 <= y <= 960):
                report["safe_zone_pass"] = False
                report["violations"].append(f"Cảnh {frame_num}: Tọa độ ({x}, {y}) vi phạm Safe Zone [80..1840, 250..960]")

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
    sample = "Năm 1945, bản Tuyên ngôn Độc lập được tuyên đọc tại Quảng trường Ba Đình."
    print("--- Test Senior Storyboard Art Direction (Ba Đình 1945) ---")
    res = agent.generate(sample)
    if res['success']:
        print("Tiêu đề:", res['storyboard'].get('scene_title'))
        frames = res['storyboard'].get('frames', [])
        for f in frames:
            print(f"Cảnh #{f.get('frame_number')}: Text='{f.get('on_screen_text')}' ({len(f.get('on_screen_text',''))} chars)")
            print(f"SVG Code Length: {len(f.get('svg_code',''))} chars")
    else:
        print("Lỗi:", res.get('error'))
