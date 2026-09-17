# Kế Hoạch Hình Ảnh & Bản Mock Bấm Được (Deliverable CP2)

**Người thực hiện:** Phạm Đình Hải (2A202602482)  
**Nhánh:** `hai`  
**Dự án:** Track C · Đề C4: StoryboardAI — Agent dựng kịch bản hình ảnh cho video bài giảng  
**Nhóm:** `K4-3B-E403-BotVN` (Hoàng · Hải · Đại)

---

## 📌 Nội dung bàn giao trong Pull Request

### 1. File Prototype: `mockup-cp2.html`
Bản mock bấm được tương tác hoàn chỉnh (Clickable Prototype) đáp ứng 100% tiêu chí của **Checkpoint 2 (CP2)** theo yêu cầu của BTC Hackathon.

* **Cách mở:** Nhấp đúp chuột vào file `mockup-cp2.html` hoặc chuột phải chọn *Open with Chrome / Edge*. Không cần cài đặt thêm thư viện (chạy offline độc lập).
* **Các tính năng đã hoàn thiện:**
  1. **Bước 1 — Nạp kịch bản & Sổ quy ước (Stylebook):**
     * Hỗ trợ dữ liệu JSON `loi-doc-d1-2.json` có mốc thời gian từng từ (`mocTu`, `chuoiMocTu`).
     * Khóa cứng Sổ quy ước: Bảng màu ngữ nghĩa (Semantic Palette), Thư viện ký hiệu (Database hình trụ 3 tầng, Server đèn LED), và nguyên tắc không bịa số liệu ảo.
  2. **Bước 2 — Bảng duyệt Storyboard (Visual Board):**
     * Khung hình chuẩn 1920×1080 @ 30fps.
     * **Lưới Vùng An Toàn (Safe Zone):** Chuẩn xác tọa độ nhóm quy định ($x \in [80, 1840]$, $y \in [250, 960]$), chừa dải trên cho HUD và dải đáy cho phụ đề. Có công tắc bật/tắt trực quan.
     * **Cụm từ kích hoạt (Trigger Words):** Được highlight vàng cam nổi bật kèm mốc thời gian.
     * **Tự soát chữ màn hình:** Bộ đếm ký tự thời gian thực báo xanh khi $\le 40$ ký tự, báo đỏ khi vượt quá.
     * **Sửa cục bộ 1 cảnh (Granular Edit):** Bấm *✏ Góp ý cảnh này* ở Cảnh 02 $\rightarrow$ Chỉ riêng Cảnh 02 phát sáng và cập nhật sang hình đám mây/khiên, các cảnh khác giữ nguyên 100% (bảo toàn ngữ cảnh).
     * **Đổi phong cách giữ nguyên ý:** Chuyển đổi giữa *Tech Blueprint*, *Hand-drawn Chalkboard* (Bảng phấn), và *Minimal 2D* mà không làm mất ý sư phạm.
  3. **Bước 3 — Trình phát Animatic xem thử:**
     * Chạy thử mô phỏng video player theo dòng thời gian, đồng bộ nhịp đọc và phụ đề ở đáy trước khi tốn chi phí dựng video.
  4. **Bước 4 — Bàn giao thông số kỹ thuật (Handoff Spec):**
     * Xuất file Storyboard Spec JSON chuẩn chỉnh cho Motion Designer / Coding Agent (Remotion/Manim).
     * Xuất Báo cáo kiểm định Sổ quy ước (Audit Log) minh chứng không vi phạm quy chuẩn BTC.

---

## 🗺️ Sơ đồ luồng hoạt động (Dành cho Slide / Form nộp CP2)

```mermaid
flowchart TD
    subgraph G1 ["Bước 1: Nạp JSON & Stylebook (Trần Tuấn Hoàng)"]
        U(["Người viết kịch bản"]) --> S1["Nạp file JSON kịch bản (mocTu, chuoiMocTu)"]
        S1 --> S2["Áp dụng Sổ Quy Ước: Màu ngữ nghĩa & Biểu tượng chuẩn"]
        S2 --> S3["Khóa ràng buộc: Safe-zone x:80-1840, y:250-960 & Chữ <= 40 ký tự"]
        S3 --> S4["Bấm '🚀 Tạo Kế Hoạch Hình Cho Cả Video'"]
    end

    subgraph G2 ["Bước 2: AI Pipeline & Xử lý Ca Khó (Phạm Đình Hải)"]
        S4 --> P1["Bóc tách 'Ý sư phạm cần thấy' độc lập phong cách vẽ"]
        P1 --> P2["Gắn Trigger Words đồng bộ mốc thời gian đọc"]
        P2 --> P3["Kiểm soát Non-hallucination: Không tự bịa số liệu ảo"]
        P3 --> P4["Sinh ảnh phác 1920x1080 chuẩn Safe-zone"]
    end

    subgraph G3 ["Bước 3: Bảng Duyệt & Sửa Cảnh (Nguyễn Văn Đại)"]
        P4 --> B1["Bảng Storyboard: Khung 16:9 + Trigger Word + Chữ màn hình"]
        B1 --> B2{"Thao tác người duyệt:"}
        B2 -->|"Góp ý 1 cảnh"| EDIT1["AI vẽ lại DUY NHẤT cảnh đó (Cảnh khác giữ nguyên)"]
        B2 -->|"Đổi style"| EDIT2["Đổi nét vẽ (Ý sư phạm giữ nguyên)"]
        B2 -->|"Xem thử"| PLAY["Chạy thử Animatic theo nhịp thời gian"]
        B2 -->|"Chốt kịch bản"| APP["Bấm 'Hoàn tất & Bàn giao'"]
    end

    subgraph G4 ["Bước 4: Bàn Giao Handoff"]
        APP --> OUT1["Storyboard Spec (JSON) cho Motion Designer / Coding Agent"]
        APP --> OUT2["Báo cáo Kiểm định Sổ quy ước & Lưới an toàn"]
    end
```
