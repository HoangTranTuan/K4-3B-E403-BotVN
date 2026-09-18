import json
import re
from copy import deepcopy

from google import genai
from google.genai import types


MODEL_NAME = "gemini-2.5-flash"


DEFAULT_STYLEBOOK = """
SỔ QUY ƯỚC HÌNH ẢNH

1. Màu xanh dương:
   - dữ liệu
   - input
   - token hoặc mảnh văn bản

2. Màu tím:
   - mô hình AI
   - hệ thống xử lý
   - thuật toán

3. Màu xanh lá:
   - kết quả
   - output
   - thông tin đã hoàn tất

4. Màu vàng:
   - cảnh báo
   - thông tin cần kiểm tra
   - uncertainty

5. Một khái niệm xuất hiện nhiều lần phải giữ:
   - cùng biểu tượng
   - cùng màu
   - cùng vai trò thị giác

6. Không tự thêm:
   - số liệu
   - phần trăm
   - ngày giờ
   - tên riêng
   - logo
   - kết quả
   nếu lời đọc không nói.

7. Không dùng:
   - logo có bản quyền
   - hình người thật
   - nhân vật có bản quyền

8. Chữ trên màn hình tối đa 40 ký tự.

9. Khung hình:
   - 1920x1080
   - 30fps
   - vùng nội dung an toàn x=80..1840, y=250..960
   - vùng dưới y=960..1080 dành cho phụ đề
""".strip()


def _get_client(api_key):
    if not api_key:
        raise ValueError("Chưa có GEMINI_API_KEY.")

    return genai.Client(api_key=api_key)


def _clean_json(raw_text):
    if not raw_text:
        raise ValueError("Model không trả dữ liệu.")

    text = raw_text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    first_object = text.find("{")
    first_array = text.find("[")

    candidates = [
        x for x in [first_object, first_array]
        if x >= 0
    ]

    if candidates:
        text = text[min(candidates):]

    return json.loads(text)


def _call_json(prompt, api_key, temperature=0.25):
    client = _get_client(api_key)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="application/json",
        ),
    )

    return _clean_json(response.text)


def _compact_sentence(sentence):
    result = {
        "n": sentence.get("n"),
        "loi": sentence.get("loi", ""),
        "soFrame": sentence.get("soFrame"),
        "batDau": sentence.get("batDau"),
        "ketThuc": sentence.get("ketThuc"),
    }

    chuoi_moc_tu = sentence.get("chuoiMocTu")

    if chuoi_moc_tu:
        result["chuoiMocTu"] = chuoi_moc_tu

    moc_tu = sentence.get("mocTu")

    if moc_tu:
        result["mocTu"] = moc_tu

    return result


def audit_scene(scene, narration):
    """
    Rule đơn giản chạy local.
    Không cần AI.
    """

    issues = []

    screen_text = str(
        scene.get("on_screen_text", "")
    ).strip()

    if len(screen_text) > 40:
        issues.append(
            f"Chữ màn hình dài {len(screen_text)} ký tự, vượt giới hạn 40."
        )

    # Kiểm tra số AI có tự thêm không.
    narration_numbers = set(
        re.findall(r"\d+(?:[.,]\d+)?%?", narration or "")
    )

    visual_blob = " ".join(
        [
            str(scene.get("visual_description", "")),
            str(scene.get("on_screen_text", "")),
        ]
    )

    output_numbers = set(
        re.findall(r"\d+(?:[.,]\d+)?%?", visual_blob)
    )

    invented_numbers = output_numbers - narration_numbers

    if invented_numbers:
        issues.append(
            "Có số không xuất hiện trong lời đọc: "
            + ", ".join(sorted(invented_numbers))
        )

    if not scene.get("teaching_intent"):
        issues.append("Thiếu teaching intent.")

    if not scene.get("visual_description"):
        issues.append("Thiếu mô tả hình.")

    if not scene.get("on_screen_text"):
        issues.append("Thiếu chữ trên màn hình.")

    return {
        "passed": len(issues) == 0,
        "issues": issues,
    }


