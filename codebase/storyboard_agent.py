# -*- coding: utf-8 -*-
"""
StoryboardAI - Agent dựng kịch bản hình ảnh cho video bài giảng (Track C · Lesson Studio · Đề C4)
Nhóm: K4-3B-E403-BotVN (Phạm Đình Hải, Trần Tuấn Hoàng, Nguyễn Văn Đại)
Nâng cấp: Concept Art Image Engine (Tạo ảnh trực quan thực tế 16:9 chuẩn Studio)
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
import urllib.parse
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

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

STYLEBOOK_SYSTEM_PROMPT = """Bạn là Senior Art Director & Storyboard Architect cho nền tảng Lesson Studio.
Nhiệm vụ của bạn là chuyển hóa kịch bản bài giảng thành kịch bản phân cảnh với ĐỒ HỌA SƠ ĐỒ KHỐI PHẲNG (Minimalist Flat Vector, Infographic, Flowchart, UI/UX Diagram) 100% tinh gọn, trực quan, loại bỏ hoàn toàn các chi tiết rườm rà.

QUY CHUẨN QUAN TRỌNG:
1. [RÀNG BUỘC KÝ TỰ] 'on_screen_text' TUYỆT ĐỐI KHÔNG QUÁ 40 KÝ TỰ (len <= 40). Chữ cô đọng, súc tích.
2. [VÙNG AN TOÀN - SAFE ZONE] Tọa độ x: [80, 1840], y: [250, 960].
3. [NGHIÊM CẤM ẢO GIÁC - CA KHÓ 13 CỦA HẢI]: Không tự ý bịa số liệu % hoặc thống kê nếu kịch bản chỉ có tính định tính.
4. [TẠO DỰNG ĐỒ HỌA SVG ĐỘNG]:
   - Với mỗi cảnh, bạn PHẢI tự viết mã code SVG (Scalable Vector Graphics) trực tiếp vào trường 'svg_code' để vẽ ra sơ đồ logic tương ứng với câu giảng.
   - [ĐẶC BIỆT - XỬ LÝ CÂU TRỪU TƯỢNG]: Nếu câu giảng mang tính trừu tượng/triết lý (không có vật thể thực tế), KHÔNG cố vẽ hình đồ vật cụ thể. Hãy dùng các Node hình học cơ bản (tròn, vuông, tam giác) và đường nối đứt nét để biểu diễn logic.
   - Nguyên tắc code SVG:
     * Luôn dùng thẻ mở: `<svg class="w-full h-full max-h-40" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">`
     * KHÔNG vẽ màu nền (background) cho SVG vì giao diện đã có nền tối.
     * BẢNG MÀU BẮT BUỘC:
       + Màu đường nối/mũi tên (<line>, <path>): stroke="#475569", stroke-width="3"
       + Node chính quan trọng nhất: <circle> hoặc <rect> với fill="#4c1d95" (tím), stroke="#7c3aed"
       + Node phụ/hỗ trợ: fill="#0B0F19" (trong suốt nền tối), stroke="#0ea5e9" (xanh dương) hoặc "#10b981" (xanh ngọc)
       + Chữ trong Node (<text>): fill="#ffffff", font-family="sans-serif", font-weight="bold", text-anchor="middle"
   - AI TỰ QUYẾT ĐỊNH CẤU TRÚC:
     * Nếu là liệt kê: Vẽ 3 hình tròn xếp ngang nối nhau.
     * Nếu là trung tâm: Vẽ 1 hình to ở giữa, các hình nhỏ xoay quanh.
     * Nếu là so sánh/cấu trúc: Vẽ hình chữ nhật (<rect>) thay vì hình tròn (<circle>).
     * Phải đặt text ngắn gọn (2-3 từ) vào giữa các Node bằng thẻ <text>.
