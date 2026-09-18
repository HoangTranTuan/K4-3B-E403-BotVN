# Tài Liệu Kỹ Thuật StoryboardAI — Live Prototype (Track C · Đề C4)

**Người thực hiện:** Phạm Đình Hải (2A202602482)  
**Nhánh:** `hai`  
**Dự án:** Track C · Đề C4: StoryboardAI — Agent dựng kịch bản hình ảnh cho video bài giảng  
**Nhóm:** `K4-3B-E403-BotVN` (Hoàng · Hải · Đại)  

---

## 📌 Nội dung hoàn thiện trong phiên bản nâng cấp

Thư mục `codebase/` đã được chuyển hóa hoàn toàn từ mô phỏng sang **Hệ thống AI Động 100% (Dynamic AI Visual Engine)**:

| File | Vai trò & Năng lực mới | Trạng thái |
|---|---|:---:|
| `index.html` | **Giao diện Web App tương tác hoàn chỉnh:** Nhúng Dynamic SVG 100%, tích hợp Modal Sửa Cục Bộ bằng AI (Granular Edit), và Phòng Thí Nghiệm 3 Ca Khó của Hải | Hoàn thiện 100% |
| `app_server.py` | **Local Web Server (Python):** Cung cấp API `/api/generate` và `/api/edit_frame` kết nối Live Gemini AI | Hoàn thiện 100% |
| `storyboard_agent.py` | **Module AI Lõi:** Sinh mã vector SVG động độc bản cho từng cảnh, ép chữ $\le 40$ ký tự, khóa Safe Zone và hậu kiểm Stylebook | Hoàn thiện 100% |
| `app_demo.py` | Demo phiên bản dòng lệnh tương tác trực tiếp (CLI) | Hoàn thiện 100% |

---

## 🎯 4 Điểm Đột Phá Kỹ Thuật

### 1. Dynamic SVG Generator (Xóa bỏ hoàn toàn hình ảnh fix cứng)
- Không dùng bất kỳ template SVG tĩnh nào.
- Mô hình Gemini Flash Lite trực tiếp lập trình mã vector `<svg viewBox="0 0 320 180">` phù hợp 100% với ngữ nghĩa của từng câu bài giảng (dù là mạng nơ-ron, lỗ đen vũ trụ, kinh tế số, thuật toán đệ quy, hay ADN sinh học).
- Ứng dụng bảng màu ngữ nghĩa Stylebook: Xanh dương (#2563EB - hệ thống/chính), Vàng cam (#F59E0B - luồng dữ liệu/trigger), Xanh lá (#10B981 - thành công/kết quả), Tím/Đỏ (#A855F7/#EF4444 - trừu tượng/cảnh báo).

### 2. Sửa Cục Bộ Bằng Live AI (Granular Live AI Edit)
- Đáp ứng đúng Lát Cắt Một Câu trong Canvas CP1: *"người viết sửa một câu thì chỉ đúng ảnh phác thảo của câu đó được cập nhật bằng AI, giữ nguyên các câu khác"*.
- Trên mỗi thẻ cảnh, bấm *✏ Góp ý cảnh này* $\rightarrow$ AI thực thi lệnh gọi riêng biệt để vẽ lại cảnh đó $\rightarrow$ Cảnh được cập nhật và nhấp nháy viền xanh lá, toàn bộ các cảnh khác được giữ nguyên 100%.

### 3. Phòng Thí Nghiệm 3 Ca Khó Của Phạm Đình Hải (Edge Cases Lab)
- Được tích hợp 1-click ngay tại Bước 1 để kiểm chứng năng lực xử lý biên trước ban giám khảo:
  * **Ca 1 (Câu 29 - Khái niệm trừu tượng):** *"Sóng hấp dẫn sinh ra khi hai lỗ đen sáp nhập..."* $\rightarrow$ AI chuyển hóa thành mô hình uốn cong không-thời gian.
  * **Ca 2 (Câu 31 - Câu nhồi nhét nhiều ý):** *"Theo định luật bảo toàn năng lượng 49 từ..."* $\rightarrow$ AI tách cảnh và ép chữ $\le 40$ ký tự.
  * **Ca 3 (Câu 13 - Ám chỉ số liệu không có số thật):** *"Kinh tế số Việt Nam bứt phá mạnh mẽ..."* $\rightarrow$ AI tuân thủ nguyên tắc không bịa % ảo.

### 4. Bàn Giao Handoff & Kiểm Định Tự Động
- Xuất file Handoff Spec JSON chuẩn xác cho Remotion / Manim / Motion Designer.
- Xuất Báo cáo kiểm định Sổ quy ước (Audit Log) minh chứng 100% cảnh nằm trong Safe Zone $x: [80, 1840], y: [250, 960]$ và chữ màn hình $\le 40$ ký tự.

---

## 🚀 Hướng Dẫn Khởi Chạy

- **Cách 1-Click (Khuyên dùng):** Nhấp đúp chuột vào file **`run_demo.bat`** tại thư mục gốc dự án.
- **Cách gõ lệnh:**
  ```powershell
  python codebase/app_server.py
  ```
  Trình duyệt web sẽ tự động mở tại `http://localhost:8501`.
