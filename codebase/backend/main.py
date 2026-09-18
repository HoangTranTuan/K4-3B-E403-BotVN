import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from storyboard_agent import (
    DEFAULT_STYLEBOOK,
    generate_storyboard,
    revise_scene,
)


HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[2]

SAMPLE_FILE = (
    REPO_ROOT
    / "data"
    / "studio-pack"
    / "c4-storyboardai"
    / "vi-du"
    / "loi-doc-d1-2.json"
)

load_dotenv(HERE.parent / ".env")
load_dotenv(REPO_ROOT / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


app = FastAPI(title="StoryboardAI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    sentences: list[dict[str, Any]]
    stylebook: str = DEFAULT_STYLEBOOK


class ReviseRequest(BaseModel):
    scene: dict[str, Any]
    feedback: str
    stylebook: str = DEFAULT_STYLEBOOK
    original_sentence: dict[str, Any] | None = None


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def extract_sentences(data: Any) -> list[dict]:
    if isinstance(data, dict):
        if isinstance(data.get("cau"), list):
            return [x for x in data["cau"] if x.get("loi")]
        if isinstance(data.get("sentences"), list):
            return [x for x in data["sentences"] if x.get("loi")]
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict) and x.get("loi")]
    return []


def require_key():
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Chưa cấu hình GEMINI_API_KEY trong codebase/backend/.env",
        )


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "gemini_configured": bool(GEMINI_API_KEY),
        "sample_exists": SAMPLE_FILE.exists(),
    }


@app.get("/api/stylebook")
def stylebook():
    return {"stylebook": DEFAULT_STYLEBOOK}


@app.get("/api/sample")
def sample():
    if not SAMPLE_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy fixture: {SAMPLE_FILE}",
        )

    data = load_json(SAMPLE_FILE)
    sentences = extract_sentences(data)
    return {
        "id": data.get("id"),
        "title": data.get("tieuDe", "Video bài giảng"),
        "objective": data.get("mucTieu", ""),
        "fps": data.get("fps", 30),
        "count": len(sentences),
        "sentences": sentences,
    }


@app.post("/api/storyboard")
def storyboard(request: GenerateRequest):
    require_key()

    if not request.sentences:
        raise HTTPException(status_code=400, detail="Chưa có lời đọc.")

    try:
        scenes = generate_storyboard(
            request.sentences,
            request.stylebook,
            GEMINI_API_KEY,
        )
        return {"count": len(scenes), "scenes": scenes}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/scenes/{scene_id}/revise")
def revise(scene_id: int, request: ReviseRequest):
    require_key()

    if int(request.scene.get("n") or -1) != scene_id:
        raise HTTPException(status_code=400, detail="scene_id không khớp payload.")

    if not request.feedback.strip():
        raise HTTPException(status_code=400, detail="Feedback đang trống.")

    try:
        scene = revise_scene(
            request.scene,
            request.feedback,
            request.stylebook,
            GEMINI_API_KEY,
            request.original_sentence,
        )
        return {"scene": scene}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
