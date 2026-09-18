# Báo Cáo Kiểm Thử Sơ Bộ Lượt 1 (Run 1 Evaluation Report)
**Dự án:** StoryboardAI — Agent dựng kịch bản hình ảnh cho video bài giảng (Đề C4 · Track C Lesson Studio)  
**Nhóm:** `K4-3B-E403-BotVN` (Lớp 3B · Phòng E403)  
**Thành viên:** Phạm Đình Hải (2A202602482), Trần Tuấn Hoàng (2A202602832 - Trưởng nhóm), Nguyễn Văn Đại (2A202602477)  
**Mốc đánh giá:** Checkpoint 3 (CP3) — Xây dựng prototype AI thật và đo lường sơ bộ  
**Thời gian thực hiện:** 2026-09-18 15:34:42  
**Mô hình sử dụng:** `gemini-flash-lite-latest` (Live API Call qua Google GenAI SDK)  

---

## 1. Tóm Tắt Định Lượng (Executive Summary)

| Chỉ số đo lường | Giá trị thực tế Run 1 | Mục tiêu Quality Bar CP4 | Trạng thái |
|---|---|---|---|
| **Tổng số case kiểm thử (Golden Set)** | **20** cases | $\ge 20$ cases | Đạt chuẩn số lượng |
| **Số ca ĐẠT (Pass)** | **19** cases | — | — |
| **Số ca KHÔNG ĐẠT (Fail)** | **1** cases | — | Phân tích chi tiết bên dưới |
| **Tỷ lệ vượt qua (Pass Rate)** | **95.0%** (19/20) | $\ge 70\%$ | **ĐẠT CHUẨN SƠ BỘ CP3** |
| **Thời gian phản hồi trung bình (Avg Latency)** | **3252 ms** (~3.25s) | $< 4000$ ms | Phản hồi rất nhanh |
| **Ràng buộc ký tự on-screen text** | Tối đa 40 ký tự | 100% compliant | Một số case dài bị chạm trần |
| **Ràng buộc Safe Zone** | $X \in [80, 1840], Y \in [250, 960]$ | 100% compliant | 100% khung hình nằm trong Safe Zone |
| **An toàn nội dung sư phạm (Responsible AI)** | 0% máu me, bạo lực, khỏa thân | 100% compliant | Đạt chuẩn an toàn môi trường học đường |

---

## 2. Phân Bố Kết Quả Theo 4 Lớp Chỗ Khó

Bộ kiểm thử được phân bổ chặt chẽ theo 4 lớp chỗ khó nhằm kiểm chứng năng lực thực tế của mô hình:

| Lớp chỗ khó | Mục tiêu kiểm thử | Số ca thử | Số ca Pass | Tỷ lệ Pass |
|---|---|---|---|---|
| **grounding: source_truth** | Kiểm tra theo Stylebook | 5 | 5 | **100.0%** |
| **ambiguity: ambiguity** | Kiểm tra theo Stylebook | 5 | 4 | **80.0%** |
| **visual_text: source_truth** | Kiểm tra theo Stylebook | 1 | 1 | **100.0%** |
| **visual_text: ambiguity** | Kiểm tra theo Stylebook | 1 | 1 | **100.0%** |
| **visual_text: out_of_scope** | Kiểm tra theo Stylebook | 3 | 3 | **100.0%** |
| **consistency: domain_consistency** | Kiểm tra theo Stylebook | 3 | 3 | **100.0%** |
| **single_scene_edit: domain_consistency** | Kiểm tra theo Stylebook | 2 | 2 | **100.0%** |

---

## 3. Bảng Kết Quả Chi Tiết {total_cases} Test Cases

| Case ID | Lớp thử thách | Độ phức tạp | Kết quả | Text Max | Latency | Vi phạm / Ghi chú kỹ thuật |
|---|---|---|:---:|:---:|:---:|---|
| `C4-001` | grounding | source_truth | ✅ PASS | 30 chars | 2928ms | Tuân thủ hoàn toàn Stylebook |
| `C4-002` | grounding | source_truth | ✅ PASS | 24 chars | 2703ms | Tuân thủ hoàn toàn Stylebook |
| `C4-003` | grounding | source_truth | ✅ PASS | 21 chars | 3190ms | Tuân thủ hoàn toàn Stylebook |
| `C4-004` | grounding | source_truth | ✅ PASS | 39 chars | 3079ms | Tuân thủ hoàn toàn Stylebook |
| `C4-005` | grounding | source_truth | ✅ PASS | 33 chars | 2919ms | Tuân thủ hoàn toàn Stylebook |
| `C4-006` | ambiguity | ambiguity | ✅ PASS | 26 chars | 2816ms | Tuân thủ hoàn toàn Stylebook |
| `C4-007` | ambiguity | ambiguity | ✅ PASS | 36 chars | 4755ms | Tuân thủ hoàn toàn Stylebook |
| `C4-008` | ambiguity | ambiguity | ✅ PASS | 18 chars | 2894ms | Tuân thủ hoàn toàn Stylebook |
| `C4-009` | ambiguity | ambiguity | ✅ PASS | 28 chars | 2923ms | Tuân thủ hoàn toàn Stylebook |
| `C4-010` | ambiguity | ambiguity | ❌ FAIL | 27 chars | 2745ms | Cảnh 1: Nghi vấn bịa số liệu '4' không có trong kịch bản gốc |
| `C4-011` | visual_text | source_truth | ✅ PASS | 32 chars | 2757ms | Tuân thủ hoàn toàn Stylebook |
| `C4-012` | visual_text | ambiguity | ✅ PASS | 23 chars | 2641ms | Tuân thủ hoàn toàn Stylebook |
| `C4-013` | visual_text | out_of_scope | ✅ PASS | 20 chars | 3097ms | Tuân thủ hoàn toàn Stylebook |
| `C4-014` | visual_text | out_of_scope | ✅ PASS | 33 chars | 2814ms | Tuân thủ hoàn toàn Stylebook |
| `C4-015` | visual_text | out_of_scope | ✅ PASS | 25 chars | 2876ms | Tuân thủ hoàn toàn Stylebook |
| `C4-016` | consistency | domain_consistency | ✅ PASS | 29 chars | 7044ms | Tuân thủ hoàn toàn Stylebook |
| `C4-017` | consistency | domain_consistency | ✅ PASS | 26 chars | 4168ms | Tuân thủ hoàn toàn Stylebook |
| `C4-018` | consistency | domain_consistency | ✅ PASS | 25 chars | 3094ms | Tuân thủ hoàn toàn Stylebook |
| `C4-019` | single_scene_edit | domain_consistency | ✅ PASS | 20 chars | 2768ms | Tuân thủ hoàn toàn Stylebook |
| `C4-020` | single_scene_edit | domain_consistency | ✅ PASS | 23 chars | 2830ms | Tuân thủ hoàn toàn Stylebook |

---

## 4. Phân Tích Sâu Nguyên Nhân Lỗi (Failure Deep Dive & Root Cause)

Thay vì che giấu lỗi, nhóm đối mặt trung thực với số liệu kiểm thử thực tế để làm rõ các điểm mù của prompt sơ khởi:

### Lỗi #1 — Case `C4-010` (ambiguity: ambiguity)
- **Đầu vào kiểm thử:** *"Muốn so hai lần thử, hãy kiểm tra câu hỏi, thông tin gửi kèm, mô hình và cách chọn có giống nhau không."*
- **Các điểm vi phạm ghi nhận:**
  - ⚠️ `Cảnh 1: Nghi vấn bịa số liệu '4' không có trong kịch bản gốc`
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
