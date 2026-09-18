import json
import os
import re
from copy import deepcopy
from typing import Any

from google import genai
from google.genai import types


DEFAULT_STYLEBOOK = """
SỔ QUY ƯỚC HÌNH ẢNH

1. Xanh dương = dữ liệu, input, token hoặc mảnh văn bản.
2. Tím = AI, mô hình, thuật toán hoặc hệ thống xử lý.
3. Xanh lá = output, kết quả hoặc trạng thái hoàn tất.
4. Vàng = cảnh báo, uncertainty hoặc nội dung cần kiểm tra.
5. Một khái niệm xuất hiện nhiều lần phải giữ cùng biểu tượng, màu và vai trò thị giác.
6. Không tự thêm số liệu, phần trăm, ngày giờ, tên riêng, logo hoặc kết quả nếu lời đọc không nói.
7. Không dùng logo có bản quyền, người thật hoặc nhân vật có bản quyền.
8. Chữ trên màn hình tối đa 40 ký tự.
9. Khung 1920x1080, 30 fps; vùng dưới dành cho phụ đề.
10. Ưu tiên sơ đồ, thẻ, timeline, comparison hoặc concept map đơn giản.
""".strip()


# ============================================================
# GEMINI
# ============================================================

def _extract_json(text: str) -> Any:
    if not text:
        raise ValueError("Gemini không trả dữ liệu.")

    cleaned = text.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    )

    first_obj = cleaned.find("{")
    first_arr = cleaned.find("[")

    starts = [
        value
        for value in (first_obj, first_arr)
        if value >= 0
    ]

    if starts:
        cleaned = cleaned[min(starts):]

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Gemini trả JSON không hợp lệ: {exc}"
        ) from exc


def _call_json(
    prompt: str,
    api_key: str,
    temperature: float = 0.2,
) -> Any:

    if not api_key:
        raise ValueError(
            "Chưa cấu hình GEMINI_API_KEY."
        )

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash",
    )

    # Quan trọng:
    # giữ client trong biến local cho đến khi request hoàn tất.
    client = genai.Client(
        api_key=api_key
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json",
            ),
        )

        if response is None:
            raise ValueError(
                "Gemini không trả response."
            )

        if not response.text:
            raise ValueError(
                "Gemini không trả nội dung."
            )

        return _extract_json(
            response.text
        )

    except Exception as exc:
        raise RuntimeError(
            f"Lỗi khi gọi Gemini: {exc}"
        ) from exc


# ============================================================
# INPUT
# ============================================================

def _compact_sentence(
    sentence: dict,
) -> dict:

    return {
        "n": sentence.get("n"),
        "loi": sentence.get(
            "loi",
            "",
        ),
        "phan": sentence.get("phan"),
        "soFrame": sentence.get("soFrame"),
        "batDau": sentence.get("batDau"),
        "ketThuc": sentence.get("ketThuc"),
        "chuoiMocTu": sentence.get(
            "chuoiMocTu",
            sentence.get(
                "loi",
                "",
            ),
        ),
        "mocTu": sentence.get(
            "mocTu",
            [],
        ),
    }


def _normalize(
    text: str,
) -> str:

    return re.sub(
        r"\s+",
        " ",
        (text or "")
        .strip()
        .lower(),
    )


# ============================================================
# TIMING
# ============================================================

def resolve_trigger_frame(
    sentence: dict,
    trigger_phrase: str,
) -> int:

    """
    Lấy frame gần nhất từ mocTu
    thay vì để LLM tự đoán frame.
    """

    phrase = (
        trigger_phrase or ""
    ).strip()

    markers = (
        sentence.get("mocTu")
        or []
    )

    source = (
        sentence.get("chuoiMocTu")
        or sentence.get("loi")
        or ""
    )

    if (
        not phrase
        or not markers
        or not source
    ):
        return 0

    start = source.lower().find(
        phrase.lower()
    )

    # Nếu không match nguyên cụm,
    # thử từ đầu tiên.
    if start < 0:

        words = phrase.split()

        token = (
            words[0]
            if words
            else ""
        )

        if token:
            start = source.lower().find(
                token.lower()
            )

    if start < 0:
        return 0

    try:

        nearest = min(
            markers,
            key=lambda item: abs(
                int(item[0]) - start
            ),
        )

        return int(
            nearest[1]
        )

    except Exception:
        return 0


# ============================================================
# RULE CHECK
# ============================================================

