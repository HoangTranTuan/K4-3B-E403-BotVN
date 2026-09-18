# 🎬 StoryboardAI — Agent Dựng Kịch Bản Hình Ảnh Bài Giảng Chuẩn Studio

**Mini Hackathon AI — Batch 04 · Lớp 3B · Phòng E403 · Nhóm K4-3B-E403-BotVN**  
**Track C — Lesson Studio · Đề C4: StoryboardAI**  
*SPEC → Prototype → Demo.*

---

## 👥 Thành viên nhóm & Phân công vai trò

| Họ và Tên | Mã Học Viên | Vai trò chính | Phần việc đảm nhiệm trong dự án | Trạng thái |
|---|---|---|---|:---:|
| **Trần Tuấn Hoàng** | 2A202602832 | Trưởng nhóm & Product Lead | Định vị JTBD & Lát cắt Canvas CP1, viết AI Spec CP4, kịch bản Video Demo & chuẩn bị Slide pitch CP5 | **Hoàn thành** |
| **Phạm Đình Hải** | 2A202602482 | Lead AI & Prototype Engineer | Xây dựng lõi `StoryboardAgent` (Live Gemini), lập trình prompt 16:9 Concept Art, xử lý Safe Zone & 3 Ca Khó, thiết lập Golden Set 20 case & đo lường Run 1 | **Hoàn thành** |
| **Nguyễn Văn Đại** | 2A202602477 | Frontend & Integration Engineer | Phát triển giao diện Web App tương tác (`index.html`), trình phát Animatic, bộ xuất Handoff Spec & Audit Log, kết nối API backend | **Hoàn thành** |

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY (QUICK START)

Tài liệu này dành cho ban giám khảo, mentor hoặc bất kỳ ai clone mã nguồn về máy tính cá nhân để cài đặt và trải nghiệm phần mềm.

### 📋 Yêu cầu hệ thống
- **Hệ điều hành:** Windows 10/11, macOS, hoặc Linux.
- **Python:** Phiên bản `>= 3.10` (Khuyên dùng Python 3.10 hoặc 3.11).
- **Trình duyệt web:** Google Chrome, Microsoft Edge, Firefox hoặc Safari.
- **Git** đã được cài đặt trên máy.

---

### 📦 Bước 1: Clone Repository về máy
Mở Terminal / PowerShell / Command Prompt và chạy lệnh:
```bash
git clone https://github.com/vantoandx/K4-3B-E403-BotVN.git
cd K4-3B-E403-BotVN
```

---

### 📦 Bước 2: Cài đặt thư viện phụ thuộc
Dự án được tối ưu hóa cực nhẹ, chỉ sử dụng 2 thư viện chuẩn:
```bash
pip install -r requirements.txt
```
> *(Tùy chọn) Nếu bạn muốn sử dụng môi trường ảo venv:*
> ```bash
> python -m venv venv
> # Kích hoạt trên Windows:
> venv\Scripts\activate
> # Kích hoạt trên macOS/Linux:
> source venv/bin/activate
> pip install -r requirements.txt
> ```

---

### 🔑 Bước 3: Cấu hình Gemini API Key (BẮT BUỘC ĐỂ GỌI LIVE AI)

> ⚠️ **TẠI SAO REPO KHÔNG CÓ SẴN FILE .ENV HAY API KEY?**  
> GitHub kích hoạt cơ chế tự động quét bảo mật mã nguồn (*GitHub Secret Scanning*). Nếu đẩy file chứa API Key thật lên GitHub, khoá sẽ ngay lập tức bị GitHub chặn push hoặc tự động thu hồi/khóa key vĩnh viễn để bảo vệ tài khoản.  
> Do đó, theo nguyên tắc bảo mật chuẩn công nghiệp, file cấu hình bảo mật `.env` đã được đưa vào `.gitignore`. Bạn chỉ cần tạo file `.env` trên máy cá nhân theo hướng dẫn sau:

