# Hướng Dẫn Quay Video 30 Giây Thao Tác Trực Tiếp Sản Phẩm (CP3 Video Guide)

**Dự án:** StoryboardAI — Agent dựng kịch bản hình ảnh cho video bài giảng (Track C · Lesson Studio)  
**Nhóm:** `K4-3B-E403-BotVN` (Lớp 3B · Phòng E403)  
**Yêu cầu CP3:** Video 30 giây quay màn hình thao tác thật trên sản phẩm, thấy AI trả kết quả thật (Live AI call), không cần dựng cầu kỳ, không cần lồng tiếng.

---

## 1. Chuẩn Bị Trước Khi Bấm Quay
1. Mở Terminal (PowerShell hoặc Command Prompt) tại thư mục dự án:
   ```powershell
   cd D:\VinAi\Chieu\minihackathon\K4-3B-E403-BotVN
   ```
2. Kích hoạt môi trường Python (hoặc chạy trực tiếp bằng python venv):
   ```powershell
   & "D:\VinAi\Chieu\day3\K4-Day03-PhamDinhHai-2A202602482\.venv\Scripts\python.exe" codebase/app_demo.py
   ```
3. Chuẩn bị phần mềm quay màn hình:
   - Sử dụng **Xbox Game Bar** (phím tắt: `Windows + Alt + R` để bật/tắt quay).
   - Hoặc **OBS Studio**, **ShareX**, **Snagit** đều được.

---

## 2. Kịch Bản Thao Tác 30 Giây (Chi Tiết Từng Giây)

| Thời gian | Hành động trên màn hình | Điểm nhấn cần cho giám khảo/người xem thấy |
|---|---|---|
| **00:00 - 00:05** (5s) | Khởi động lệnh `python codebase/app_demo.py`. Banner sản phẩm StoryboardAI và menu chọn kịch bản xuất hiện. | Tên dự án, tên nhóm `K4-3B-E403-BotVN`, mốc CP3, model `gemini-flash-lite-latest`. |
| **00:05 - 00:08** (3s) | Nhấn phím `1` (hoặc `Enter`) chọn kịch bản kiến trúc Caching: *"Khi người dùng gửi yêu cầu, Web Server tiếp nhận..."* | Thấy rõ kịch bản văn bản bài giảng đầu vào thực tế. |
| **00:08 - 00:12** (4s) | Màn hình hiển thị: `⚡ Đang gửi yêu cầu đến Gemini AI Model...` | Chứng minh **LIVE CALL** gọi API thật, không phải hardcode tĩnh. |
| **00:12 - 00:22** (10s) | AI trả về kết quả phân cảnh trong ~2.2 giây! Các Frame phân cảnh xuất hiện: `Frame 1`, `Frame 2`. Cuộn chuột chậm xem chi tiết. | **On-screen text**: ngắn gọn $\le 40$ ký tự.<br>**Visual Symbol**: Server rack, Cache chip, Database cylinder.<br>**Safe Zone**: Tọa độ nằm trong khung chuẩn. |
| **00:22 - 00:30** (8s) | Dừng lại ở khối kiểm thử tự động cuối cùng: `🔍 ĐÁNH GIÁ STYLEBOOK: ✅ ĐẠT CHUẨN` (Ràng buộc ký tự: ĐẠT, Safe Zone: ĐẠT, Chống ảo giác: ĐẠT). | Khẳng định tính kỷ luật kỹ thuật và độ tin cậy của sản phẩm. Kết thúc video! |

---

## 3. Demo Giao Diện Web Trực Tiếp (Khuyên dùng khi quay video)
1. Khởi chạy server bằng cách nhấp đúp file `run_demo.bat` (hoặc lệnh `python codebase/app_server.py`).
2. Trình duyệt tự động mở tại `http://localhost:8501`.
3. Thao tác 4 bước:
   - **Bước 1 (Nhập kịch bản):** Dán kịch bản bài giảng bất kỳ (hoặc bấm nút chọn mẫu).
   - **Bước 2 (Bảng duyệt AI thật):** AI phân cảnh với tranh vẽ Concept Art 16:9 sắc nét, chữ màn hình $\le 40$ ký tự, hợp chuẩn Safe Zone. Thử bấm *"✏ Góp ý cảnh này"* để chứng minh tính năng Granular Live Edit.
   - **Bước 3 (Animatic):** Bấm Play xem luồng chạy theo dòng thời gian.
   - **Bước 4 (Handoff):** Xuất đặc tả kỹ thuật JSON cho Remotion và Báo cáo kiểm định Audit Log.

---
*Kịch bản được tối ưu để quay 30 - 45 giây thể hiện trọn vẹn sức mạnh AI thật chuẩn tiêu chí Checkpoint 3.*
