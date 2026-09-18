import html
import textwrap


def _safe(value):
    return html.escape(str(value or ""))


def _wrap(text, width=34):
    return textwrap.wrap(str(text or ""), width=width)[:4]


def _text_lines(lines, x, y, size=24, gap=32, anchor="middle"):
    result = []

    for index, line in enumerate(lines):
        result.append(
            f'''
            <text
                x="{x}"
                y="{y + index * gap}"
                text-anchor="{anchor}"
                font-size="{size}"
                font-family="Arial, sans-serif"
                fill="#e2e8f0"
            >
                {_safe(line)}
            </text>
            '''
        )

    return "\n".join(result)


def render_scene_sketch(scene):
    """
    Sinh ảnh phác 16:9 bằng SVG.
    Không gọi AI image generation -> nhanh, miễn phí, dễ demo.
    """

    sketch_type = scene.get("sketch_type", "diagram")
    title = scene.get("on_screen_text", "")
    visual = scene.get("visual_description", "")
    scene_id = scene.get("n", "?")

    visual_lines = _wrap(visual, 42)

    body = ""

    # ---------------------------------------------------------
    # Comparison
    # ---------------------------------------------------------
    if sketch_type == "comparison":
        body = """
        <rect x="180" y="300" width="550" height="350"
              rx="30" fill="#172554" stroke="#60a5fa"
              stroke-width="5"/>

        <rect x="1190" y="300" width="550" height="350"
              rx="30" fill="#3b0764" stroke="#c084fc"
              stroke-width="5"/>

        <path d="M760 475 L1160 475"
              stroke="#94a3b8"
              stroke-width="8"
              stroke-dasharray="18 14"/>

        <text x="455" y="485"
              text-anchor="middle"
              fill="#93c5fd"
              font-size="34">A</text>

        <text x="1465" y="485"
              text-anchor="middle"
              fill="#d8b4fe"
              font-size="34">B</text>
        """

    # ---------------------------------------------------------
    # Timeline
    # ---------------------------------------------------------
    elif sketch_type == "timeline":
        body = """
        <line x1="300" y1="500"
              x2="1620" y2="500"
              stroke="#64748b"
              stroke-width="10"/>

        <circle cx="420" cy="500" r="60"
                fill="#1e3a8a"
                stroke="#60a5fa"
                stroke-width="5"/>

        <circle cx="960" cy="500" r="60"
                fill="#4c1d95"
                stroke="#c084fc"
                stroke-width="5"/>

        <circle cx="1500" cy="500" r="60"
                fill="#14532d"
                stroke="#4ade80"
                stroke-width="5"/>

        <text x="420" y="515"
              text-anchor="middle"
              fill="white"
              font-size="30">1</text>

        <text x="960" y="515"
              text-anchor="middle"
              fill="white"
              font-size="30">2</text>

        <text x="1500" y="515"
              text-anchor="middle"
              fill="white"
              font-size="30">3</text>
        """

    # ---------------------------------------------------------
    # Cards
    # ---------------------------------------------------------
    elif sketch_type == "cards":
        card_positions = [210, 710, 1210]

        for i, x in enumerate(card_positions, start=1):
            body += f"""
            <rect x="{x}" y="315"
                  width="400" height="300"
                  rx="28"
                  fill="#172033"
                  stroke="#64748b"
                  stroke-width="4"/>

            <text x="{x + 200}"
                  y="480"
                  text-anchor="middle"
                  fill="#cbd5e1"
                  font-size="30">
                  Thẻ {i}
            </text>
            """

    # ---------------------------------------------------------
    # Concept
    # ---------------------------------------------------------
    elif sketch_type == "concept":
        body = """
        <circle cx="960" cy="480" r="130"
                fill="#312e81"
                stroke="#818cf8"
                stroke-width="6"/>

        <circle cx="480" cy="380" r="80"
                fill="#172554"
                stroke="#60a5fa"
                stroke-width="5"/>

        <circle cx="1440" cy="380" r="80"
                fill="#14532d"
                stroke="#4ade80"
                stroke-width="5"/>

        <circle cx="960" cy="720" r="80"
                fill="#713f12"
                stroke="#fbbf24"
                stroke-width="5"/>

        <line x1="560" y1="400"
              x2="830" y2="455"
              stroke="#64748b"
              stroke-width="5"/>

        <line x1="1360" y1="400"
              x2="1090" y2="455"
              stroke="#64748b"
              stroke-width="5"/>

        <line x1="960" y1="610"
              x2="960" y2="640"
              stroke="#64748b"
              stroke-width="5"/>

        <text x="960" y="495"
              text-anchor="middle"
              fill="white"
              font-size="34">
              Ý chính
        </text>
        """

    # ---------------------------------------------------------
    # Default Diagram
    # ---------------------------------------------------------
    else:
        body = """
        <rect x="240" y="350"
              width="470" height="280"
              rx="30"
              fill="#172554"
              stroke="#60a5fa"
              stroke-width="5"/>

        <rect x="1210" y="350"
              width="470" height="280"
              rx="30"
              fill="#14532d"
              stroke="#4ade80"
              stroke-width="5"/>

        <line x1="750" y1="490"
              x2="1160" y2="490"
              stroke="#cbd5e1"
              stroke-width="8"/>

        <polygon points="1160,490 1100,455 1100,525"
                 fill="#cbd5e1"/>

        <text x="475" y="500"
              text-anchor="middle"
              fill="#93c5fd"
              font-size="32">
              Đầu vào
        </text>

        <text x="1445" y="500"
              text-anchor="middle"
              fill="#86efac"
              font-size="32">
              Kết quả
        </text>
        """

    description = _text_lines(
        visual_lines,
        x=960,
        y=760,
        size=24,
        gap=30
    )

    svg = f"""
    <div style="
        width:100%;
        background:#020617;
        border:1px solid #334155;
        border-radius:16px;
        overflow:hidden;
    ">
        <svg viewBox="0 0 1920 1080"
             width="100%"
             xmlns="http://www.w3.org/2000/svg">

            <rect width="1920"
                  height="1080"
                  fill="#020617"/>

            <!-- Vùng HUD -->
            <rect x="0" y="0"
                  width="1920"
                  height="250"
                  fill="#0f172a"/>

            <!-- Safe zone -->
            <rect x="80" y="250"
                  width="1760"
                  height="710"
                  fill="none"
                  stroke="#334155"
                  stroke-width="4"
                  stroke-dasharray="14 12"/>

            <!-- Subtitle zone -->
            <rect x="0" y="960"
                  width="1920"
                  height="120"
                  fill="#1e293b"/>

            <text x="90"
                  y="90"
                  fill="#64748b"
                  font-size="28">
                  SCENE {_safe(scene_id)}
            </text>

            <text x="960"
                  y="170"
                  text-anchor="middle"
                  fill="#f8fafc"
                  font-size="46"
                  font-weight="700">
                  {_safe(title)}
            </text>

            {body}

            {description}

            <text x="960"
                  y="1030"
                  text-anchor="middle"
                  fill="#64748b"
                  font-size="24">
                  Vùng phụ đề
            </text>

        </svg>
    </div>
    """

    return svg