#### 1. Tạo file `.env` từ file mẫu `.env.example`
Ở thư mục gốc dự án đã có sẵn file mẫu `.env.example`. Hãy sao chép thành file `.env`:
- **Trên Windows (PowerShell / Command Prompt):**
  ```powershell
  copy .env.example .env
  ```
- **Trên macOS / Linux:**
  ```bash
  cp .env.example .env
  ```
*(Hoặc bạn có thể tạo thủ công một file văn bản mới tên là `.env` ngay tại thư mục gốc của dự án).*

#### 2. Điền API Key của bạn vào file `.env`
Mở file `.env` vừa tạo bằng bất kỳ trình soạn thảo nào (VS Code, Notepad, Notepad++, Cursor, v.v.) và thay thế chuỗi `your_gemini_api_key_here` bằng key của bạn:
```env
GEMINI_API_KEY=AIzaSy...your_gemini_api_key_here...
GEMINI_MODEL=gemini-flash-lite-latest
```

#### 3. Hướng dẫn lấy Gemini API Key (Hoàn toàn Miễn Phí)
1. Truy cập trang chính thức của Google: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Đăng nhập bằng tài khoản Google.
3. Bấm **"Create API key"** (Tạo khóa API chỉ mất khoảng 15 giây, miễn phí với hạn mức thoải mái cho thử nghiệm).
4. Sao chép chuỗi khóa và dán vào biến `GEMINI_API_KEY` trong file `.env`.

> 💡 **Cơ chế Dự phòng (Fallback / Safe Mode):**  
> Nếu bạn chưa có sẵn API Key ngay, hệ thống vẫn tích hợp chế độ AI Concept Art Visualizer trực tiếp qua Internet và Wireframe Blueprint dự phòng. Bạn hoàn toàn có thể mở và trải nghiệm toàn bộ giao diện, các kịch bản mẫu và 3 ca khó mà không bị crash.

---

### 💻 Bước 4: Khởi chạy và Sử dụng Phần mềm

Bạn có thể lựa chọn một trong các cách sau:

#### Cách 1: 1-Click Chạy Ngay trên Windows (Khuyên dùng nhất ⭐)
- Nhấp đúp chuột vào file **`run_demo.bat`** tại thư mục gốc của dự án.
- Script sẽ tự khởi động backend server và tự mở trình duyệt web tại: `http://localhost:8501`.

#### Cách 2: Khởi chạy Web Server bằng dòng lệnh
Chạy lệnh sau tại thư mục gốc dự án:
```bash
python codebase/app_server.py
```
Sau đó mở trình duyệt web bất kỳ và truy cập vào:
👉 **`http://localhost:8501`**

#### Cách 3: Chạy bản Demo Dòng Lệnh (CLI Demo — Phục vụ Video Thao Tác 30s)
Để kiểm tra phản hồi tức thì của AI qua terminal hoặc quay video thao tác 30 giây phục vụ nghiệm thu Checkpoint 3:
```bash
python codebase/app_demo.py
```

#### Cách 4: Chạy bộ kiểm thử tự động Golden Set (Benchmark Evaluation)
Để chạy tự động 20 ca kiểm thử thực tế trích xuất từ dữ liệu bài giảng VLearn, đo lường độ tuân thủ Sổ quy ước, Safe Zone và On-screen Text ≤ 40 ký tự:
```bash
# Trên Windows:
run_eval.bat

# Hoặc gõ lệnh Python trực tiếp:
python eval/run_eval.py
```
Báo cáo kết quả chi tiết sẽ được tự động xuất tại `eval/run1_report.md`.

#### Cách 5: Xem lại bản Mockup tương tác Checkpoint 2 (CP2)
Bản mockup tương tác tĩnh được nộp tại Checkpoint 2 vẫn được lưu trữ nguyên vẹn:
- Mở file: **`codebase/mockup-cp2.html`** bằng cách nhấp đúp chuột hoặc kéo thả vào trình duyệt Chrome/Edge.
- Không cần cài đặt bất kỳ thư viện hay chạy server nào.

---

## 🌟 5 Điểm Đột Phá Kỹ Thuật Của StoryboardAI