def audit_scene(
    scene: dict,
    narration: str,
) -> dict:

    issues = []

    screen_text = str(
        scene.get(
            "on_screen_text",
            "",
        )
    ).strip()

    # --------------------------------------------------------
    # 40 ký tự
    # --------------------------------------------------------

    if len(screen_text) > 40:
        issues.append(
            f"On-screen text dài "
            f"{len(screen_text)} ký tự, "
            f"vượt giới hạn 40."
        )

    # --------------------------------------------------------
    # Kiểm tra AI tự thêm số
    # --------------------------------------------------------

    narration_numbers = set(
        re.findall(
            r"\d+(?:[.,]\d+)?%?",
            narration or "",
        )
    )

    visual_blob = " ".join(
        [
            str(
                scene.get(
                    "visual_description",
                    "",
                )
            ),
            str(
                scene.get(
                    "on_screen_text",
                    "",
                )
            ),
        ]
    )

    output_numbers = set(
        re.findall(
            r"\d+(?:[.,]\d+)?%?",
            visual_blob,
        )
    )

    invented_numbers = (
        output_numbers
        - narration_numbers
    )

    if invented_numbers:

        issues.append(
            "Có số không xuất hiện "
            "trong lời đọc: "
            + ", ".join(
                sorted(
                    invented_numbers
                )
            )
        )

    # --------------------------------------------------------
    # Trigger phrase
    # --------------------------------------------------------

    trigger_phrase = str(
        scene.get(
            "trigger_phrase",
            "",
        )
    ).strip()

    if (
        trigger_phrase
        and _normalize(
            trigger_phrase
        )
        not in _normalize(
            narration
        )
    ):
        issues.append(
            "Trigger phrase không xuất hiện "
            "nguyên văn trong lời đọc."
        )

    # --------------------------------------------------------
    # Required fields
    # --------------------------------------------------------

    if not scene.get(
        "teaching_intent"
    ):
        issues.append(
            "Thiếu teaching intent."
        )

    if not scene.get(
        "visual_description"
    ):
        issues.append(
            "Thiếu visual description."
        )

    if not screen_text:
        issues.append(
            "Thiếu on-screen text."
        )

    return {
        "passed": len(issues) == 0,
        "issues": issues,
    }


# ============================================================
# SANITIZE
# ============================================================

def _sanitize_scene(
    scene: dict,
    sentence: dict,
) -> dict:

    narration = sentence.get(
        "loi",
        "",
    )

    scene["n"] = sentence.get("n")

    scene["narration"] = narration

    scene["soFrame"] = sentence.get(
        "soFrame"
    )

    scene["batDau"] = sentence.get(
        "batDau"
    )

    scene["ketThuc"] = sentence.get(
        "ketThuc"
    )

    # --------------------------------------------------------
    # Sketch type
    # --------------------------------------------------------

    allowed_types = {
        "diagram",
        "comparison",
        "timeline",
        "cards",
        "concept",
    }

    if (
        scene.get("sketch_type")
        not in allowed_types
    ):
        scene["sketch_type"] = (
            "diagram"
        )

    # --------------------------------------------------------
    # Giới hạn chữ
    # --------------------------------------------------------

    text = str(
        scene.get(
            "on_screen_text",
            "",
        )
    ).strip()

    if len(text) > 40:

        scene[
            "on_screen_text"
        ] = (
            text[:39]
            .rstrip()
            + "…"
        )

    # --------------------------------------------------------
    # Timing
    # --------------------------------------------------------

    trigger = str(
        scene.get(
            "trigger_phrase",
            "",
        )
    ).strip()

    scene[
        "trigger_frame"
    ] = resolve_trigger_frame(
        sentence,
        trigger,
    )

    # --------------------------------------------------------
    # Audit
    # --------------------------------------------------------

    scene["audit"] = audit_scene(
        scene,
        narration,
    )

    return scene


# ============================================================
# GENERATE STORYBOARD
# ============================================================

def generate_storyboard(
    sentences: list[dict],
    stylebook: str,
    api_key: str,
) -> list[dict]:

    compact = [
        _compact_sentence(
            sentence
        )
        for sentence in sentences
        if sentence.get("loi")
    ]

    if not compact:
        raise ValueError(
            "Không có câu lời đọc hợp lệ."
        )

    prompt = f"""
Bạn là StoryboardAI cho video bài giảng tiếng Việt.

MỤC TIÊU

Nhận lời đọc đã chốt và tạo đúng
MỘT scene storyboard cho mỗi câu.

SỔ QUY ƯỚC

{stylebook}

QUY TẮC BẮT BUỘC

- Không thêm fact, số liệu, phần trăm,
  ngày giờ, tên riêng, logo hoặc kết quả
  không có trong narration.

- Tách rõ:
  teaching_intent = ý cần truyền đạt.
  visual_description = cách thể hiện bằng hình.

- on_screen_text tối đa 40 ký tự.

- trigger_phrase phải là một cụm từ
  xuất hiện nguyên văn trong narration.

- Không tự quyết định trigger_frame.
  Backend sẽ tính từ mocTu.

- Một concept xuất hiện nhiều lần
  phải dùng cùng consistency_key.

- Với câu trừu tượng:
  ưu tiên concept map hoặc sơ đồ.

- Không bịa vật thể cụ thể
  khi narration không cung cấp.

- sketch_type chỉ được là:
  diagram
  comparison
  timeline
  cards
  concept

- Visual phải đơn giản,
  dễ dựng trong khung 1920x1080.

- Không sinh video.
  Chỉ lập kế hoạch hình.

TRẢ VỀ JSON DUY NHẤT:

{{
  "scenes": [
    {{
      "n": 1,
      "teaching_intent": "...",
      "visual_description": "...",
      "on_screen_text": "...",
      "layout": "...",
      "trigger_phrase": "...",
      "sketch_type": "diagram",
      "consistency_key": "...",
      "reasoning_short": "..."
    }}
  ]
}}

INPUT:

{json.dumps(
    compact,
    ensure_ascii=False,
    indent=2
)}
"""

    data = _call_json(
        prompt,
        api_key,
        temperature=0.18,
    )

    raw_scenes = (
        data.get(
            "scenes",
            [],
        )
        if isinstance(
            data,
            dict,
        )
        else []
    )

    sentence_map = {
        item.get("n"): item
        for item in compact
    }

    result = []

    for raw in raw_scenes:

        scene_number = raw.get("n")

        sentence = sentence_map.get(
            scene_number
        )

        if not sentence:
            continue

        cleaned = _sanitize_scene(
            raw,
            sentence,
        )

        result.append(
            cleaned
        )

    result.sort(
        key=lambda item: int(
            item.get("n")
            or 0
        )
    )

    return result


