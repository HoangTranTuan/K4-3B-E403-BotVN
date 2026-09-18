import { AlertTriangle, ArrowUpRight, CheckCircle2, Pencil, TimerReset } from "lucide-react";
import SceneSketch from "../lib/sceneSketch";

export default function SceneCard({ scene, approved, edited, onOpen }) {
  const passed = scene?.audit?.passed;
  return (
    <article className="group overflow-hidden rounded-2xl border border-slate-700/70 bg-[#0a1322] transition duration-200 hover:-translate-y-1 hover:border-indigo-400/40 hover:shadow-2xl hover:shadow-black/30">
      <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3">
        <div className="flex items-center gap-2">
          <span className="text-xs font-black tracking-wider text-slate-200">CẢNH {String(scene.n).padStart(2, "0")}</span>
          {edited && <span className="chip border-violet-500/20 bg-violet-500/10 text-violet-300"><Pencil size={11} /> Edited</span>}
        </div>
        <span className={`chip ${passed ? "border-emerald-500/20 bg-emerald-500/10 text-emerald-300" : "border-amber-500/20 bg-amber-500/10 text-amber-300"}`}>
          {passed ? <CheckCircle2 size={11} /> : <AlertTriangle size={11} />}
          {passed ? "Pass" : "Review"}
        </span>
      </div>

      <div className="p-3"><SceneSketch scene={scene} /></div>

      <div className="px-4 pb-4">
        <h3 className="line-clamp-1 text-base font-extrabold text-white">{scene.on_screen_text || "Storyboard Scene"}</h3>
        <p className="mt-2 line-clamp-2 min-h-10 text-xs leading-5 text-slate-500">{scene.visual_description}</p>
        <div className="mt-3 flex flex-wrap gap-2">
          <span className="chip"><TimerReset size={11} /> frame {scene.trigger_frame ?? 0}</span>
          {approved && <span className="chip border-emerald-500/20 bg-emerald-500/10 text-emerald-300">Approved</span>}
        </div>
        <div className="mt-4 flex items-center justify-between border-t border-slate-800 pt-3">
          <span className="max-w-[65%] truncate font-mono text-[10px] text-slate-600">{scene.consistency_key || "no-key"}</span>
          <button onClick={() => onOpen(scene.n)} className="flex items-center gap-1 text-xs font-extrabold text-indigo-300 hover:text-white">Duyệt cảnh <ArrowUpRight size={14} /></button>
        </div>
      </div>
    </article>
  );
}
