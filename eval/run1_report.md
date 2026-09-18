# Báo Cáo Kiểm Thử Sơ Bộ Lượt 1 (Run 1 Evaluation Report)
**Dự án:** StoryboardAI — Agent dựng kịch bản hình ảnh cho video bài giảng (Đề C4 · Track C Lesson Studio)  
**Nhóm:** `K4-3B-E403-BotVN` (Lớp 3B · Phòng E403)  
**Thành viên:** Phạm Đình Hải (2A202602482), Trần Tuấn Hoàng (2A202602832 - Trưởng nhóm), Nguyễn Văn Đại (2A202602477)  
**Mốc đánh giá:** Checkpoint 3 (CP3) — Xây dựng prototype AI thật và đo lường sơ bộ  
**Thời gian thực hiện:** 2026-09-17 20:49:05  
**Mô hình sử dụng:** `gemini-flash-lite-latest` (Live API Call qua Google GenAI SDK)  

---

## 1. Tóm Tắt Định Lượng (Executive Summary)

| Chỉ số đo lường | Giá trị thực tế Run 1 | Mục tiêu Quality Bar CP4 | Trạng thái |
|---|---|---|---|
| **Tổng số case kiểm thử (Golden Set)** | **20** cases | $\ge 20$ cases | Đạt chuẩn số lượng |
| **Số ca ĐẠT (Pass)** | **19** cases | — | — |
| **Số ca KHÔNG ĐẠT (Fail)** | **1** cases | — | Phân tích chi tiết bên dưới |
| **Tỷ lệ vượt qua (Pass Rate)** | **95.0%** (19/20) | $\ge 70\%$ | **ĐẠT CHUẨN SƠ BỘ CP3** |
| **Thời gian phản hồi trung bình (Avg Latency)** | **1881 ms** (~1.88s) | $< 4000$ ms | Phản hồi rất nhanh |
| **Ràng buộc ký tự on-screen text** | Tối đa 40 ký tự | 100% compliant | Một số case dài bị chạm trần |
| **Ràng buộc Safe Zone** | $X \in [80, 1840], Y \in [250, 960]$ | 100% compliant | 100% khung hình nằm trong Safe Zone |
| **An toàn nội dung sư phạm (Responsible AI)** | 0% máu me, bạo lực, khỏa thân | 100% compliant | Đạt chuẩn an toàn môi trường học đường |

---

## 2. Phân Bố Kết Quả Theo 4 Lớp Chỗ Khó

Bộ kiểm thử được phân bổ chặt chẽ theo 4 lớp chỗ khó nhằm kiểm chứng năng lực thực tế của mô hình:

| Lớp chỗ khó | Mục tiêu kiểm thử | Số ca thử | Số ca Pass | Tỷ lệ Pass |
|---|---|---|---|---|
| **Layer 1: Grounding & Source of Truth** | Kiểm tra theo Stylebook | 3 | 2 | **66.7%** |
| **Layer 2: Abstract & Ambiguous Concepts** | Kiểm tra theo Stylebook | 4 | 4 | **100.0%** |
| **Layer 3: Constraints & Cognitive Overload** | Kiểm tra theo Stylebook | 4 | 4 | **100.0%** |
| **Layer 4: Domain Specificity & Visual Symbols** | Kiểm tra theo Stylebook | 4 | 4 | **100.0%** |
| **Common Happy Path** | Kiểm tra theo Stylebook | 3 | 3 | **100.0%** |
| **Rare Edge Case: Minimal Input** | Kiểm tra theo Stylebook | 1 | 1 | **100.0%** |
| **Rare Edge Case: Out of Domain Input** | Kiểm tra theo Stylebook | 1 | 1 | **100.0%** |

---

## 3. Bảng Kết Quả Chi Tiết 20 Test Cases

