import { useMemo, useState } from "react";
import { AlertTriangle, Check, Clock3, Link2, WandSparkles } from "lucide-react";
import SceneSketch from "../lib/sceneSketch";

export default function ReviewStudioPage({ scenes, selectedSceneId, setSelectedSceneId, onApprove, onRevise, loading }) {
  const [feedback, setFeedback] = useState("");
  const scene = useMemo(() => scenes.find((s) => Number(s.n) === Number(selectedSceneId)), [scenes, selectedSceneId]);

  if (!scene) {
    return (
      <section className="mx-auto max-w-[1500px] px-4 py-7 lg:px-8">
        <div className="eyebrow">REVIEW · GRANULAR EDIT</div>
        <div className="panel mt-5 p-16 text-center"><WandSparkles className="mx-auto text-indigo-400" /><h2 className="mt-4 font-black text-white">Chưa chọn Scene</h2><p className="mt-1 text-sm text-slate-500">Chọn một scene ở Bảng Duyệt để xem chi tiết và sửa riêng scene đó.</p></div>
      </section>
    );
  }

  const issues = scene?.audit?.issues || [];
  const submit = async () => { await onRevise(scene, feedback); setFeedback(""); };

  return (
    <section className="mx-auto max-w-[1500px] px-4 py-7 lg:px-8">
      <div className="mb-5">
        <div className="eyebrow">GRANULAR EDIT · HUMAN IN THE LOOP</div>
        <h1 className="mt-2 text-2xl font-black text-white">Duyệt Cảnh {String(scene.n).padStart(2, "0")}</h1>
        <p className="mt-1 text-sm text-slate-500">AI chỉ regenerate đúng scene này; narration và các scene còn lại được giữ nguyên.</p>
      </div>

      <div className="grid gap-5 xl:grid-cols-[1.18fr_.82fr]">
        <div>
          <SceneSketch scene={scene} large cinematic />
          <div className="mt-4 flex flex-wrap gap-2">{scenes.map((s) => <button key={s.n} onClick={() => setSelectedSceneId(s.n)} className={`chip ${Number(s.n) === Number(scene.n) ? "border-indigo-400/40 bg-indigo-500/10 text-indigo-200" : "hover:border-slate-600"}`}>{String(s.n).padStart(2, "0")}</button>)}</div>
        </div>

        <div className="panel-strong p-5">
          <div className="flex items-start justify-between gap-3 border-b border-slate-800 pb-4">
            <div><div className="eyebrow">SCENE {scene.n}</div><div className="mt-1 text-xs text-slate-500">{scene.batDau || "—"} → {scene.ketThuc || "—"}</div></div>
            <span className={`chip ${scene?.audit?.passed ? "border-emerald-500/20 bg-emerald-500/10 text-emerald-300" : "border-amber-500/20 bg-amber-500/10 text-amber-300"}`}>{scene?.audit?.passed ? <Check size={12} /> : <AlertTriangle size={12} />}{scene?.audit?.passed ? "Rule-check đạt" : "Cần review"}</span>
          </div>

          <Info label="Lời đọc" value={scene.narration} />
          <Info label="Ý cần truyền đạt" value={scene.teaching_intent} />
          <Info label="Visual Plan" value={scene.visual_description} />
          <Info label="On-screen text" value={scene.on_screen_text} code />

          <div className="grid grid-cols-2 gap-3"><Mini icon={Clock3} label="Trigger frame" value={scene.trigger_frame ?? 0} /><Mini icon={Link2} label="Consistency" value={scene.consistency_key || "—"} /></div>

          {!!issues.length && <div className="mt-4 rounded-xl border border-amber-500/20 bg-amber-500/5 p-3"><div className="text-xs font-bold text-amber-300">Rule-check</div><ul className="mt-2 space-y-1 text-[11px] leading-5 text-amber-100/60">{issues.map((x) => <li key={x}>• {x}</li>)}</ul></div>}

          <textarea className="field mt-5 min-h-28 resize-y" placeholder="Ví dụ: Đơn giản hóa hình, bỏ nhân vật, giữ nguyên teaching intent và chữ." value={feedback} onChange={(e) => setFeedback(e.target.value)} />
          <div className="mt-3 grid gap-2 sm:grid-cols-2"><button className="btn-secondary !border-emerald-500/20 !text-emerald-300" onClick={() => onApprove(scene.n)}><Check size={16} /> Duyệt Scene</button><button className="btn-primary" disabled={!feedback.trim() || loading} onClick={submit}><WandSparkles size={16} /> AI sửa Scene này</button></div>
        </div>
      </div>
    </section>
  );
}

function Info({ label, value, code }) { return <div className="mt-4"><div className="text-[10px] font-black uppercase tracking-wider text-slate-600">{label}</div>{code ? <div className="mt-2 inline-block rounded-lg border border-indigo-500/20 bg-indigo-500/10 px-3 py-2 text-sm font-bold text-indigo-200">{value || "—"}</div> : <p className="mt-1 text-sm leading-6 text-slate-300">{value || "—"}</p>}</div>; }
function Mini({ icon: Icon, label, value }) { return <div className="mt-4 rounded-xl border border-slate-800 bg-[#070d18] p-3"><div className="flex items-center gap-1.5 text-[10px] uppercase tracking-wide text-slate-600"><Icon size={12} />{label}</div><div className="mt-1 truncate text-xs font-bold text-slate-300">{value}</div></div>; }
