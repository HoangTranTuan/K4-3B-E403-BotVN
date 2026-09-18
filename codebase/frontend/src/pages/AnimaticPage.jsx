import { useEffect, useMemo, useState } from "react";
import { ChevronLeft, ChevronRight, Pause, Play, RotateCcw } from "lucide-react";
import SceneSketch from "../lib/sceneSketch";

export default function AnimaticPage({ scenes, onReview }) {
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(0);

  const scene = scenes[index];
  const durationMs = useMemo(() => {
    const frames = Number(scene?.soFrame || 180);
    return Math.max(2500, Math.min(8000, (frames / 30) * 1000));
  }, [scene]);

  useEffect(() => {
    setProgress(0);
    if (!playing || !scene) return;

    const tick = 100;
    const step = (tick / durationMs) * 100;
    const timer = setInterval(() => {
      setProgress((p) => {
        const next = p + step;
        if (next >= 100) {
          if (index < scenes.length - 1) {
            setIndex((x) => x + 1);
            return 0;
          }
          setPlaying(false);
          return 100;
        }
        return next;
      });
    }, tick);

    return () => clearInterval(timer);
  }, [playing, index, scene, durationMs, scenes.length]);

  if (!scene) {
    return <section className="mx-auto max-w-[1500px] px-4 py-12 lg:px-8"><div className="panel p-16 text-center text-slate-500">Chưa có storyboard để xem Animatic.</div></section>;
  }

  const prev = () => { setPlaying(false); setProgress(0); setIndex((i) => Math.max(0, i - 1)); };
  const next = () => { setPlaying(false); setProgress(0); setIndex((i) => Math.min(scenes.length - 1, i + 1)); };
  const reset = () => { setPlaying(false); setIndex(0); setProgress(0); };

  return (
    <section className="mx-auto max-w-[1300px] px-4 py-7 lg:px-8">
      <div className="mb-5 text-center"><div className="eyebrow">BƯỚC 3 · XEM THỬ ANIMATIC</div><h1 className="mt-2 text-2xl font-black text-white">Preview nhịp cảnh trước khi render video thật</h1><p className="mt-1 text-sm text-slate-500">Đây là animatic nhẹ: phát lần lượt storyboard theo thời lượng ước tính từ frame count.</p></div>

      <div className="panel-strong p-4">
        <div className="mb-3 flex flex-wrap items-center justify-between gap-2 text-xs"><div className="font-bold text-slate-200"><span className="mr-2 inline-block h-2 w-2 rounded-full bg-rose-400" />Đang xem: Cảnh {String(scene.n).padStart(2, "0")} · {index + 1}/{scenes.length}</div><div className="chip">1920×1080 · 30fps</div></div>
        <SceneSketch scene={scene} large cinematic />

        <div className="mt-4 rounded-xl border border-slate-800 bg-[#060c17] p-4">
          <div className="h-2 overflow-hidden rounded-full bg-slate-800"><div className="h-full rounded-full bg-gradient-to-r from-indigo-500 via-violet-500 to-fuchsia-500 transition-all" style={{ width: `${progress}%` }} /></div>
          <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
            <div className="flex gap-2"><button className="btn-secondary !px-3" onClick={prev} disabled={index === 0}><ChevronLeft size={16} /> Cảnh trước</button><button className="btn-primary !px-5" onClick={() => setPlaying((v) => !v)}>{playing ? <Pause size={16} /> : <Play size={16} />}{playing ? "Tạm dừng" : "Tiếp tục"}</button><button className="btn-secondary !px-3" onClick={next} disabled={index === scenes.length - 1}>Cảnh sau <ChevronRight size={16} /></button></div>
            <div className="flex gap-2"><button className="btn-ghost !px-3" onClick={reset}><RotateCcw size={15} /> Reset</button><button className="btn-ghost !px-3" onClick={() => onReview(scene.n)}>Review cảnh này</button></div>
          </div>
        </div>
      </div>
    </section>
  );
}