def generate_storyboard(
    sentences,
    stylebook,
    api_key,
):
    compact = [
        _compact_sentence(item)
        for item in sentences
        if item.get("loi")
    ]

    prompt = f"""
Bạn là StoryboardAI cho video bài giảng tiếng Việt.

NHIỆM VỤ
Biến từng câu lời đọc thành đúng MỘT scene storyboard.

SỔ QUY ƯỚC CỦA ĐỘI
{stylebook}

YÊU CẦU BẮT BUỘC

- Không thêm kiến thức, số liệu, phần trăm, ngày giờ, tên riêng hoặc kết quả
  không xuất hiện trong narration.
- Một concept lặp lại phải dùng cùng consistency_key.
- on_screen_text tối đa 40 ký tự.
- Tách rõ:
  teaching_intent = ý cần truyền đạt.
  visual_description = cách thể hiện ý đó bằng hình.
- Không cần tạo video thật.
- Ảnh phác sẽ được frontend dựng bằng SVG.
- Chọn sketch_type trong:
  diagram, comparison, timeline, cards, concept.
- Nếu câu trừu tượng, dùng sơ đồ khái niệm thay vì bịa vật thể cụ thể.
- Nếu narration không có số thì visual không được tự thêm số.
- trigger_phrase phải là một cụm từ có trong narration.
- Nếu có mocTu, trigger_frame phải dựa vào mocTu.
- Nếu không chắc frame, dùng 0 thay vì bịa.
- Không dùng logo hoặc người thật.

OUTPUT
Chỉ trả JSON theo đúng cấu trúc:

{{
  "scenes": [
    {{
      "n": 1,
      "narration": "...",
      "teaching_intent": "...",
      "visual_description": "...",
      "on_screen_text": "...",
      "layout": "...",
      "trigger_phrase": "...",
      "trigger_frame": 0,
      "sketch_type": "diagram",
      "consistency_key": "...",
      "reasoning_short": "giải thích ngắn vì sao chọn cách vẽ"
    }}
  ]
}}

INPUT:
{json.dumps(compact, ensure_ascii=False)}
"""

    result = _call_json(
        prompt,
        api_key,
        temperature=0.20,
    )

    scenes = result.get("scenes", [])

    narration_map = {
        item.get("n"): item.get("loi", "")
        for item in compact
    }

    clean_scenes = []

    for scene in scenes:
        scene_number = scene.get("n")

        if scene_number not in narration_map:
            continue

        scene["narration"] = narration_map[scene_number]

        scene["audit"] = audit_scene(
            scene,
            narration_map[scene_number],
        )

        clean_scenes.append(scene)

    clean_scenes.sort(
        key=lambda x: x.get("n", 0)
    )

    return clean_scenes


def revise_scene(
    scene,
    feedback,
    stylebook,
    api_key,
):
    original = deepcopy(scene)

    prompt = f"""
Bạn là StoryboardAI.

Người duyệt đang sửa DUY NHẤT một scene.

QUY TẮC QUAN TRỌNG

- Chỉ sửa scene được gửi.
- Giữ nguyên scene number.
- Không thêm dữ kiện không có trong narration.
- Chữ màn hình tối đa 40 ký tự.
- Giữ đúng sổ quy ước.
- Giữ teaching_intent nếu feedback chỉ yêu cầu đổi cách vẽ.
- Không dùng logo hoặc người thật.
- Nếu feedback yêu cầu thông tin không có trong narration,
  bỏ phần yêu cầu ngoài phạm vi và ghi lại trong reasoning_short.
- Chọn sketch_type:
  diagram, comparison, timeline, cards hoặc concept.

SỔ QUY ƯỚC:
{stylebook}

SCENE HIỆN TẠI:
{json.dumps(original, ensure_ascii=False)}

FEEDBACK:
{feedback}

Trả về DUY NHẤT JSON:

{{
  "n": 1,
  "narration": "...",
  "teaching_intent": "...",
  "visual_description": "...",
  "on_screen_text": "...",
  "layout": "...",
  "trigger_phrase": "...",
  "trigger_frame": 0,
  "sketch_type": "diagram",
  "consistency_key": "...",
  "reasoning_short": "..."
}}
"""

    revised = _call_json(
        prompt,
        api_key,
        temperature=0.25,
    )

    # Không cho model đổi scene number.
    revised["n"] = original["n"]

    # Không cho model sửa narration.
    revised["narration"] = original.get(
        "narration",
        ""
    )

    revised["audit"] = audit_scene(
        revised,
        revised["narration"],
    )

    return revised