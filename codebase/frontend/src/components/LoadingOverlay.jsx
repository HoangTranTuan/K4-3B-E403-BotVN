import { CheckCircle2, Sparkles } from "lucide-react";

export default function LoadingOverlay({ open, title = "StoryboardAI đang xử lý", subtitle }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[100] grid place-items-center bg-[#030711]/80 px-5 backdrop-blur-md">
      <div className="w-full max-w-lg rounded-3xl border border-indigo-500/20 bg-[#0b1422] p-8 shadow-2xl shadow-black/50">
        <div className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-gradient-to-br from-indigo-500 via-violet-500 to-fuchsia-500 shadow-glow">
          <Sparkles className="animate-pulse" />
        </div>
        <h3 className="mt-5 text-center text-xl font-black text-white">{title}</h3>
        <p className="mt-2 text-center text-sm text-slate-500">{subtitle || "Gemini đang phân tích narration và dựng concept art plan."}</p>
        <div className="mt-6 space-y-3 rounded-2xl border border-slate-800 bg-[#060c17] p-4 text-xs">
          <div className="flex items-center gap-2 text-emerald-400"><CheckCircle2 size={14} /> Đọc narration</div>
          <div className="flex items-center gap-2 text-emerald-400"><CheckCircle2 size={14} /> Tách teaching intent</div>
          <div className="flex items-center gap-2 text-indigo-300"><span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-indigo-300/20 border-t-indigo-300" /> Tạo visual plan + timing + consistency…</div>
        </div>
      </div>
    </div>
  );
}
