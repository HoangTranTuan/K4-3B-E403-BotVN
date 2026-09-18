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

STYLEBOOK_SYSTEM_PROMPT = """Bạn là Senior Art Director & Storyboard Architect cho nền tảng Lesson Studio (Đề C4).
Nhiệm vụ của bạn là chuyển hóa kịch bản bài giảng thành kịch bản phân cảnh hình ảnh với ẢNH MINH HỌA CONCEPT ART ĐIỆN ẢNH SƯ PHẠM 100% (Chuẩn mực giáo dục học đường, đồ họa khoa học hiện đại, sắc nét).

QUY CHUẨN QUAN TRỌNG:
1. [RÀNG BUỘC KÝ TỰ] 'on_screen_text' TUYỆT ĐỐI KHÔNG QUÁ 40 KÝ TỰ (len <= 40). Chữ cô đọng, súc tích.
2. [VÙNG AN TOÀN - SAFE ZONE] Tọa độ x: [80, 1840], y: [250, 960].
3. [NGHIÊM CẤM ẢO GIÁC - CA KHÓ 13 CỦA HẢI]: Không tự ý bịa số liệu % hoặc thống kê nếu kịch bản chỉ có tính định tính.
4. [TẠO DỰNG Ý NIỆM HÌNH ẢNH SỐNG ĐỘNG - LINH HOẠT THEO ĐÚNG SẮC THÁI CỦA TỪNG CÂU VÀ NGỮ CẢNH CỤ THỂ]:
   - Với mỗi cảnh, bạn PHẢI VIẾT một câu 'image_prompt' tiếng Anh cực kỳ chi tiết, sống động theo phong cách nghệ thuật:
     "Clean modern educational digital concept art of [mô tả chi tiết chủ thể thực tế, bối cảnh, ánh sáng, góc máy], professional scientific editorial illustration style, masterpiece, 16:9 aspect ratio, family-friendly educational concept art, professional academic presentation"
   - TUYỆT ĐỐI KHÔNG DẬP KHUÔN CÙNG MỘT HÌNH ẢNH CHO CÙNG MỘT TỪ KHÓA:
     * Mỗi lần tạo ảnh, mỗi phân cảnh trong kịch bản PHẢI LÀ MỘT BỨC TRANH ĐỘC BẢN, phản ánh chính xác sắc thái, khía cạnh chuyên sâu và thời không của câu nói đó:
     * Ví dụ với "AI / Trí tuệ nhân tạo":
       + Nếu nói về "AI phát triển / Bản chất AI": Phải vẽ các dàn máy chủ siêu máy tính hiện đại phát sáng, mạng nơ-ron không gian 3D kết nối các nút dữ liệu, vi mạch bán dẫn tinh xảo (glowing 3D neural network topology, futuristic data center server racks, glowing semiconductor microchips, data visualization streams, no human figures, pure technology). CẤM TIỆT vẽ hình dáng người hay robot nữ/nam!
       + Nếu nói về "Toán học / Nền tảng của AI": Phải vẽ các công thức vi tích phân phát sáng, ma trận đại số tuyến tính 3 chiều, không gian hình học vector đan xen các nút mạng nơ-ron rực rỡ (glowing mathematical calculus equations, linear algebra matrices in 3D coordinate space, geometric vector fields intertwined with luminous neural nodes, no people).
       + Nếu nói về "AI trong y tế": Bác sĩ đeo khẩu trang mặc áo blouse trắng rộng rãi cùng mô hình chẩn đoán 3D, bản đồ phân tử sinh học.
       + Nếu nói về "AI trong nông nghiệp / môi trường": Drone tự hành bay qua cánh đồng xanh, cảm biến thông minh.
       + Nếu nói về "Kỹ sư / Nhân lực công nghệ": Kỹ sư mặc áo sơ mi công sở lịch sự hoặc áo lab rộng rãi làm việc trước màn hình hiển thị code.
     * Ví dụ với "Ba Đình / Địa danh":
       + Nếu nói về "Năm 1945 / Tuyên ngôn": Bác Hồ đứng trên bục gỗ phát biểu trước biển người dân và cờ đỏ sao vàng lịch sử dưới nắng thu Ba Đình.
       + Nếu nói về "Quảng trường Ba Đình đêm pháo hoa / ngày lễ": Toàn cảnh Quảng trường Ba Đình rực rỡ dưới bầu trời đêm ngập tràn pháo hoa đa sắc màu, người dân hân hoan vẫy cờ.
       + Nếu nói về "Lăng Bác / Buổi sáng / Thượng cờ": Lăng Chủ tịch uy nghiêm trong ánh bình minh mờ sương, tiêu binh bồng súng trang nghiêm, hàng tre ngà rì rào.
     * Với kịch bản nhiều phân cảnh (multi-frame): Mỗi cảnh phải thể hiện một góc nhìn/chủ thể tiếp nối mới mẻ, KHÔNG lặp lại cùng một góc máy hay mô tả hình ảnh giữa các cảnh!
   - NGUYÊN TẮC VÀNG VỀ ĐỒNG NHẤT THỊ GIÁC (DIRECT SUBJECT FOCUS - NGHIÊM CẤM TỰ BỊA LỚP HỌC):
     * Hình ảnh PHẢI TẢ ĐÚNG VÀ TRỰC DIỆN CHỦ THỂ CỐT LÕI của câu nói:
       + Nói về "lửa / nghịch lửa / cẩn thận với lửa": Phải vẽ NGỌN LỬA CHÁY RỰC SÁNG, ĐỐNG LỬA TRẠI BỐC KHÓI, TÀN LỬA ĐỎ CAM RỰC RỠ hoặc BIỂN CẢNH BÁO NGUY CƠ CHÁY NỔ (bright burning campfire flames, crackling fire embers, dramatic smoke, caution fire hazard warning sign). CẤM TIỆT vẽ lớp học hay phòng học!
       + Nói về "đại dương / cá voi / sinh vật biển": Phải vẽ lòng đại dương xanh thẳm lung linh. CẤM vẽ lớp học!
       + Nói về "núi lửa / thiên nhiên hoang dã": Phải vẽ đúng khung cảnh thiên nhiên hùng vĩ. CẤM vẽ lớp học!
     * LƯU Ý ĐẶC BIỆT: Trừ khi kịch bản nhắc đến "lớp học, trường học, giáo viên, học sinh", NGHIÊM CẤM TỰ Ý CHÈN các từ "classroom, school, teacher, students listening" vào câu image_prompt!
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

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC (JSON):
{
  "scene_title": "Tiêu đề phân cảnh",
  "core_concept": "Ý niệm sư phạm cốt lõi",
  "frames": [
    {
      "frame_number": 1,
      "duration_seconds": 6,
      "timeline": "00:00.000 - 00:06.000",
      "script_anchor": "Câu trích dẫn trong bài giảng",
      "trigger_word": "Từ then chốt kích hoạt hình ảnh",
      "visual_description": "Mô tả chi tiết ý sư phạm cần thấy",
      "visual_symbol": "Tên chủ thể chính",
      "on_screen_text": "Chữ cô đọng tối đa 40 ký tự",
      "image_prompt": "Vibrant educational digital concept art of ..., 16:9",
      "safe_zone": { "x": 960, "y": 540, "width": 800, "height": 400, "compliant": true }
    }
  ],
  "compliance_summary": {
    "all_text_under_40": true,
    "safe_zone_compliant": true,
    "no_hallucination": true,
    "safety_content_compliant": true
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
                    f["image_url"] = self._resolve_image_url(f, script_text, frame_idx=idx)

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
        prompt = f"""Bạn là Senior Art Director. Người dùng yêu cầu chỉnh sửa DUY NHẤT một cảnh phân cảnh.

