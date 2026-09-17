# Thư Mục Kiểm Thử & Đo Lường Định Lượng (Checkpoint 3 - CP3)

**Dự án:** StoryboardAI — Agent dựng kịch bản hình ảnh cho video bài giảng (Đề C4 · Track C Lesson Studio)  
**Nhóm:** `K4-3B-E403-BotVN` (Lớp 3B · Phòng E403)  
**Thành viên:** Phạm Đình Hải (2A202602482), Trần Tuấn Hoàng (2A202602832 - Trưởng nhóm), Nguyễn Văn Đại (2A202602477)  

---

## 📁 Cấu Trúc Thư Mục `eval/`

```
eval/
├── golden_set.json        # Bộ 20 test case kiểm thử mẫu phủ 4 lớp chỗ khó
├── run_eval.py            # Script tự động chạy kiểm thử 20 case qua Live Gemini API
├── run1_raw_logs.jsonl    # Log thô từng case (raw prompt, raw response, latency, audit)
├── run1_report.md         # Báo cáo đánh giá tổng hợp Lượt 1 (Pass Rate 95.0%)
└── video_demo_guide.md    # Hướng dẫn chi tiết kịch bản quay video 30 giây thao tác sản phẩm
```

---

## 🎯 1. Bộ Kiểm Thử Mẫu (`golden_set.json`)
Bao gồm **20 test cases** được thiết kế có chủ đích nhằm đối mặt trực tiếp với các điểm mù và thách thức thực tế của LLM:
- **Lớp ① Nguồn sự thật (Grounding - 3 cases):** Văn bản chỉ có thông tin định tính, nghiêm cấm AI tự bịa số liệu, tỷ lệ %.
- **Lớp ② Trừu tượng & Mơ hồ (Abstract Concepts - 4 cases):** Khái niệm trừu tượng (Con trỏ RAM, Agile, Sóng hấp dẫn, Hiệu ứng cánh bướm) phải được chuyển hóa thành ẩn dụ trực quan cụ thể.
- **Lớp ③ Ràng buộc & Quá tải nhận thức (Constraints & Overload - 4 cases):** Câu thoại dài 50-70 từ, ép AI phải chia cắt hợp lý và giữ `on_screen_text` $\le 40$ ký tự.
- **Lớp ④ Biểu tượng chuyên ngành (Domain Symbols - 4 cases):** Khóa cứng biểu tượng Stylebook (Database cylinder 3 tầng, Server rack xanh có đèn LED, Queue băng chuyền Kafka).
- **Trường hợp phổ biến (Common Happy Path - 3 cases):** Lời chào mở đầu, so sánh CPU vs GPU, quy trình SDLC.
- **Ca biên hiếm gặp (Rare Edge Cases - 2 cases):** Đầu vào cực tiểu 1 từ ("Docker.") và văn bản ngoại lai lạc đề.

---

## 🚀 2. Cách Chạy Kiểm Thử Tự Động (`run_eval.py`)

Chạy lệnh sau từ thư mục gốc của repo:
```powershell
python eval/run_eval.py
```
*(Nếu dùng môi trường ảo, chỉ định python: `& "D:\VinAi\Chieu\day3\K4-Day03-PhamDinhHai-2A202602482\.venv\Scripts\python.exe" eval/run_eval.py`)*

Script sẽ:
1. Đọc từng case từ `golden_set.json`.
2. Gọi Live AI qua Google Gemini SDK (`gemini-flash-lite-latest`).
3. Tự động kiểm tra 4 tiêu chuẩn kỹ thuật: Độ dài chữ $\le 40$, Safe Zone $[80..1840, 250..960]$, Chống ảo giác số liệu, và JSON Schema hợp lệ.
4. Ghi nối tiếp vào `run1_raw_logs.jsonl`.
5. Tự động kết xuất báo cáo `run1_report.md`.

---

## 📊 3. Tóm Tắt Kết Quả Lượt 1 (Run 1)

* **Tổng số case:** 20 / 20
* **Số case ĐẠT (PASS):** **19 / 20** (**95.0%**)
* **Số case KHÔNG ĐẠT (FAIL):** **1 / 20** (Case `TC03` - vi phạm độ dài chữ `on_screen_text` 44 ký tự > 40).
* **Thời gian phản hồi trung bình (Avg Latency):** **1881 ms** (~1.88 giây/lần gọi AI).
* **Tuân thủ Safe Zone:** **100%** (Tất cả tọa độ $x, y$ nằm trọn vẹn trong vùng an toàn).

---

## 🎬 4. Hướng Dẫn Quay Video 30 Giây Thao Tác Trực Tiếp
Xem chi tiết tại [video_demo_guide.md](video_demo_guide.md) để thực hiện quay đúng 30 giây màn hình tương tác với `codebase/app_demo.py` chứng minh lệnh gọi AI thật.