# ============================================================
# REVISE ONE SCENE
# ============================================================

def revise_scene(
    scene: dict,
    feedback: str,
    stylebook: str,
    api_key: str,
    original_sentence: dict | None = None,
) -> dict:

    if not feedback.strip():
        raise ValueError(
            "Feedback đang trống."
        )

    original = deepcopy(
        scene
    )

    narration = original.get(
        "narration",
        "",
    )

    prompt = f"""
Bạn là StoryboardAI.

Người duyệt đang sửa DUY NHẤT
một scene.

QUY TẮC

- Chỉ sửa scene được gửi.

- Không đổi scene number.

- Không đổi narration.

- Nếu feedback chỉ nói về hình,
  giữ nguyên teaching_intent.

- Không thêm fact,
  số liệu,
  tên riêng,
  logo
  nếu narration không có.

- on_screen_text tối đa 40 ký tự.

- trigger_phrase phải nằm trong narration.

- sketch_type chỉ là:
  diagram
  comparison
  timeline
  cards
  concept

- Giữ consistency_key
  nếu concept không thay đổi.

- Nếu feedback yêu cầu
  thông tin ngoài narration,
  không thực hiện phần đó.

- Ghi lý do ngắn trong reasoning_short.

SỔ QUY ƯỚC

{stylebook}

SCENE HIỆN TẠI

{json.dumps(
    original,
    ensure_ascii=False,
    indent=2
)}

FEEDBACK

{feedback}

TRẢ VỀ JSON DUY NHẤT:

{{
  "n": {json.dumps(original.get("n"))},
  "teaching_intent": "...",
  "visual_description": "...",
  "on_screen_text": "...",
  "layout": "...",
  "trigger_phrase": "...",
  "sketch_type": "diagram",
  "consistency_key": "...",
  "reasoning_short": "..."
}}
"""

    revised = _call_json(
        prompt,
        api_key,
        temperature=0.22,
    )

    # --------------------------------------------------------
    # Không cho AI đổi ID
    # --------------------------------------------------------

    revised["n"] = original.get(
        "n"
    )

    # --------------------------------------------------------
    # Không cho AI đổi narration
    # --------------------------------------------------------

    revised["narration"] = (
        narration
    )

    revised["soFrame"] = (
        original.get(
            "soFrame"
        )
    )

    revised["batDau"] = (
        original.get(
            "batDau"
        )
    )

    revised["ketThuc"] = (
        original.get(
            "ketThuc"
        )
    )

    # --------------------------------------------------------
    # Trigger frame
    # --------------------------------------------------------

    if original_sentence:

        revised[
            "trigger_frame"
        ] = resolve_trigger_frame(
            original_sentence,
            revised.get(
                "trigger_phrase",
                "",
            ),
        )

    else:

        revised[
            "trigger_frame"
        ] = original.get(
            "trigger_frame",
            0,
        )

    # --------------------------------------------------------
    # Sketch type
    # --------------------------------------------------------

    allowed_types = {
        "diagram",
        "comparison",
        "timeline",
        "cards",
        "concept",
    }

    if (
        revised.get(
            "sketch_type"
        )
        not in allowed_types
    ):

        revised[
            "sketch_type"
        ] = "diagram"

    # --------------------------------------------------------
    # Text 40 chars
    # --------------------------------------------------------

    text = str(
        revised.get(
            "on_screen_text",
            "",
        )
    ).strip()

    if len(text) > 40:

        revised[
            "on_screen_text"
        ] = (
            text[:39]
            .rstrip()
            + "…"
        )

    # --------------------------------------------------------
    # Audit
    # --------------------------------------------------------

    revised[
        "audit"
    ] = audit_scene(
        revised,
        narration,
    )

    return revised