### 1. Studio-Grade 16:9 Digital Concept Art Engine (Sinh ảnh AI động 100%)
- **Không hardcode ảnh tĩnh:** Từng câu thoại kịch bản bài giảng đều được AI phân tích ngữ cảnh sư phạm để sinh tranh minh họa 16:9 giàu tính điện ảnh.
- **Bộ lọc An toàn Sư phạm (Zero Nudity Guardrails):** Hệ thống tích hợp bộ từ khóa Negative Prompt nghiêm ngặt, loại bỏ hoàn toàn các nội dung phản cảm, khỏa thân, bạo lực máu me, bảo vệ tuyệt đối môi trường giáo dục.
- **Cơ chế Staggered Loader & Skeleton:** Tải tuần tự giãn cách 1.2s giữa các frame ảnh, triệt tiêu hoàn toàn nguy cơ nghẽn mạng hay lỗi Rate Limit HTTP 429 từ nhà cung cấp; hiển thị Loading Skeleton và Spinner mượt mà.
- **Wireframe Blueprint Fallback:** Tự động chuyển sang sơ đồ đồ họa sư phạm kỹ thuật nếu đường truyền mạng gặp sự cố, đảm bảo 0% tỷ lệ chết giao diện.

### 2. Sửa Cục Bộ Bằng Live AI (Granular Live AI Edit)
- Thực thi chính xác Lát cắt Một Câu đã cam kết trong Canvas CP1: *"Khi người dùng sửa một câu thì chỉ đúng ảnh phác thảo của câu đó được cập nhật bằng AI, giữ nguyên các câu khác"*.
- Mỗi thẻ cảnh đều có nút **"✏ Góp ý cảnh này"**. Khi nhập yêu cầu chỉnh sửa, AI thực hiện lệnh gọi độc lập để tạo mới duy nhất cảnh đó. Cảnh được sửa sẽ nhấp nháy viền xanh lá, toàn bộ các phân cảnh còn lại được bảo lưu nguyên vẹn 100%.

### 3. Phòng Thí Nghiệm 3 Ca Khó (Edge Cases Lab)
Tích hợp sẵn bộ test 1-click ngay trên giao diện để chứng minh năng lực trước hội đồng giám khảo:
- **Ca 1 (Khái niệm trừu tượng):** *"Sóng hấp dẫn sinh ra khi hai lỗ đen sáp nhập..."* → AI hình tượng hóa thành mô hình lưới không-thời gian cong của Einstein, thay vì vẽ hình đen sì vô nghĩa.
- **Ca 2 (Câu nhồi nhét nhiều ý):** Đoạn văn 49 từ về định luật nhiệt động lực học → AI tự động phân rã nhịp thị giác, cô đọng chữ hiển thị trên màn hình ≤ 40 ký tự.
- **Ca 3 (Ám chỉ số liệu không có số thật):** *"Kinh tế số Việt Nam bứt phá mạnh mẽ..."* → AI hiển thị biểu đồ xu hướng định tính trừu tượng, tuyệt đối không tự bịa số phần trăm vô căn cứ.

### 4. Bàn Giao Handoff Spec Chuẩn REMOTION & MANIM
- Xuất dữ liệu kịch bản chuẩn cấu trúc JSON kỹ thuật số cho Remotion / Manim / After Effects.
- Tích hợp **Sổ quy ước (Design Tokens)** khóa chặt Safe Zone màn hình:
  - Vùng nội dung an toàn: `x: [80, 1840], y: [250, 960]`
  - Tránh hoàn toàn vùng chiếm dụng của Giảng viên (PiP Camera 16:9 ở góc dưới phải) và thanh điều khiển bài giảng.
  - Lớp phủ chữ màn hình (`on_screen_text`) hiển thị dạng Badge tinh tế ở góc trên trong Safe Zone, không che lấp chi tiết quan trọng.

### 5. Trình Chiếu Animatic Player & Báo Cáo Kiểm Định Audit Log
- Trình phát Animatic Player tích hợp sẵn, mô phỏng video bài giảng chạy theo thời lượng (duration) thực tế của từng phân cảnh.
- Trình xuất Báo cáo Kiểm định Sổ quy ước (Audit Log Report) minh chứng tính minh bạch và độ chính xác của kịch bản phân cảnh.