THÔNG TIN CẢNH #{frame_data.get('frame_number', 1)}:
- Lời đọc: "{frame_data.get('script_anchor', '')}"
- Chữ màn hình cũ: "{frame_data.get('on_screen_text', '')}"
- Ý trực quan cũ: "{frame_data.get('visual_description', '')}"

GÓP Ý CỦA NGƯỜI DUYỆT:
\"\"\"
{feedback}
\"\"\"

YÊU CẦU:
1. Viết lại câu 'image_prompt' tiếng Anh cực kỳ chi tiết theo đúng góp ý của người duyệt (phong cách Vibrant educational digital concept art, anime editorial illustration style, 16:9).
2. 'on_screen_text' tối đa 40 ký tự (len <= 40).
3. TUYỆT ĐỐI AN TOÀN SƯ PHẠM: Không vẽ máu me, bạo lực ghê rợn, khỏa thân hay cơ thể trần chuồng nhạy cảm (luôn chèn 'family-friendly, fully clothed, no gore, no violence, no nudity').
4. Trả về DUY NHẤT JSON hợp lệ:
{{
  "frame_number": {frame_data.get('frame_number', 1)},
  "duration_seconds": {frame_data.get('duration_seconds', 6)},
  "timeline": "{frame_data.get('timeline', '00:00.000 - 00:06.000')}",
  "script_anchor": "{frame_data.get('script_anchor', '')}",
  "trigger_word": "{frame_data.get('trigger_word', 'Key')}",
  "visual_description": "Mô tả chi tiết hình ảnh mới",
  "visual_symbol": "Tên chủ thể mới",
  "on_screen_text": "Chữ màn hình mới <= 40 ký tự",
  "image_prompt": "Vibrant educational digital concept art of ..., 16:9",
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
            parsed["image_url"] = self._resolve_image_url(parsed, feedback, frame_idx=parsed.get("frame_number", 1))
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
        safety_tokens = ", family-friendly educational concept art, professional academic presentation, clean technical illustration"
        if "family-friendly" not in clean_p.lower():
            clean_p = clean_p.strip().rstrip(",") + safety_tokens
        return clean_p.strip()

    def _resolve_image_url(self, frame: Dict[str, Any], context_text: str = "", frame_idx: int = 0) -> str:
        """Sinh URL ảnh AI điện ảnh động 100% (Pollinations AI) với Negative Prompt kiểm duyệt triệt để nhạy cảm / khỏa thân."""
        raw_prompt = frame.get("image_prompt") or f"Clean modern educational digital concept art of {frame.get('visual_description', 'educational lesson')}, professional scientific editorial illustration style, masterpiece, 16:9 aspect ratio"
        # Bắt buộc đi qua màng lọc an toàn sư phạm (Content Safety Guardrail)
        safe_prompt = self.sanitize_image_prompt(raw_prompt)
        frame["image_prompt"] = safe_prompt

        encoded = urllib.parse.quote(safe_prompt)
        # Bộ Negative Prompt chuẩn học đường tuyệt đối ngăn chặn khỏa thân, đường cong gợi cảm hay bạo lực
        negative_prompt = "nudity, naked, sensual, suggestive, female curves, breasts, cleavage, revealing clothing, skintight, bodysuit, sexy, nsfw, erotic, violence, blood, gore, horrific, distorted body"
        encoded_neg = urllib.parse.quote(negative_prompt)

        # Sinh seed ngẫu nhiên độc nhất dựa trên timestamp mili-giây, số thứ tự cảnh và nội dung prompt
        frame_num = frame.get("frame_number", frame_idx + 1)
        unique_seed = int(time.time() * 1000 + frame_num * 3571 + abs(hash(safe_prompt))) % 1000000
        # Tối ưu kích thước 1024x576 chuẩn 16:9 sắc nét, kèm negative prompt và safe=true
        return f"https://image.pollinations.ai/prompt/{encoded}?negative={encoded_neg}&width=1024&height=576&nologo=true&seed={unique_seed}&safe=true"

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
