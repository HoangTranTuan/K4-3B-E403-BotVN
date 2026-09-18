# StoryboardAI React + FastAPI pack

Gói này được viết để copy vào repo:

```text
K4-3B-E403-BotVN/
├── codebase/
│   ├── backend/       <- copy backend vào đây
│   └── frontend/      <- copy frontend vào đây
├── data/
│   └── studio-pack/
│       └── c4-storyboardai/
└── eval/
```

## 1. Copy folder

Copy hai folder:

```text
backend
frontend
```

vào:

```text
K4-3B-E403-BotVN/codebase/
```

Kết quả:

```text
codebase/
├── backend/
│   ├── main.py
│   ├── storyboard_agent.py
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── index.html
    └── src/
```

## 2. Backend

PowerShell:

```powershell
cd codebase\backend

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
Copy-Item .env.example .env
```

Mở `.env` và sửa:

```env
GEMINI_API_KEY=YOUR_REAL_KEY
GEMINI_MODEL=gemini-2.5-flash
```

Chạy:

```powershell
python -m uvicorn main:app --reload --port 8000
```

Test:

```text
http://127.0.0.1:8000/api/health
```

## 3. Frontend

Mở terminal thứ hai:

```powershell
cd codebase\frontend
npm install
npm run dev
```

Mở:

```text
http://127.0.0.1:5173
```

Vite proxy `/api` sang FastAPI port 8000 nên không cần sửa URL.

## 4. Flow demo

1. `Input` -> bấm `BTC sample`.
2. Để `Scene MVP = 10`.
3. Bấm `Tạo Storyboard`.
4. Mở một Scene ở `Storyboard`.
5. Feedback ví dụ:
   `Đơn giản hóa hình, không dùng nhân vật. Giữ nguyên ý và chữ.`
6. Bấm `AI sửa Scene này`.
7. Cho BGK thấy chỉ scene đang chọn đổi.
8. Approve vài scene.
9. Sang `Export` -> Download JSON.

## 5. Không commit secret

Thêm vào `.gitignore` ở root repo:

```gitignore
.env
**/.env
**/.venv/
**/node_modules/
**/dist/
__pycache__/
*.pyc
```

## 6. Push branch cá nhân

```powershell
git add codebase .gitignore
git commit -m "Add StoryboardAI React UI and FastAPI backend"
git pull --rebase origin NguyenVanDai-2A202602477
git push origin NguyenVanDai-2A202602477
```

Nếu `git pull --rebase` có conflict, dừng lại và xử lý conflict trước, không dùng `git push --force`.
