import React from "react";

const colors = {
  data: { fill: "#0f2e58", stroke: "#38bdf8" },
  ai: { fill: "#34206b", stroke: "#a78bfa" },
  output: { fill: "#123d32", stroke: "#34d399" },
  warn: { fill: "#4a3210", stroke: "#fbbf24" }
};

function Card({ x, y, w, h, palette, label }) {
  const c = colors[palette];
  return (
    <g>
      <rect x={x} y={y} width={w} height={h} rx="28" fill={c.fill} stroke={c.stroke} strokeWidth="4" />
      <text x={x + w / 2} y={y + h / 2 + 9} textAnchor="middle" fill="#e5e7eb" fontSize="28" fontWeight="700">
        {label}
      </text>
    </g>
  );
}

export default function SceneSketch({ scene, large = false, cinematic = false }) {
  const type = scene?.sketch_type || "diagram";
  const title = scene?.on_screen_text || "Storyboard Preview";
  const narration = scene?.narration || "";

  let visual;
  if (type === "comparison") {
    visual = (
      <>
        <Card x={120} y={220} w={420} h={250} palette="data" label="Phương án A" />
        <Card x={660} y={220} w={420} h={250} palette="ai" label="Phương án B" />
        <line x1="560" y1="345" x2="640" y2="345" stroke="#64748b" strokeWidth="6" strokeDasharray="12 10" />
      </>
    );
  } else if (type === "timeline") {
    visual = (
      <>
        <line x1="170" y1="355" x2="1030" y2="355" stroke="#475569" strokeWidth="9" />
        {[270, 600, 930].map((x, i) => (
          <g key={x}>
            <circle cx={x} cy="355" r="54" fill={["#123a67", "#3c2378", "#164335"][i]} stroke={["#38bdf8", "#a78bfa", "#34d399"][i]} strokeWidth="4" />
            <text x={x} y="366" textAnchor="middle" fill="white" fontSize="28" fontWeight="700">{i + 1}</text>
          </g>
        ))}
      </>
    );
  } else if (type === "cards") {
    visual = (
      <>
        <Card x={120} y={220} w={285} h={250} palette="data" label="Khối 1" />
        <Card x={458} y={220} w={285} h={250} palette="ai" label="Khối 2" />
        <Card x={795} y={220} w={285} h={250} palette="output" label="Khối 3" />
      </>
    );
  } else if (type === "concept") {
    visual = (
      <>
        <circle cx="600" cy="350" r="108" fill="#30216b" stroke="#a78bfa" strokeWidth="5" />
        <text x="600" y="360" textAnchor="middle" fill="white" fontSize="28" fontWeight="700">Ý chính</text>
        <circle cx="255" cy="350" r="60" fill="#123a67" stroke="#38bdf8" strokeWidth="4" />
        <circle cx="945" cy="350" r="60" fill="#164335" stroke="#34d399" strokeWidth="4" />
        <line x1="318" y1="350" x2="488" y2="350" stroke="#64748b" strokeWidth="5" />
        <line x1="712" y1="350" x2="882" y2="350" stroke="#64748b" strokeWidth="5" />
      </>
    );
  } else {
    visual = (
      <>
        <Card x={125} y={220} w={355} h={250} palette="data" label="Đầu vào" />
        <Card x={720} y={220} w={355} h={250} palette="output" label="Kết quả" />
        <rect x="512" y="276" width="176" height="138" rx="69" fill="#2f1d66" stroke="#a78bfa" strokeWidth="5" />
        <text x="600" y="355" textAnchor="middle" fill="white" fontSize="28" fontWeight="800">AI</text>
        <line x1="485" y1="345" x2="508" y2="345" stroke="#cbd5e1" strokeWidth="7" />
        <line x1="692" y1="345" x2="716" y2="345" stroke="#cbd5e1" strokeWidth="7" />
      </>
    );
  }

  return (
    <div className={`overflow-hidden rounded-2xl border border-slate-700/70 bg-[#030711] ${large ? "shadow-2xl shadow-black/40" : ""} ${cinematic ? "animatic-glow" : ""}`}>
      <svg viewBox="0 0 1200 675" className="block w-full">
        <defs>
          <linearGradient id={`bg-${scene?.n}`} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#07111f" />
            <stop offset="45%" stopColor="#07101b" />
            <stop offset="100%" stopColor="#0a1422" />
          </linearGradient>
          <radialGradient id={`light-${scene?.n}`} cx="50%" cy="32%" r="70%">
            <stop offset="0%" stopColor="#143055" stopOpacity=".62" />
            <stop offset="100%" stopColor="#030711" stopOpacity="0" />
          </radialGradient>
        </defs>
        <rect width="1200" height="675" fill={`url(#bg-${scene?.n})`} />
        <rect width="1200" height="675" fill={`url(#light-${scene?.n})`} />
        <rect x="46" y="118" width="1108" height="474" rx="22" fill="none" stroke="#22304a" strokeWidth="3" strokeDasharray="12 10" />
        <text x="58" y="48" fill="#64748b" fontSize="18" fontWeight="700">SCENE {scene?.n ?? "—"}</text>
        <text x="600" y="92" textAnchor="middle" fill="#f8fafc" fontSize="31" fontWeight="800">{title}</text>
        {visual}
        <rect x="0" y="610" width="1200" height="65" fill="#0b1422" />
        <text x="600" y="650" textAnchor="middle" fill="#facc15" fontSize="18" fontWeight="700">
          {narration.length > 72 ? `${narration.slice(0, 72)}…` : narration}
        </text>
      </svg>
    </div>
  );
}