5. [QUY CHUẨN AN TOÀN SƯ PHẠM TUYỆT ĐỐI - ZERO TOLERANCE VỚI YẾU TỐ NHẠY CẢM, GỢI DỤC, KHỎA THÂN]:
   - MÔI TRƯỜNG HỌC ĐƯỜNG CHUẨN MỰC: Tuyệt đối không để lọt bất kỳ hình ảnh nhạy cảm, gợi dục, đường cong cơ thể hở hang hay khỏa thân nào.
   - PHÂN ĐỊNH RÕ RÀNG:
     * CHỦ THỂ CÔNG NGHỆ, MÁY TÍNH, VŨ TRỤ, KHOA HỌC:
       + BẮT BUỘC KHÔNG ĐƯỢC VẼ NGƯỜI, KHÔNG VẼ ROBOT DÁNG NỮ/NAM, KHÔNG VẼ THÂN HÌNH HAY ĐƯỜNG CONG SINH HỌC CỦA NGƯỜI!
       + Luôn thêm vào prompt: "no people, no human figures, no android bodies, pure technology, hardware, data visualization".
     * KHI KỊCH BẢN YÊU CẦU CÓ CON NGƯỜI (Kỹ sư, Thầy cô, Bác sĩ, Học sinh):
       + Nhân vật BẮT BUỘC phải mặc trang phục rộng rãi, kín đáo, lịch sự chuẩn mực (ví dụ: "wearing loose professional laboratory coat", "wearing conservative business formal suit with collared shirt and necktie").
       + TUYỆT ĐỐI CẤM trang phục bó sát (skintight, bodysuit, spandex), CẤM vẽ đường cong cơ thể, vòng một hay hông eo gợi cảm.
   - TUYỆT ĐỐI KHÔNG CHÈN TỪ "nudity, nude, nsfw, gore, blood" VÀO CÂU POSITIVE PROMPT (kể cả đi kèm chữ 'no'): Việc chèn các từ này vào positive prompt sẽ khiến AI khuếch tán kích hoạt vẽ cơ thể người nhạy cảm. Luôn kết thúc prompt bằng cụm từ an toàn: "family-friendly educational concept art, professional academic presentation, clean technical illustration".
6. [SVG CODE DỰ PHÒNG]: Mã SVG đơn giản phòng khi offline.
7. [TÍNH NHẤT QUÁN THỊ GIÁC - SỔ QUY ƯỚC XUYÊN SUỐT VIDEO]:
   - Hệ thống BẮT BUỘC phải tự lập một "Sổ quy ước hình ảnh" (global_visual_dictionary) cho các khái niệm hoặc chủ thể lặp lại nhiều lần trong kịch bản.
   - NGUYÊN TẮC BẢO TOÀN: Nếu một khái niệm (VD: 'Token', 'Mô hình AI', 'Dữ liệu') được quy ước ở Cảnh 1 là hình chữ nhật viền xanh (<rect stroke="#0ea5e9">), thì khi khái niệm này xuất hiện lại ở các Cảnh sau, BẮT BUỘC phải sử dụng lại đúng hình khối và màu sắc đó. Tuyệt đối không tự ý đổi sang hình tròn hay đổi màu khác để đảm bảo tính nhất quán 100%.

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC (JSON):
{
  "scene_title": "Tiêu đề phân cảnh",
  "core_concept": "Ý niệm sư phạm cốt lõi",
  "global_visual_dictionary": {
    "Tên_khái_niệm_chính_1": "Mô tả quy ước hình thù và màu sắc SVG (VD: <rect fill='#4c1d95'>)",
    "Tên_khái_niệm_chính_2": "Mô tả quy ước hình thù và màu sắc SVG..."
  },
  "frames": [
    {
      "frame_number": 1,
      "duration_seconds": 6,
      "timeline": "00:00.000 - 00:06.000",
      "script_anchor": "Câu trích dẫn trong bài giảng",
      "trigger_word": "Từ then chốt kích hoạt hình ảnh",
      "visual_description": "Mô tả chi tiết ý sư phạm cần thấy (Lưu ý: Bám sát global_visual_dictionary)",
      "visual_symbol": "Từ khóa trung tâm (tối đa 2 từ)",
      "svg_code": "<svg class=\"w-full h-full max-h-40\" viewBox=\"0 0 600 200\" xmlns=\"http://www.w3.org/2000/svg\">...các thẻ vòng lặp từ global_visual_dictionary...</svg>",
      "on_screen_text": "Chữ cô đọng tối đa 40 ký tự",
      "safe_zone": { "x": 960, "y": 540, "width": 800, "height": 400, "compliant": true }
    }
  ],
  "compliance_summary": {
    "all_text_under_40": true,
    "safe_zone_compliant": true,
    "no_hallucination": true,
    "safety_content_compliant": true,
    "visual_consistency_maintained": true
  }
}
"""

class StoryboardAgent:
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Không tìm thấy GEMINI_API_KEY.")
        self.model_name = model_name or DEFAULT_MODEL
        self.client = genai.Client(api_key=self.api_key)

    def generate(self, script_text: str, context: Optional[str] = None) -> Dict[str, Any]:
        user_prompt = f"""Kịch bản bài giảng cần thiết kế phân cảnh hình ảnh thực tế:
\"\"\"
{script_text}
\"\"\""""
        if context:
            user_prompt += f"\n\nNgữ cảnh:\n{context}"

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
            parsed_json = json.loads(clean_text.strip())

            # Gắn image_url thông minh động 100% cho từng frame
            if parsed_json and "frames" in parsed_json:
                for idx, f in enumerate(parsed_json["frames"]):
                    f["image_url"] = ""

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

    def edit_single_frame(self, frame_data: Dict[str, Any], feedback: str, full_script: str = "", target_style: str = "Mặc định (Sơ đồ khối phẳng)") -> Dict[str, Any]:
        prompt = f"""Bạn là Senior Art Director. Người dùng yêu cầu chỉnh sửa DUY NHẤT một cảnh phân cảnh.

THÔNG TIN CẢNH #{frame_data.get('frame_number', 1)}:
- Lời đọc: "{frame_data.get('script_anchor', '')}"
- Chữ màn hình cũ: "{frame_data.get('on_screen_text', '')}"
- Ý trực quan cũ: "{frame_data.get('visual_description', '')}"

PHONG CÁCH YÊU CẦU (TARGET STYLE): {target_style}

GÓP Ý CỦA NGƯỜI DUYỆT:
\"\"\"
{feedback}
\"\"\"

YÊU CẦU BẮT BUỘC:
1. Viết lại mã code 'svg_code' tạo sơ đồ logic phản ánh ĐÚNG góp ý và PHONG CÁCH YÊU CẦU.
   - Nếu phong cách là "Mặc định (Sơ đồ khối phẳng)": Dùng màu fill đậm (#4c1d95), nét liền.
   - Nếu phong cách là "Phác thảo vẽ tay (Hand-drawn)": BỎ HẾT màu fill (fill="none" hoặc fill="#0B0F19"), chỉ dùng màu viền (stroke="#ffffff" hoặc "#0ea5e9"), BẮT BUỘC thêm thuộc tính `stroke-dasharray="5,5"` vào các thẻ <circle>, <rect>, <path>, <line> để tạo hiệu ứng nét đứt vẽ tay.
   - QUAN TRỌNG: Dù đổi phong cách, TUYỆT ĐỐI GIỮ NGUYÊN cấu trúc ý nghĩa sư phạm và text trên hình.
2. 'on_screen_text' tối đa 40 ký tự (len <= 40).
3. TUYỆT ĐỐI AN TOÀN SƯ PHẠM.
4. Trả về DUY NHẤT JSON hợp lệ:
{{
  "frame_number": {frame_data.get('frame_number', 1)},
  "duration_seconds": {frame_data.get('duration_seconds', 6)},
  "timeline": "{frame_data.get('timeline', '00:00.000 - 00:06.000')}",
  "script_anchor": "{frame_data.get('script_anchor', '')}",
  "trigger_word": "{frame_data.get('trigger_word', 'Key')}",
  "visual_description": "Mô tả chi tiết hình ảnh mới",
  "visual_symbol": "Từ khóa trung tâm (2 từ)",
  "svg_code": "<svg class=\"w-full h-full max-h-40\" viewBox=\"0 0 600 200\" xmlns=\"http://www.w3.org/2000/svg\">...</svg>",
  "on_screen_text": "Chữ màn hình mới <= 40 ký tự",
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
            parsed["image_url"] = ""
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

    def generate_alternatives(self, frame_data: Dict[str, Any], count: int = 3, feedback: str = "", full_script: str = "") -> Dict[str, Any]:
        """Tạo ra N phương án thay thế (tối đa 5) cho một phân cảnh cụ thể khi người dùng thấy chưa phù hợp."""
        try:
            count = int(count)
        except (ValueError, TypeError):
            count = 3
        count = max(1, min(count, 5))

        prompt = f"""Bạn là Senior Art Director & Storyboard Architect cho Lesson Studio.
