import { Database, FileUp, Sparkles, ShieldCheck, Type, ScanLine, Wand2, Palette, Film } from "lucide-react";

function parseText(text) {
  return text
    .split(/\r?\n/)
    .map((x) => x.trim())
    .filter(Boolean)
    .map((loi, i) => ({
      n: i + 1,
      loi,
      chuoiMocTu: loi,
      mocTu: [],
      soFrame: Math.max(90, loi.split(/\s+/).length * 8)
    }));
}

export default function InputStudioPage({
  sentences,
  setSentences,
  sceneLimit,
  setSceneLimit,
  sampleMeta,
  loadSample,
  generate,
  stylebook,
  setStylebook,
  loading
}) {
  const text = sentences.map((x) => x.loi || "").join("\n");

  const onFile = async (file) => {
    if (!file) return;
    const raw = await file.text();
    const data = JSON.parse(raw);
    let items = [];
    if (Array.isArray(data?.cau)) items = data.cau;
    else if (Array.isArray(data?.sentences)) items = data.sentences;
    else if (Array.isArray(data)) items = data;
    setSentences(items.filter((x) => x?.loi));
  };

  return (
    <section className="mx-auto max-w-[1500px] px-4 py-7 lg:px-8">
      <div className="mb-5">
        <div className="eyebrow">BƯỚC 1 · NẠP KỊCH BẢN BÀI GIẢNG</div>
        <h1 className="mt-2 text-2xl font-black tracking-tight text-white">Từ narration thành kế hoạch hình ảnh có thể duyệt trước khi dựng video</h1>
        <p className="mt-1 text-sm text-slate-500">Dùng fixture thật của BTC, upload JSON hoặc dán từng câu. Hệ thống giữ Safe Zone, text ≤ 40 ký tự và grounding theo narration.</p>
      </div>

      <div className="grid gap-5 xl:grid-cols-[1.25fr_.75fr]">
        <div className="panel-strong p-5">
          <div className="flex flex-wrap items-start justify-between gap-3 border-b border-slate-800 pb-4">
            <div>
              <div className="flex items-center gap-2"><Film size={17} className="text-amber-400" /><h2 className="font-extrabold text-white">Nhập hoặc dán nội dung bài giảng</h2></div>
              <div className="mt-1 text-xs text-slate-500">{sentences.length} câu · AI tự tách ý sư phạm và tạo visual plan cho từng cảnh</div>
            </div>
            <div className="flex flex-wrap gap-2">
              <button className="btn-secondary !px-3 !py-2 text-xs" onClick={loadSample}><Database size={14} /> BTC sample</button>
              <label className="btn-secondary !cursor-pointer !px-3 !py-2 text-xs"><FileUp size={14} /> Upload JSON<input className="hidden" type="file" accept=".json" onChange={(e) => onFile(e.target.files?.[0])} /></label>
              <button className="btn-secondary !px-3 !py-2 text-xs" onClick={() => setSentences([])}>Clear</button>
            </div>
          </div>

          {sampleMeta?.title && (
            <div className="mt-4 rounded-xl border border-indigo-400/15 bg-indigo-400/5 px-4 py-3">
              <div className="text-xs font-extrabold text-indigo-200">{sampleMeta.title}</div>
              <div className="mt-1 text-xs leading-5 text-slate-500">{sampleMeta.objective}</div>
            </div>
          )}

          <textarea
            className="field mt-4 min-h-[360px] resize-y leading-7"
            value={text}
            placeholder={"Mỗi dòng là một câu lời đọc…\nVí dụ: Mô hình chia văn bản thành các token."}
            onChange={(e) => setSentences(parseText(e.target.value))}
          />

          <div className="mt-4 grid gap-3 rounded-xl border border-slate-800 bg-[#080f1b] p-3 sm:grid-cols-3">
            <Info icon={ScanLine} label="Safe Zone" value="x:80–1840 · y:250–960" tone="text-emerald-300" />
            <Info icon={Type} label="On-screen text" value="≤ 40 ký tự" tone="text-amber-300" />
            <Info icon={ShieldCheck} label="Grounding" value="Không tự thêm fact/số" tone="text-sky-300" />
          </div>

          <div className="mt-4 flex flex-col gap-4 border-t border-slate-800 pt-4 sm:flex-row sm:items-end sm:justify-between">
            <label className="block">
              <span className="mb-1 block text-[11px] font-bold uppercase tracking-wide text-slate-500">Scene MVP</span>
              <input type="number" min="1" max={Math.max(1, Math.min(12, sentences.length || 12))} value={sceneLimit} onChange={(e) => setSceneLimit(Number(e.target.value))} className="field !w-24" />
            </label>

            <button className="btn-primary min-w-[330px] !py-3.5 text-sm" disabled={!sentences.length || loading} onClick={generate}><Sparkles size={18} /> DỰNG STORYBOARD BẰNG AI THẬT</button>
          </div>
        </div>

        <aside className="panel-strong p-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div className="flex items-center gap-2"><Palette size={18} className="text-violet-400" /><h2 className="font-extrabold text-white">Sổ Quy Ước Hình Ảnh</h2></div>
            <span className="chip border-indigo-500/20 bg-indigo-500/10 text-indigo-300">Quy chuẩn chốt</span>
          </div>

          <div className="mt-4 space-y-3">
            <Rule title="1. ART DIRECTION" bullets={["Xanh dương = dữ liệu / input / token", "Tím = AI / mô hình / xử lý", "Xanh lá = output / kết quả"]} />
            <Rule title="2. TECHNICAL RULES" bullets={["Khung 1920×1080 · 30fps", "Text tối đa 40 ký tự", "Safe Zone và vùng subtitle cố định"]} />
            <Rule title="3. CONTENT GUARDRAILS" warning bullets={["Không thêm số liệu/tên riêng nếu narration không có", "Không dùng logo, người thật hoặc nhân vật có bản quyền", "Concept lặp lại phải giữ consistency key"]} />
          </div>

          <details className="mt-4 rounded-xl border border-slate-800 bg-[#070d18] p-3">
            <summary className="cursor-pointer text-xs font-bold text-slate-300">Chỉnh Stylebook chi tiết</summary>
            <textarea className="field mt-3 min-h-48 resize-y text-xs leading-5" value={stylebook} onChange={(e) => setStylebook(e.target.value)} />
          </details>

          <div className="mt-4 rounded-xl border border-indigo-500/15 bg-indigo-500/5 p-4">
            <div className="flex items-center gap-2 text-xs font-bold text-indigo-200"><Wand2 size={15} /> AI Director behavior</div>
            <p className="mt-2 text-[11px] leading-5 text-slate-500">Teaching intent được tách riêng khỏi cách vẽ; góp ý ở bước Review chỉ sửa đúng scene đang chọn.</p>
          </div>
        </aside>
      </div>
    </section>
  );
}

function Info({ icon: Icon, label, value, tone }) {
  return <div className="flex items-center gap-2"><Icon size={15} className={tone} /><div><div className="text-[10px] uppercase tracking-wide text-slate-600">{label}</div><div className={`mt-0.5 text-xs font-bold ${tone}`}>{value}</div></div></div>;
}

function Rule({ title, bullets, warning }) {
  return (
    <div className={`rule-card ${warning ? "border-rose-500/20" : ""}`}>
      <div className={`text-xs font-black ${warning ? "text-rose-300" : "text-indigo-300"}`}>{title}</div>
      <ul className="mt-2 space-y-1.5 text-[11px] leading-5 text-slate-500">{bullets.map((x) => <li key={x}>• {x}</li>)}</ul>
    </div>
  );
}
