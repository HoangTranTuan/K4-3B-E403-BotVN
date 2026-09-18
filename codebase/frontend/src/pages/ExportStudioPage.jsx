import { CheckCircle2, Download, FileJson2, ShieldCheck } from "lucide-react";

export default function ExportStudioPage({ scenes, approved, edited, exportJson }) {
  const passed = scenes.filter((s) => s?.audit?.passed).length;
  return (
    <section className="mx-auto max-w-[1250px] px-4 py-7 lg:px-8">
      <div className="mb-5 text-center"><div className="eyebrow">BƯỚC 4 · BÀN GIAO</div><h1 className="mt-2 text-2xl font-black text-white">Delivery Package</h1><p className="mt-1 text-sm text-slate-500">Bàn giao storyboard JSON cùng trạng thái review để tiếp tục dựng video hoặc đưa cho coding agent.</p></div>

      <div className="grid gap-3 sm:grid-cols-4"><Stat label="Scene" value={scenes.length} /><Stat label="Rule-check" value={`${passed}/${scenes.length}`} tone="text-emerald-300" /><Stat label="Approved" value={approved.size} tone="text-sky-300" /><Stat label="Edited" value={edited.size} tone="text-violet-300" /></div>

      <div className="panel-strong mt-5 overflow-hidden">
        <div className="flex items-center gap-3 border-b border-slate-800 p-5"><div className="grid h-11 w-11 place-items-center rounded-xl bg-indigo-500/10 text-indigo-300"><FileJson2 size={20} /></div><div><h2 className="font-black text-white">storyboard-output.json</h2><p className="mt-1 text-xs text-slate-500">Visual plan · timing · consistency · audit · human review</p></div></div>
        <div className="grid gap-5 p-5 lg:grid-cols-[1fr_340px]">
          <div className="rounded-xl border border-slate-800 bg-[#060c17] p-4 font-mono text-xs leading-6 text-slate-500"><div>{"{"}</div><div className="pl-4"><span className="text-violet-300">"schema"</span>: "botvn-storyboard/1",</div><div className="pl-4"><span className="text-violet-300">"scenes"</span>: [{scenes.length} scene objects],</div><div className="pl-4"><span className="text-violet-300">"approved_scenes"</span>: [{[...approved].join(", ")}],</div><div className="pl-4"><span className="text-violet-300">"edited_scenes"</span>: [{[...edited].join(", ")}]</div><div>{"}"}</div></div>
          <div className="flex flex-col justify-between rounded-xl border border-emerald-500/15 bg-emerald-500/5 p-5"><div><ShieldCheck className="text-emerald-400" /><h3 className="mt-3 font-black text-white">Ready for handoff</h3><p className="mt-2 text-xs leading-5 text-slate-500">Có thể dùng JSON này cho pipeline dựng video, editor hoặc một agent khác.</p></div><button className="btn-primary mt-6" disabled={!scenes.length} onClick={exportJson}><Download size={16} /> Download JSON</button></div>
        </div>
      </div>
    </section>
  );
}

function Stat({ label, value, tone = "text-white" }) { return <div className="panel p-4"><div className="text-[10px] font-bold uppercase tracking-wider text-slate-600">{label}</div><div className={`mt-1 text-3xl font-black ${tone}`}>{value}</div></div>; }