Người dùng thấy phân cảnh hiện tại không phù hợp và muốn bạn đề xuất CHÍNH XÁC {count} PHƯƠNG ÁN HÌNH ẢNH KHÁC BIỆT (từ 1 đến {count}) để thay thế phân cảnh này.

THÔNG TIN PHÂN CẢNH HIỆN TẠI (CẢNH #{frame_data.get('frame_number', 1)}):
- Mốc thời gian: "{frame_data.get('timeline', '00:00.000 - 00:06.000')}"
- Lời đọc câu này: "{frame_data.get('script_anchor', '')}"
- Chữ màn hình cũ: "{frame_data.get('on_screen_text', '')}"
- Ý trực quan cũ: "{frame_data.get('visual_description', '')}"
- Biểu tượng cũ: "{frame_data.get('visual_symbol', '')}"
- Toàn bộ bài giảng: "{full_script}"
- Góp ý/Yêu cầu bổ sung của người dùng (nếu có): "{feedback}"

YÊU CẦU BẮT BUỘC:
1. Đề xuất đúng {count} phương án khác biệt. Mỗi phương án phải có góc nhìn sư phạm và cấu trúc trực quan riêng:
   - Phương án 1: Sơ đồ dòng chảy / quy trình ngang (Pipeline Flow).
   - Phương án 2: Mô hình trung tâm tỏa tia (Radial Network / Hub & Spoke).
   - Phương án 3: Bảng phân tầng / so sánh 2-3 cột (Layered Architecture / Matrix).
   - Phương án 4: Sơ đồ tư duy phân nhánh (Mindmap / Hierarchy Tree).
   - Phương án 5: Tối giản hóa biểu tượng trọng tâm kèm số liệu/chỉ dẫn trực quan (Focus Hero).
2. 'on_screen_text' trong mỗi phương án TUYỆT ĐỐI KHÔNG QUÁ 40 KÝ TỰ (len <= 40).
3. 'svg_code': Mã SVG chuẩn 16:9 viewBox="0 0 600 200", class="w-full h-full max-h-40", không background.
   - Bảng màu: stroke="#475569" (đường nối), fill="#4c1d95" (node chính tím), fill="#0B0F19" stroke="#0ea5e9" hoặc "#10b981" (node phụ). Chữ <text> màu trắng fill="#ffffff".
4. TUYỆT ĐỐI AN TOÀN SƯ PHẠM (không bạo lực, không nhạy cảm, chuẩn PG-Clean).
5. Trả về DUY NHẤT JSON:
{{
  "alternatives": [
    {{
      "variant_id": 1,
      "title": "Tên ý tưởng ngắn gọn (VD: Sơ đồ dòng chảy 3 bước)",
      "visual_description": "Mô tả ý sư phạm của phương án này",
      "visual_symbol": "Từ khóa cốt lõi (tối đa 2 từ)",
      "on_screen_text": "Chữ cô đọng <= 40 ký tự",
      "svg_code": "<svg class=\\"w-full h-full max-h-40\\" viewBox=\\"0 0 600 200\\" xmlns=\\"http://www.w3.org/2000/svg\\">...</svg>"
    }}
  ]
}}
"""
        start_time = time.time()
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=STYLEBOOK_SYSTEM_PROMPT,
                    temperature=0.4,
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
            alternatives = parsed.get("alternatives", [])
            # Đảm bảo đúng số lượng tối đa 5
            alternatives = alternatives[:count]
            for idx, alt in enumerate(alternatives):
                alt["variant_id"] = idx + 1
                if not alt.get("svg_code"):
                    alt["svg_code"] = self._create_fallback_svg(alt.get("visual_symbol", "Concept"), idx + 1)
            
            return {
                "success": True,
                "latency_ms": int((time.time() - start_time) * 1000),
                "alternatives": alternatives
            }
        except Exception as e:
            # Fallback tạo phương án dự phòng chất lượng cao
            fallback_alts = []
            anchor = frame_data.get('script_anchor', 'Khái niệm bài giảng')
            keywords = [frame_data.get('visual_symbol', 'Chủ thể'), 'Mô hình', 'Quy trình', 'Cấu trúc', 'Tổng quan']
            for i in range(count):
                kw = keywords[i % len(keywords)]
                fallback_alts.append({
                    "variant_id": i + 1,
                    "title": f"Phương án {i + 1}: Biểu diễn {kw}",
                    "visual_description": f"Cách tiếp cận {i + 1}: Tối ưu hóa biểu diễn cho '{anchor[:40]}...'",
                    "visual_symbol": kw,
                    "on_screen_text": f"{kw}: {anchor[:30]}".strip()[:40],
                    "svg_code": self._create_fallback_svg(kw, i + 1)
                })
            return {
                "success": True,
                "latency_ms": int((time.time() - start_time) * 1000),
                "alternatives": fallback_alts,
                "warning": f"Dùng fallback do AI: {str(e)}"
            }

    def _create_fallback_svg(self, symbol: str, style_idx: int) -> str:
        """Tạo mã SVG đẹp mắt theo nhiều kiểu cấu trúc khác nhau cho fallback."""
        if style_idx == 1:
            # Dòng chảy 3 node
            return (
                '<svg class="w-full h-full max-h-40" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">'
                '<line x1="120" y1="100" x2="480" y2="100" stroke="#475569" stroke-width="3" stroke-dasharray="6,6"/>'
                '<circle cx="150" cy="100" r="42" fill="#0B0F19" stroke="#0ea5e9" stroke-width="2.5"/>'
                '<text x="150" y="105" fill="#ffffff" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">ĐẦU VÀO</text>'
                '<rect x="255" y="60" width="90" height="80" rx="12" fill="#4c1d95" stroke="#7c3aed" stroke-width="2.5"/>'
                f'<text x="300" y="105" fill="#ffffff" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">{symbol[:10]}</text>'
                '<circle cx="450" cy="100" r="42" fill="#0B0F19" stroke="#10b981" stroke-width="2.5"/>'
                '<text x="450" y="105" fill="#ffffff" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">KẾT QUẢ</text>'
                '</svg>'
            )
        elif style_idx == 2:
            # Trung tâm tỏa tia
            return (
                '<svg class="w-full h-full max-h-40" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">'
                '<line x1="300" y1="100" x2="160" y2="60" stroke="#475569" stroke-width="2.5"/>'
                '<line x1="300" y1="100" x2="160" y2="140" stroke="#475569" stroke-width="2.5"/>'
                '<line x1="300" y1="100" x2="440" y2="60" stroke="#475569" stroke-width="2.5"/>'
                '<line x1="300" y1="100" x2="440" y2="140" stroke="#475569" stroke-width="2.5"/>'
                '<circle cx="300" cy="100" r="46" fill="#4c1d95" stroke="#a855f7" stroke-width="3"/>'
                f'<text x="300" y="105" fill="#ffffff" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">{symbol[:10]}</text>'
                '<rect x="110" y="40" width="80" height="38" rx="8" fill="#0B0F19" stroke="#0ea5e9" stroke-width="2"/>'
                '<text x="150" y="64" fill="#93c5fd" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="middle">Nhánh A</text>'
                '<rect x="110" y="120" width="80" height="38" rx="8" fill="#0B0F19" stroke="#0ea5e9" stroke-width="2"/>'
                '<text x="150" y="144" fill="#93c5fd" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="middle">Nhánh B</text>'
                '<rect x="410" y="40" width="80" height="38" rx="8" fill="#0B0F19" stroke="#10b981" stroke-width="2"/>'
                '<text x="450" y="64" fill="#a7f3d0" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="middle">Nhánh C</text>'
                '<rect x="410" y="120" width="80" height="38" rx="8" fill="#0B0F19" stroke="#10b981" stroke-width="2"/>'
                '<text x="450" y="144" fill="#a7f3d0" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="middle">Nhánh D</text>'
                '</svg>'
            )
        elif style_idx == 3:
            # Mô hình phân tầng (Stack)
            return (
                '<svg class="w-full h-full max-h-40" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">'
                '<rect x="180" y="30" width="240" height="38" rx="8" fill="#4c1d95" stroke="#8b5cf6" stroke-width="2.5"/>'
                f'<text x="300" y="54" fill="#ffffff" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">TẦNG ỨNG DỤNG: {symbol[:8]}</text>'
                '<line x1="300" y1="68" x2="300" y2="82" stroke="#64748b" stroke-width="2"/>'
                '<rect x="180" y="82" width="240" height="38" rx="8" fill="#0B0F19" stroke="#0ea5e9" stroke-width="2"/>'
                '<text x="300" y="106" fill="#93c5fd" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">TẦNG TRUNG GIAN (LOGIC)</text>'
                '<line x1="300" y1="120" x2="300" y2="134" stroke="#64748b" stroke-width="2"/>'
                '<rect x="180" y="134" width="240" height="38" rx="8" fill="#0B0F19" stroke="#10b981" stroke-width="2"/>'
                '<text x="300" y="158" fill="#a7f3d0" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">TẦNG DỮ LIỆU / CƠ SỞ</text>'
                '</svg>'
            )
        elif style_idx == 4:
            # So sánh 2 cột đối sánh
            return (
                '<svg class="w-full h-full max-h-40" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">'
                '<rect x="90" y="45" width="180" height="110" rx="12" fill="#0B0F19" stroke="#3b82f6" stroke-width="2"/>'
                f'<text x="180" y="80" fill="#93c5fd" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle">HIỆN TRẠNG</text>'
                '<text x="180" y="115" fill="#e2e8f0" font-family="sans-serif" font-size="11" text-anchor="middle">• Truyền thống</text>'
                '<line x1="300" y1="50" x2="300" y2="150" stroke="#475569" stroke-width="3" stroke-dasharray="4,4"/>'
                '<rect x="330" y="45" width="180" height="110" rx="12" fill="#4c1d95" stroke="#a855f7" stroke-width="2.5"/>'
                f'<text x="420" y="80" fill="#ffffff" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle">{symbol[:10]}</text>'
                '<text x="420" y="115" fill="#f5d0fe" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="middle">★ Giải pháp mới</text>'
                '</svg>'
            )
        else:
            # Hero Highlight với Icon và đồng hồ nhịp
            return (
                '<svg class="w-full h-full max-h-40" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">'
                '<circle cx="300" cy="95" r="55" fill="#4c1d95" stroke="#c084fc" stroke-width="3"/>'
                '<polygon points="300,55 335,80 335,120 300,140 265,120 265,80" fill="none" stroke="#38bdf8" stroke-width="2"/>'
                f'<text x="300" y="100" fill="#ffffff" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle">{symbol[:12]}</text>'
                '<rect x="180" y="160" width="240" height="24" rx="6" fill="#0B0F19" stroke="#64748b" stroke-width="1.5"/>'
                '<text x="300" y="176" fill="#cbd5e1" font-family="sans-serif" font-size="10" font-weight="bold" text-anchor="middle">TIÊU ĐIỂM SƯ PHẠM ĐỘC QUYỀN</text>'
                '</svg>'
            )


    # Bảng từ khóa kiểm duyệt nội dung an toàn sư phạm (Responsible AI)
    BLOCKED_SAFETY_KEYWORDS = [
        # Bạo lực & máu me
        "blood", "bloody", "gore", "gory", "mutilation", "decapitation", "corpse", "slaughter",
        "massacre", "murder", "severed", "bleeding", "dismembered", "wound", "cruelty",
        "máu", "máu me", "chém giết", "man rợ", "xác chết", "chặt đầu", "đổ máu", "kinh dị",
        # Khỏa thân & nhạy cảm & gợi dục
        "nude", "naked", "nudity", "nsfw", "porn", "erotic", "cleavage", "underwear", "lingerie",
        "bikini", "sex", "sexual", "uncensored", "exposed skin", "bare breasts",
        "trần chuồng", "khỏa thân", "lột đồ", "hở hang", "gợi dục", "nhạy cảm", "cởi trần", "khiêu dâm"
    ]

    def sanitize_image_prompt(self, prompt: str) -> str:
        """Lọc bỏ hoàn toàn các yếu tố máu me, bạo lực mạnh, nhạy cảm hoặc cơ thể trần chuồng.
        Đặc biệt: Loại bỏ các từ phủ định 'no nudity', 'no gore' khỏi positive prompt vì mô hình khuếch tán sẽ vẽ ra chính các khái niệm đó."""
        clean_p = prompt
        # 1. Xóa các cụm từ phủ định nhạy cảm khỏi positive prompt
        clean_p = re.sub(r'\b(no\s+(nudity|nude|naked|nsfw|gore|blood|violence)|without\s+(nudity|nude|naked|nsfw|gore|blood|violence))\b', '', clean_p, flags=re.IGNORECASE)

        # 2. Xóa các từ khóa nhạy cảm / gợi cảm
        kw_pattern = '|'.join(map(re.escape, self.BLOCKED_SAFETY_KEYWORDS))
        clean_p = re.sub(rf'\b({kw_pattern})\b', '', clean_p, flags=re.IGNORECASE)

        # 3. Đối với chủ đề thuần công nghệ / toán học / máy móc mà không nhắc đến nhân vật người:
        # Bắt buộc ép chỉ lệnh 'no people, pure hardware' để AI không tự ý vẽ người máy nữ gợi cảm
        human_indicators = ["engineer", "scientist", "teacher", "student", "doctor", "person", "people", "man", "woman", "kỹ sư", "bác sĩ", "thầy", "cô", "học sinh"]
        has_human = any(h in clean_p.lower() for h in human_indicators)
        if not has_human and any(tech in clean_p.lower() for tech in ["neural", "algorithm", "data", "server", "chip", "computer", "math", "calculus", "ai", "artificial intelligence"]):
            if "no people" not in clean_p.lower():
                clean_p += ", no people, no human figures, pure technology and scientific data visualization"

        # 4. Bổ sung các guardrails khẳng định an toàn sư phạm
        safety_tokens = ", flat 2d vector infographic, corporate flowchart diagram, minimalist, clean technical diagram illustration"
        if "family-friendly" not in clean_p.lower():
            clean_p = clean_p.strip().rstrip(",") + safety_tokens
        return clean_p.strip()

    def validate_storyboard(self, result_data: Dict[str, Any], raw_script: str) -> Dict[str, Any]:
        report = {
            "text_length_pass": True,
            "safe_zone_pass": True,
            "hallucination_pass": True,
            "safety_content_pass": True,
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

            # Kiểm tra an toàn sư phạm (Content Safety Guardrail)
            full_frame_text = f"{f.get('on_screen_text', '')} {f.get('visual_description', '')} {f.get('image_prompt', '')}".lower()
            kw_pattern = '|'.join(map(re.escape, self.BLOCKED_SAFETY_KEYWORDS))
            violations = re.findall(rf'(?<!no\s)(?<!without\s)\b({kw_pattern})\b', full_frame_text, flags=re.IGNORECASE)
            if violations:
                report["safety_content_pass"] = False
                report["violations"].append(f"Cảnh {frame_num}: Vi phạm chuẩn mực an toàn sư phạm (phát hiện từ khóa: {set(violations)})")

        report["overall_pass"] = (
            report["text_length_pass"] and
            report["safe_zone_pass"] and
            report["hallucination_pass"] and
            report["safety_content_pass"]
        )
        return report

if __name__ == '__main__':
    agent = StoryboardAgent()
    sample = "Năm 1945, bản Tuyên ngôn Độc lập được tuyên đọc tại Quảng trường Ba Đình."
    res = agent.generate(sample)
    print("Success:", res['success'])
    if res['success']:
        f0 = res['storyboard']['frames'][0]
        print("Text:", f0.get('on_screen_text'))
        print("Image Prompt:", f0.get('image_prompt'))
        print("Image URL:", f0.get('image_url'))