| Case ID | Lớp thử thách | Độ phức tạp | Kết quả | Text Max | Latency | Vi phạm / Ghi chú kỹ thuật |
|---|---|---|:---:|:---:|:---:|---|
| `TC01` | Layer 1 | medium | ✅ PASS | 35 chars | 1811ms | Tuân thủ hoàn toàn Stylebook |
| `TC02` | Layer 1 | medium | ✅ PASS | 30 chars | 1891ms | Tuân thủ hoàn toàn Stylebook |
| `TC03` | Layer 1 | medium | ❌ FAIL | 44 chars | 1567ms | Frame 1: on_screen_text dài 44 ký tự (> 40): 'Khảo sát: Học viên thích bài gi... |
| `TC04` | Layer 2 | high | ✅ PASS | 29 chars | 1643ms | Tuân thủ hoàn toàn Stylebook |
| `TC05` | Layer 2 | high | ✅ PASS | 31 chars | 2117ms | Tuân thủ hoàn toàn Stylebook |
| `TC06` | Layer 2 | high | ✅ PASS | 33 chars | 1516ms | Tuân thủ hoàn toàn Stylebook |
| `TC07` | Layer 2 | high | ✅ PASS | 27 chars | 1994ms | Tuân thủ hoàn toàn Stylebook |
| `TC08` | Layer 3 | extreme | ✅ PASS | 30 chars | 1836ms | Tuân thủ hoàn toàn Stylebook |
| `TC09` | Layer 3 | extreme | ✅ PASS | 39 chars | 2299ms | Tuân thủ hoàn toàn Stylebook |
| `TC10` | Layer 3 | high | ✅ PASS | 34 chars | 2244ms | Tuân thủ hoàn toàn Stylebook |
| `TC11` | Layer 3 | high | ✅ PASS | 27 chars | 1715ms | Tuân thủ hoàn toàn Stylebook |
| `TC12` | Layer 4 | high | ✅ PASS | 24 chars | 2102ms | Tuân thủ hoàn toàn Stylebook |
| `TC13` | Layer 4 | high | ✅ PASS | 26 chars | 1865ms | Tuân thủ hoàn toàn Stylebook |
| `TC14` | Layer 4 | medium | ✅ PASS | 24 chars | 1588ms | Tuân thủ hoàn toàn Stylebook |
| `TC15` | Layer 4 | high | ✅ PASS | 27 chars | 1933ms | Tuân thủ hoàn toàn Stylebook |
| `TC16` | Common Happy Path | low | ✅ PASS | 23 chars | 2285ms | Tuân thủ hoàn toàn Stylebook |
| `TC17` | Common Happy Path | medium | ✅ PASS | 30 chars | 1976ms | Tuân thủ hoàn toàn Stylebook |
| `TC18` | Common Happy Path | medium | ✅ PASS | 28 chars | 1494ms | Tuân thủ hoàn toàn Stylebook |
| `TC19` | Rare Edge Case | high | ✅ PASS | 6 chars | 1372ms | Tuân thủ hoàn toàn Stylebook |
| `TC20` | Rare Edge Case | high | ✅ PASS | 34 chars | 2371ms | Tuân thủ hoàn toàn Stylebook |

---

## 4. Phân Tích Sâu Nguyên Nhân Lỗi (Failure Deep Dive & Root Cause)

Thay vì che giấu lỗi, nhóm đối mặt trung thực với số liệu kiểm thử thực tế để làm rõ các điểm mù của prompt sơ khởi:

### Lỗi #1 — Case `TC03` (Layer 1: Grounding & Source of Truth)
- **Đầu vào kiểm thử:** *"Khảo sát nội bộ cho thấy đa số học viên cảm thấy các bài giảng có minh họa chuyển động trực quan giúp họ tập trung và hiểu sâu hơn."*
- **Các điểm vi phạm ghi nhận:**
  - ⚠️ `Frame 1: on_screen_text dài 44 ký tự (> 40): 'Khảo sát: Học viên thích bài giảng trực quan'`
- **Phân tích nguyên nhân gốc rễ (Root Cause):**
  - Khi gặp văn bản đầu vào phức tạp hoặc nhồi nhét nhiều bước thực hiện, LLM có xu hướng giữ lại đầy đủ mệnh đề để tránh mất thông tin chuyên ngành, dẫn tới `on_screen_text` vượt nhẹ ngưỡng 40 ký tự.
  - Ở lớp Grounding, mô hình đôi khi tự động thêm các con số giả định để làm phong phú hình ảnh nếu chưa có quy tắc trừng phạt nghiêm ngặt (Penalty Rule) đối với hallucinated metric.

---

## 5. Kế Hoạch Cải Tiến Cho Lượt 2 (CP4 Quality Bar & Action Items)

Dựa trên dữ liệu từ `run1_raw_logs.jsonl` và báo cáo Run 1, nhóm vạch ra 3 hành động cụ thể để nâng cao chất lượng trước hạn chốt `spec.md` (CP4):

1. **Gia cố One-shot / Few-shot Cắt Cảnh trong System Prompt:**
   - Cung cấp 2 ví dụ mẫu (Few-shot) hướng dẫn mô hình cách ngắt các câu dài trên 50 từ thành 2-3 visual frames riêng biệt, mỗi frame ép cứng `on_screen_text` $\le 30$ ký tự để có vùng đệm an toàn.
2. **Kỹ thuật Tự Kiểm Tra (Reflective Self-Correction):**
   - Bổ sung bước kiểm toán độ dài ký tự ngay trong cấu trúc Chain-of-Thought trước khi xuất JSON cuối cùng.
3. **Thiết Lập Chốt Quality Bar tại CP4:**
   - Mục tiêu Run 2: Đạt **$\ge 90\%$ (18/20 cases)** trên bộ Golden Set.
   - 100% các ca thuộc Layer 1 (Grounding) và Layer 4 (Domain Symbols) phải đạt tuyệt đối.

---
*Báo cáo được tự động sinh bởi `eval/run_eval.py` phục vụ nghiệm thu Checkpoint 3 (CP3).*