---

## 📁 Cấu Trúc Thư Mục Repository

```
K4-3B-E403-BotVN/
├── README.md                  # Hướng dẫn cài đặt, khởi chạy & giới thiệu dự án (File này)
├── spec.md                    # Bản đặc tả AI Spec hoàn chỉnh theo Rubric (R1 - R7)
├── requirements.txt           # Danh sách thư viện Python phụ thuộc
├── .env.example               # Mẫu cấu hình biến môi trường GEMINI_API_KEY
├── .gitignore                 # Bảo vệ không đẩy file .env chứa key lên GitHub
├── run_demo.bat               # Phím tắt 1-click khởi chạy Web App trên Windows
├── run_eval.bat               # Phím tắt 1-click chạy kiểm thử Benchmark Golden Set
│
├── codebase/                  # Mã nguồn Prototype sản phẩm (Working Prototype)
│   ├── app_server.py          # Local Web Server kết nối Live Gemini AI (Port 8501)
│   ├── storyboard_agent.py    # Lõi Storyboard Agent điều phối kịch bản & AI Visual
│   ├── index.html             # Giao diện Web App tương tác hoàn chỉnh
│   ├── app_demo.py            # Bản Demo CLI tương tác dòng lệnh (Video thao tác 30s)
│   ├── mockup-cp2.html        # Bản Mockup tương tác tĩnh đã nộp tại Checkpoint 2
│   └── README.md              # Tài liệu kỹ thuật chi tiết của phần backend & frontend
│
├── eval/                      # Bộ công cụ đo lường & kiểm thử (Benchmark R4)
│   ├── run_eval.py            # Kịch bản tự động kiểm thử 20 ca Golden Set
│   ├── run1_report.md         # Báo cáo kết quả đo lường Run 1 (100% Passed)
│   └── video_demo_guide.md    # Kịch bản chi tiết quay video thao tác 30 giây
│
└── validation/                # Nhật ký kiểm thử với người dùng ngoài (R6)
    └── user_testing_log.md    # Biên bản khảo sát và đo lường phản hồi người dùng
```

---

## 🎯 Theo Dõi Tiến Độ Checkpoints (Mini Hackathon AI Batch 04)

| Checkpoint | Nội dung yêu cầu | Trạng thái nhóm K4-3B-E403-BotVN | Minh chứng |
|:---:|---|:---:|---|
| **CP1** | Canvas 7 dòng + Lát cắt 1 câu + Repo GitHub | ✅ Hoàn thành đúng hạn | Đã nộp Form CP1 |
| **CP2** | Bản Mockup tương tác chứng minh luồng thao tác | ✅ Hoàn thành đúng hạn | File `codebase/mockup-cp2.html` |
| **CP3** | Video thao tác 30s + Số đo kiểm thử Run 1 | ✅ Hoàn thành đúng hạn | `codebase/app_demo.py` & `eval/run1_report.md` |
| **CP4** | Chốt bản đặc tả chuẩn đạt `spec.md` | ✅ Hoàn thành | File `spec.md` |
| **CP5** | Slide PDF 6 trang + Video demo dự phòng | 🔄 Đang hoàn thiện | Thư mục repo |
| **CP6** | Thuyết trình & Q&A trước Hội đồng Giám khảo | 🎯 Sẵn sàng | Vòng chung kết phòng E403 |

---

## 🔒 Quy Định Bảo Mật Dữ Liệu
Nhóm cam kết tuân thủ nghiêm ngặt quy định bảo mật dữ liệu của Mini Hackathon AI:
1. Toàn bộ kịch bản và dữ liệu mẫu được ẩn danh hoá hoặc mô phỏng cho mục đích giáo dục.
2. Không lưu trữ thông tin nhận dạng cá nhân của giảng viên hay học viên.
3. Không chia sẻ dữ liệu được cấp ra bên ngoài phạm vi sự kiện.
