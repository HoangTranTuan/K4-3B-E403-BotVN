import { useEffect, useMemo, useState } from "react";
import { api } from "./api";
import StudioHeader from "./components/StudioHeader";
import LoadingOverlay from "./components/LoadingOverlay";
import InputStudioPage from "./pages/InputStudioPage";
import StoryboardStudioPage from "./pages/StoryboardStudioPage";
import ReviewStudioPage from "./pages/ReviewStudioPage";
import AnimaticPage from "./pages/AnimaticPage";
import ExportStudioPage from "./pages/ExportStudioPage";

export default function App() {
  const [page, setPage] = useState("input");
  const [health, setHealth] = useState(null);
  const [stylebook, setStylebook] = useState("");
  const [sentences, setSentences] = useState([]);
  const [sampleMeta, setSampleMeta] = useState(null);
  const [sceneLimit, setSceneLimit] = useState(10);
  const [scenes, setScenes] = useState([]);
  const [selectedSceneId, setSelectedSceneId] = useState(null);
  const [approved, setApproved] = useState(new Set());
  const [edited, setEdited] = useState(new Set());
  const [editLog, setEditLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingTitle, setLoadingTitle] = useState("");
  const [toast, setToast] = useState("");

  const sentenceMap = useMemo(() => new Map(sentences.map((s) => [Number(s.n), s])), [sentences]);

  useEffect(() => {
    const boot = async () => {
      try {
        const [healthData, styleData] = await Promise.all([api.health(), api.stylebook()]);
        setHealth(healthData);
        setStylebook(styleData.stylebook || "");
        await loadSample();
      } catch (error) {
        notify(error.message);
      }
    };
    boot();
  }, []);

  const notify = (message) => {
    setToast(message);
    window.clearTimeout(window.__storyboardToast);
    window.__storyboardToast = window.setTimeout(() => setToast(""), 3200);
  };

  const loadSample = async () => {
    try {
      setLoading(true);
      setLoadingTitle("Đang tải fixture của BTC…");
      const data = await api.sample();
      setSentences(data.sentences || []);
      setSampleMeta({ id: data.id, title: data.title, objective: data.objective });
      setSceneLimit(Math.min(10, data.sentences?.length || 10));
      notify(`Đã nạp ${data.count} câu từ fixture BTC.`);
    } catch (error) {
      notify(error.message);
    } finally {
      setLoading(false);
    }
  };

  const generate = async () => {
    const limit = Math.max(1, Math.min(Number(sceneLimit) || 10, 12, sentences.length));
    try {
      setLoading(true);
      setLoadingTitle("AI Director đang dựng Storyboard…");
      const data = await api.generate(sentences.slice(0, limit), stylebook);
      setScenes(data.scenes || []);
      setApproved(new Set());
      setEdited(new Set());
      setEditLog([]);
      setSelectedSceneId(null);
      setPage("board");
      notify(`Đã tạo ${data.count} scene.`);
    } catch (error) {
      notify(error.message);
    } finally {
      setLoading(false);
    }
  };

  const openScene = (id) => { setSelectedSceneId(id); setPage("review"); };
  const approveScene = (id) => { setApproved((prev) => new Set([...prev, id])); notify(`Scene ${id} đã được duyệt.`); };

  const reviseScene = async (scene, feedback) => {
    try {
      setLoading(true);
      setLoadingTitle(`AI đang sửa riêng Scene ${scene.n}…`);
      const originalSentence = sentenceMap.get(Number(scene.n)) || null;
      const data = await api.revise(scene, feedback, stylebook, originalSentence);
      const revised = data.scene;
      setScenes((prev) => prev.map((item) => (Number(item.n) === Number(revised.n) ? revised : item)));
      setEdited((prev) => new Set([...prev, revised.n]));
      setEditLog((prev) => [...prev, { scene: revised.n, feedback }]);
      setSelectedSceneId(revised.n);
      notify(`Đã sửa Scene ${revised.n}; các scene khác giữ nguyên.`);
    } catch (error) {
      notify(error.message);
    } finally {
      setLoading(false);
    }
  };

  const exportJson = () => {
    const payload = {
      schema: "botvn-storyboard/1",
      project: "C4 StoryboardAI",
      team: "K4-3B-E403-BOTVN",
      generated_at: new Date().toISOString(),
      frame: { width: 1920, height: 1080, fps: 30, max_on_screen_text_chars: 40 },
      stylebook,
      scenes,
      approved_scenes: [...approved],
      edited_scenes: [...edited],
      edit_log: editLog
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "storyboard-output.json";
    a.click();
    URL.revokeObjectURL(url);
    notify("Đã export storyboard-output.json");
  };

  return (
    <div className="min-h-screen">
      <StudioHeader page={page} setPage={setPage} health={health} />

      {page === "input" && <InputStudioPage sentences={sentences} setSentences={setSentences} sceneLimit={sceneLimit} setSceneLimit={setSceneLimit} sampleMeta={sampleMeta} loadSample={loadSample} generate={generate} stylebook={stylebook} setStylebook={setStylebook} loading={loading} />}
      {page === "board" && <StoryboardStudioPage scenes={scenes} approved={approved} edited={edited} onOpen={openScene} onRegenerate={generate} onAnimatic={() => setPage("animatic")} />}
      {page === "review" && <ReviewStudioPage scenes={scenes} selectedSceneId={selectedSceneId} setSelectedSceneId={setSelectedSceneId} onApprove={approveScene} onRevise={reviseScene} loading={loading} />}
      {page === "animatic" && <AnimaticPage scenes={scenes} onReview={openScene} />}
      {page === "export" && <ExportStudioPage scenes={scenes} approved={approved} edited={edited} exportJson={exportJson} />}

      <LoadingOverlay open={loading} title={loadingTitle} />
      {toast && <div className="fixed bottom-5 right-5 z-[120] max-w-md rounded-xl border border-slate-700 bg-[#0b1422] px-4 py-3 text-sm text-slate-200 shadow-2xl shadow-black/40">{toast}</div>}
    </div>
  );
}
