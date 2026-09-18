# StoryboardAI Cinematic Frontend v2

Backend FastAPI giữ nguyên. Chỉ thay frontend.

## Cách thay

1. Backup folder hiện tại:

```powershell
cd D:\EDARP-full-chatgpt-openai-fixed\K4-3B-E403-BotVN\codebase
Rename-Item frontend frontend-old
```

2. Copy toàn bộ folder frontend mới vào:

```text
K4-3B-E403-BotVN/codebase/frontend
```

3. Chạy:

```powershell
cd D:\EDARP-full-chatgpt-openai-fixed\K4-3B-E403-BotVN\codebase\frontend
npm install
npm run dev
```

4. Backend vẫn chạy ở terminal khác:

```powershell
cd D:\EDARP-full-chatgpt-openai-fixed\K4-3B-E403-BotVN\codebase\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload --port 8000
```

5. Mở:

```text
http://127.0.0.1:5173
```

## Flow UI mới

1. Nạp Kịch Bản
2. Bảng Duyệt Storyboard
3. Xem Thử Animatic
4. Bàn Giao

Trang Review vẫn được mở từ từng Scene trong Bảng Duyệt và dùng đúng API `/api/scenes/{id}/revise` hiện tại.
