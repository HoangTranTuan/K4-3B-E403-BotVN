import json
import os
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from storyboard_agent import (
    DEFAULT_STYLEBOOK,
    generate_storyboard,
    revise_scene,
)

from sketch import render_scene_sketch


# ============================================================
# PATH
# ============================================================

APP_DIR = Path(__file__).resolve().parent

# storyboard_app -> codebase -> repo root
ROOT_DIR = APP_DIR.parent.parent

SAMPLE_FILE = (
    ROOT_DIR
    / "data"
    / "studio-pack"
    / "c4-storyboardai"
    / "vi-du"
    / "loi-doc-d1-2.json"
)

load_dotenv(ROOT_DIR / ".env")
load_dotenv(APP_DIR / ".env")


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="StoryboardAI",
    page_icon="🎬",
    layout="wide",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                rgba(79,70,229,.14),
                transparent 28%
            ),
            #020617;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    .hero {
        border: 1px solid #1e293b;
        background:
            linear-gradient(
                135deg,
                rgba(30,41,59,.92),
                rgba(15,23,42,.92)
            );
        border-radius: 22px;
        padding: 26px 30px;
        margin-bottom: 22px;
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        color: #f8fafc;
        margin: 0;
    }

    .hero-sub {
        color: #94a3b8;
        font-size: 15px;
        margin-top: 7px;
    }

    .step-chip {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        border: 1px solid #3730a3;
        color: #c7d2fe;
        background: #1e1b4b;
        font-size: 12px;
        margin-right: 6px;
        margin-top: 12px;
    }

    .scene-meta {
        padding: 10px 13px;
        border: 1px solid #1e293b;
        background: #0f172a;
        border-radius: 12px;
        font-size: 13px;
        color: #cbd5e1;
    }

    .good {
        color: #4ade80;
        font-weight: 700;
    }

    .bad {
        color: #fb7185;
        font-weight: 700;
    }

    div[data-testid="stMetric"] {
        background: #0f172a;
        border: 1px solid #1e293b;
        padding: 14px;
        border-radius: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "source_data": None,
    "scenes": [],
    "edit_log": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPERS
# ============================================================

def load_json_file(path):
    with open(
        path,
        "r",
        encoding="utf-8-sig",
    ) as f:
        return json.load(f)


def extract_sentences(data):
    if isinstance(data, dict):
        if isinstance(data.get("cau"), list):
            return [
                item
                for item in data["cau"]
                if item.get("loi")
            ]

        if isinstance(data.get("sentences"), list):
            return data["sentences"]

    if isinstance(data, list):
        return data

    return []


def text_to_sentences(text):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    result = []

    for index, line in enumerate(
        lines,
        start=1,
    ):
        result.append(
            {
                "n": index,
                "loi": line,
                "chuoiMocTu": line,
                "mocTu": [],
                "soFrame": max(
                    90,
                    len(line.split()) * 8,
                ),
            }
        )

    return result


def scene_by_number(number):
    for scene in st.session_state.scenes:
        if scene.get("n") == number:
            return scene

    return None


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            🎬 StoryboardAI
        </div>

        <div class="hero-sub">
            Agent dựng kế hoạch hình ảnh cho video bài giảng
            từ lời đọc đã chốt.
        </div>

        <span class="step-chip">
            1 · Nhập lời đọc
        </span>

        <span class="step-chip">
            2 · AI tạo Storyboard
        </span>

        <span class="step-chip">
            3 · Human Review
        </span>

        <span class="step-chip">
            4 · Export
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("⚙️ Cấu hình")

    env_key = os.getenv(
        "GEMINI_API_KEY",
        "",
    )

    api_key = st.text_input(
        "Gemini API Key",
        value=env_key,
        type="password",
        help=(
            "Có thể đặt trong .env bằng "
            "GEMINI_API_KEY=..."
        ),
    )

    st.divider()

    st.subheader("🎨 Sổ quy ước")

    stylebook = st.text_area(
        "Stylebook",
        value=DEFAULT_STYLEBOOK,
        height=360,
    )

    st.caption(
        "Giám khảo sẽ kiểm tra tính nhất quán "
        "dựa trên chính sổ quy ước này."
    )


# ============================================================
# STEP 1 - INPUT
# ============================================================

st.header("1. Nhập lời đọc bài giảng")

source_mode = st.radio(
    "Nguồn dữ liệu",
    [
        "Dữ liệu mẫu BTC",
        "Upload JSON",
        "Dán lời đọc",
    ],
    horizontal=True,
)

sentences = []


# ------------------------------------------------------------
# Sample
# ------------------------------------------------------------

if source_mode == "Dữ liệu mẫu BTC":
    if SAMPLE_FILE.exists():
        data = load_json_file(
            SAMPLE_FILE
        )

        st.session_state.source_data = data

        sentences = extract_sentences(
            data
        )

        st.success(
            f"Đã tìm thấy dữ liệu mẫu: "
            f"{len(sentences)} câu."
        )

        st.caption(
            str(SAMPLE_FILE.relative_to(ROOT_DIR))
        )

    else:
        st.error(
            "Không tìm thấy file dữ liệu mẫu."
        )


# ------------------------------------------------------------
# Upload
# ------------------------------------------------------------

elif source_mode == "Upload JSON":
    uploaded = st.file_uploader(
        "Chọn file JSON",
        type=["json"],
    )

    if uploaded:
        try:
            data = json.load(
                uploaded
            )

            st.session_state.source_data = data

            sentences = extract_sentences(
                data
            )

            st.success(
                f"Đã nạp {len(sentences)} câu."
            )

        except Exception as exc:
            st.error(
                f"Không đọc được JSON: {exc}"
            )


# ------------------------------------------------------------
# Paste text
# ------------------------------------------------------------

else:
    pasted_text = st.text_area(
        "Mỗi dòng là một câu lời đọc",
        height=220,
        placeholder=(
            "AI học từ dữ liệu để tạo dự đoán.\n"
            "Mỗi token là một mảnh văn bản..."
        ),
    )

    if pasted_text.strip():
        sentences = text_to_sentences(
            pasted_text
        )

        st.info(
            f"Đã nhận {len(sentences)} câu."
        )


# ============================================================
# SCENE LIMIT
# ============================================================

if sentences:
    max_limit = min(
        len(sentences),
        12,
    )

    default_limit = min(
        10,
        max_limit,
    )

    scene_limit = st.slider(
        "Số câu tạo trong MVP",
        min_value=1,
        max_value=max_limit,
        value=default_limit,
        help=(
            "Hackathon nên demo 10 câu trước "
            "để giảm thời gian và chi phí API."
        ),
    )

    selected_sentences = (
        sentences[:scene_limit]
    )

    with st.expander(
        "Xem lời đọc đầu vào"
    ):
        for item in selected_sentences:
            st.markdown(
                f"**Câu {item.get('n')}** — "
                f"{item.get('loi', '')}"
            )

    create_button = st.button(
        "✨ Tạo Storyboard bằng AI",
        type="primary",
        use_container_width=True,
    )

    if create_button:
        if not api_key:
            st.error(
                "Hãy nhập GEMINI_API_KEY trước."
            )

        else:
            try:
                with st.spinner(
                    "AI đang phân tích lời đọc và "
                    "tạo kế hoạch hình..."
                ):
                    scenes = generate_storyboard(
                        selected_sentences,
                        stylebook,
                        api_key,
                    )

                st.session_state.scenes = scenes
                st.session_state.edit_log = []

                st.success(
                    f"Đã tạo {len(scenes)} scene."
                )

            except Exception as exc:
                st.exception(exc)


# ============================================================
# STEP 2 - STORYBOARD
# ============================================================

if st.session_state.scenes:
    st.divider()

    st.header(
        "2. Storyboard Dashboard"
    )

    total = len(
        st.session_state.scenes
    )

    audit_pass = sum(
        1
        for scene
        in st.session_state.scenes
        if scene.get(
            "audit",
            {},
        ).get(
            "passed",
            False,
        )
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Scene",
        total,
    )

    col2.metric(
        "Qua rule-check",
        f"{audit_pass}/{total}",
    )

    col3.metric(
        "Đã sửa thủ công",
        len(st.session_state.edit_log),
    )

    st.caption(
        "Ảnh phác được dựng bằng SVG nên không tốn "
        "chi phí sinh ảnh."
    )

    scene_columns = st.columns(2)

    for index, scene in enumerate(
        st.session_state.scenes
    ):
        target_col = scene_columns[
            index % 2
        ]

        with target_col:
            with st.container(
                border=True
            ):
                st.subheader(
                    f"Scene {scene.get('n')}"
                )

                components.html(
                    render_scene_sketch(
                        scene
                    ),
                    height=345,
                    scrolling=False,
                )

                st.markdown(
                    f"""
                    **Lời đọc**

                    {scene.get("narration", "")}

                    **Ý cần truyền đạt**

                    {scene.get("teaching_intent", "")}

                    **Mô tả hình**

                    {scene.get("visual_description", "")}

                    **Chữ trên màn hình**

                    `{scene.get("on_screen_text", "")}`

                    **Trigger**

                    `{scene.get("trigger_phrase", "")}`
                    → frame `{scene.get("trigger_frame", 0)}`

                    **Consistency key**

                    `{scene.get("consistency_key", "")}`
                    """
                )

                audit = scene.get(
                    "audit",
                    {},
                )

                if audit.get("passed"):
                    st.success(
                        "✓ Rule-check đạt"
                    )

                else:
                    st.warning(
                        "Rule-check cần xem lại"
                    )

                    for issue in audit.get(
                        "issues",
                        [],
                    ):
                        st.caption(
                            f"• {issue}"
                        )


# ============================================================
# STEP 3 - HUMAN REVIEW
# ============================================================

if st.session_state.scenes:
    st.divider()

    st.header(
        "3. Human Review — sửa riêng 1 Scene"
    )

    scene_numbers = [
        scene.get("n")
        for scene
        in st.session_state.scenes
    ]

    selected_number = st.selectbox(
        "Chọn Scene cần review",
        scene_numbers,
    )

    selected_scene = scene_by_number(
        selected_number
    )

    if selected_scene:
        left, right = st.columns(
            [1, 1],
        )

        with left:
            components.html(
                render_scene_sketch(
                    selected_scene
                ),
                height=390,
            )

        with right:
            st.markdown(
                f"""
                ### Scene {selected_number}

                **Narration**

                {selected_scene.get("narration", "")}

                **Visual**

                {selected_scene.get("visual_description", "")}

                **On-screen text**

                `{selected_scene.get("on_screen_text", "")}`
                """
            )

            feedback = st.text_area(
                "Góp ý cho riêng Scene này",
                placeholder=(
                    "Ví dụ: Đơn giản hóa hình, "
                    "không dùng nhân vật. "
                    "Giữ nguyên ý và chữ."
                ),
                key=f"feedback_{selected_number}",
            )

            if st.button(
                "🔁 AI sửa riêng Scene này",
                type="primary",
            ):
                if not feedback.strip():
                    st.warning(
                        "Hãy nhập góp ý."
                    )

                elif not api_key:
                    st.error(
                        "Chưa có Gemini API Key."
                    )

                else:
                    try:
                        with st.spinner(
                            f"Đang sửa Scene "
                            f"{selected_number}..."
                        ):
                            revised = revise_scene(
                                selected_scene,
                                feedback,
                                stylebook,
                                api_key,
                            )

                        for index, scene in enumerate(
                            st.session_state.scenes
                        ):
                            if (
                                scene.get("n")
                                == selected_number
                            ):
                                st.session_state.scenes[
                                    index
                                ] = revised

                                break

                        st.session_state.edit_log.append(
                            {
                                "scene": selected_number,
                                "feedback": feedback,
                            }
                        )

                        st.success(
                            f"Đã cập nhật Scene "
                            f"{selected_number}. "
                            f"Các Scene khác giữ nguyên."
                        )

                        st.rerun()

                    except Exception as exc:
                        st.exception(exc)


# ============================================================
# STEP 4 - EXPORT
# ============================================================

if st.session_state.scenes:
    st.divider()

    st.header(
        "4. Export Storyboard"
    )

    output_payload = {
        "schema": "botvn-storyboard/1",
        "project": "C4 StoryboardAI",
        "frame": {
            "width": 1920,
            "height": 1080,
            "fps": 30,
            "safe_zone": {
                "x_min": 80,
                "x_max": 1840,
                "y_min": 250,
                "y_max": 960,
            },
            "max_on_screen_text_chars": 40,
        },
        "stylebook": stylebook,
        "scenes": st.session_state.scenes,
        "edit_log": st.session_state.edit_log,
    }

    output_json = json.dumps(
        output_payload,
        ensure_ascii=False,
        indent=2,
    )

    left, right = st.columns(
        [2, 1],
    )

    with left:
        st.code(
            output_json[:8000],
            language="json",
        )

    with right:
        st.download_button(
            "⬇️ Tải storyboard.json",
            data=output_json,
            file_name="storyboard-output.json",
            mime="application/json",
            use_container_width=True,
        )

        st.info(
            "Demo trọng tâm: nhập lời đọc → "
            "AI tạo storyboard → sửa riêng một scene "
            "→ export JSON."
        )