import { CheckCircle2, RefreshCw, WandSparkles } from "lucide-react";
import SceneCard from "../components/SceneCard";

export default function StoryboardStudioPage({ scenes, approved, edited, onOpen, onRegenerate, onAnimatic }) {
  const passed = scenes.filter((s) => s?.audit?.passed).length;

  return (
    <section className="mx-auto max-w-[1500px] px-4 py-7 lg:px-8">
      <div className="mb-5 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <div className="eyebrow">BƯỚC 2 · BẢNG DUYỆT STORYBOARD</div>
          <h1 className="mt-2 text-2xl font-black tracking-tight text-white">Duyệt toàn bộ visual plan trước khi dựng cảnh thật</h1>
          <p className="mt-1 text-sm text-slate-500">Mỗi card là một scene độc lập, có sketch, timing, rule-check và consistency key.</p>
        </div>
        <div className="flex gap-2">
          <button className="btn-secondary" onClick={onRegenerate}><RefreshCw size={16} /> Tạo lại</button>
          <button className="btn-primary" onClick={onAnimatic}><WandSparkles size={16} /> Xem Animatic</button>
        </div>
      </div>

      <div className="mb-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <Stat label="Tổng cảnh" value={scenes.length} />
        <Stat label="Rule-check đạt" value={`${passed}/${scenes.length}`} tone="text-emerald-300" />
        <Stat label="Đã duyệt" value={approved.size} tone="text-sky-300" />
        <Stat label="Đã chỉnh" value={edited.size} tone="text-violet-300" />
      </div>

      {!scenes.length ? (
        <div className="panel p-16 text-center text-sm text-slate-500">Chưa có storyboard. Quay lại Bước 1 và bấm “Dựng Storyboard bằng AI”.</div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
          {scenes.map((scene) => <SceneCard key={scene.n} scene={scene} approved={approved.has(scene.n)} edited={edited.has(scene.n)} onOpen={onOpen} />)}
        </div>
      )}
    </section>
  );
}

function Stat({ label, value, tone = "text-white" }) {
  return <div className="panel p-4"><div className="text-[10px] font-bold uppercase tracking-wider text-slate-600">{label}</div><div className={`mt-1 text-3xl font-black ${tone}`}>{value}</div></div>;
}
