import { Clapperboard, CircleDot, Sparkles } from "lucide-react";

const steps = [
  ["input", "1", "Nạp Kịch Bản"],
  ["board", "2", "Bảng Duyệt Storyboard"],
  ["animatic", "3", "Xem Thử Animatic"],
  ["export", "4", "Bàn Giao"]
];

export default function StudioHeader({ page, setPage, health }) {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-700/60 bg-[#091321]/95 backdrop-blur-xl">
      <div className="mx-auto flex max-w-[1600px] items-center gap-4 px-4 py-3 lg:px-8">
        <div className="flex min-w-[260px] items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-indigo-500 via-violet-500 to-fuchsia-500 font-black shadow-glow">
            S4
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <div className="truncate text-sm font-black text-white">K4-3B-E403-BOTVN</div>
              <span className="hidden rounded-full border border-emerald-500/20 bg-emerald-500/10 px-2 py-0.5 text-[9px] font-bold text-emerald-300 xl:inline">CONCEPT ART ENGINE</span>
            </div>
            <div className="truncate text-[10px] text-slate-500">StoryboardAI · Track C · Lesson Studio · Đề C4</div>
          </div>
        </div>

        <nav className="mx-auto hidden rounded-2xl border border-slate-700/60 bg-[#060c17] p-1 md:flex">
          {steps.map(([id, number, label]) => {
            const active = page === id;
            return (
              <button
                key={id}
                onClick={() => setPage(id)}
                className={`flex min-w-[145px] items-center justify-center gap-2 rounded-xl px-3 py-2 text-xs font-bold transition ${active ? "bg-gradient-to-r from-indigo-500 to-violet-600 text-white shadow-lg shadow-indigo-950/30" : "text-slate-500 hover:bg-slate-900 hover:text-slate-200"}`}
              >
                <span className={`grid h-5 w-5 place-items-center rounded-full text-[10px] ${active ? "bg-white/15" : "bg-slate-800 text-slate-500"}`}>{number}</span>
                <span>{label}</span>
              </button>
            );
          })}
        </nav>

        <div className="ml-auto flex items-center gap-2 rounded-xl border border-slate-700 bg-slate-900/70 px-3 py-2">
          <CircleDot size={12} fill="currentColor" className={health?.gemini_configured ? "text-emerald-400" : "text-rose-400"} />
          <div>
            <div className="text-[9px] uppercase tracking-wide text-slate-600">AI Director</div>
            <div className="text-[10px] font-mono font-bold text-indigo-200">{health?.gemini_configured ? "gemini ready" : "not configured"}</div>
          </div>
        </div>
      </div>
    </header>
  );
}
