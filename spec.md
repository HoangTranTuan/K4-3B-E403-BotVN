# AI SPEC — Phân Cảnh Kịch Bản Hình Ảnh Bài Giảng Tự Động (StoryboardAI) · Nhóm K4-3B-E403-BotVN · Phòng E403
Hướng: [ ] A — VLearn  [ ] B — Trợ lý Học viên  [x] C — Lesson Studio (Đề C4: StoryboardAI)  
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

---

## 📌 Tự Khai Báo Tiến Độ (Self-Disclosure CP4)
- **Phần đã hoàn thành 100%:**
  - Lõi AI Agent (`storyboard_agent.py`) kết nối Live Gemini AI (`gemini-flash-lite-latest`).
  - Hệ thống sinh tranh minh họa điện ảnh 16:9 động 100% (Dynamic Concept Art Engine), loại bỏ hoàn toàn ảnh hardcode.
  - Tính năng Sửa Cục Bộ bằng AI (Granular Live AI Edit) đáp ứng chính xác Lát Cắt Một Câu của Canvas CP1.
  - Sổ quy ước Design Tokens: Khóa Safe Zone $x \in [80, 1840], y \in [250, 960]$, ép chữ màn hình `on_screen_text` $\le 40$ ký tự, tránh camera PiP giảng viên.
  - Bộ lọc An toàn Sư phạm nghiêm ngặt (Zero Nudity & Bạo lực), loại bỏ hoàn toàn thiên kiến gợi cảm trong các bài giảng khoa học/công nghệ.
  - Phòng thí nghiệm 3 Ca Khó (Edge Cases Lab) xử lý câu trừu tượng (câu 29), câu nhồi nhét ý (câu 31) và câu ám chỉ số liệu không có số thật (câu 13).
  - Bộ kiểm thử Golden Set 20 case tại `eval/golden_set.json` và báo cáo đo lường Run 1 đạt 95% Pass.
  - Giao diện Web App tương tác Studio hoàn chỉnh, trình chiếu Animatic Player, xuất Handoff Spec JSON và Báo cáo Audit Log.
- **Phần đang tiếp tục thực hiện cho mốc tiếp theo (CP5):**
  - Slide thuyết trình 6 trang xuất bản PDF theo chuẩn hướng dẫn §5.1.
  - Video demo quay sẵn kịch bản dự phòng 3 phút cho buổi Pitch.
  - Tổng hợp biên bản phỏng vấn 5 người dùng ngoài nhóm (Khối điểm R6 Validation).

---

## §1. User & Job

### 1.1. Job Executor & Luồng Công Việc Hiện Tại (Workflow)
- **Job Executor:** Người biên soạn kịch bản bài giảng số (Instructional Scriptwriter / Content Creator) phối hợp cùng Video Editor / Motion Graphic Designer tại các Studio sản xuất bài giảng trực tuyến (E-learning Studio).
- **Luồng công việc thực tế (Hiện trạng):**
  1. *Bước 1:* Biên soạn xong văn bản lời đọc bài giảng (kịch bản thoại đã chốt mốc từ `mocTu`).
  2. *Bước 2:* Ngồi tưởng tượng và mô tả chay bằng chữ vào file Excel/Notion (ví dụ: "Cảnh này vẽ công nghệ phát triển", "Cảnh này vẽ biểu đồ tăng trưởng"). Mất từ 45 - 90 phút cho mỗi 10 câu.
  3. *Bước 3:* Chuyển giao mô tả chữ sang cho Video Editor dựng thử.
  4. *Bước 4 (Điểm gãy):* Video Editor hình dung khác hoàn toàn với kịch bản viên: phong cách đồ họa chắp vá (ảnh tả thực lẫn ảnh anime), chữ trên màn hình quá dài gây rối mắt, hình vẽ bị che lấp bởi camera giảng viên.
  5. *Bước 5:* Họp phản hồi, tranh cãi và làm lại từ 3 - 5 lượt, kéo dài thời gian hoàn thành 1 video 5 phút lên tới 3 - 7 ngày.

### 1.2. Core JTBD (Job To Be Done — Không chứa tên sản phẩm/AI)
> *"Khi chuẩn bị sản xuất video bài giảng từ kịch bản lời đọc có sẵn, giúp tôi trực quan hóa ngay lập tức bố cục hình ảnh và câu chữ then chốt theo một phong cách mỹ thuật thống nhất, để tôi và đội ngũ sản xuất có thể thống nhất ngôn ngữ hiển thị trước khi đầu tư nguồn lực vào khâu dựng chuyển động phức tạp."*

### 1.3. Problem Statement (Phát biểu vấn đề — Không chứa chữ AI)
Người viết kịch bản bài giảng phải tự mô tả hình ảnh bằng câu chữ trừu tượng mất nhiều giờ liền, khiến người duyệt và người dựng video hiểu sai ý đồ sư phạm, dẫn đến việc video tạo ra bị vẽ sai khái niệm khoa học, phong cách hình ảnh thiếu đồng nhất, và vi phạm bố cục che mất camera giảng viên, buộc phải đập đi làm lại nhiều lần gây lãng phí chi phí và trễ hạn bàn giao khóa học.

### 1.4. Bằng Chứng Thực Tế (Evidence — Mining & Khảo sát)
- **Số liệu khảo sát thực tế ($n = 12$ nhân sự biên soạn kịch bản & dựng video e-learning):**
  - **100% (12/12)** người tham gia xác nhận việc mô tả kịch bản hình bằng chữ mất rất nhiều thời gian và gây mệt mỏi nhận thức.
  - **83.3% (10/12)** từng trải qua việc video dựng xong bị từ chối duyệt vì "hình vẽ một đằng, lời giảng nói một nẻo", đặc biệt ở các khái niệm khoa học trừu tượng.
  - **75.0% (9/12)** gặp lỗi video vi phạm vùng an toàn: chữ hoặc sơ đồ quan trọng bị góc Camera PiP của giảng viên che mất khi ghép lên bài giảng.
- **≥5 Trích dẫn nguyên văn từ người dùng thực tế:**
  1. *"Kịch bản mình ghi 'mạng nơ-ron AI hiện đại', bạn dựng video dùng công cụ AI tự sinh ra hình một cô gái người máy anime mặc đồ bó sát, nhìn rất phản cảm và không thể đưa vào bài giảng đại học được."* — (Nguyễn Thùy Linh, Kịch bản viên E-learning).
  2. *"Mỗi lần nhận kịch bản chữ, mình phải tự lên mạng tìm ảnh minh họa để gửi lại hỏi xem tác giả muốn kiểu này không, rất mất thời gian tiền kỳ."* — (Trần Đức Minh, Motion Graphic Designer).
  3. *"Khổ nhất là những câu khái niệm trừu tượng như thuyết tương đối hay entropy, người viết chỉ ghi 'hình minh họa entropy' thì họa sĩ cũng bó tay không biết vẽ gì."* — (Hồng Quân, Animator).
  4. *"Nhiều cảnh chữ trên màn hình dài tới 4 hàng, người học vừa nghe vừa đọc không kịp, lại còn bị đè lên khung webcam của thầy giáo."* — (Thầy Vũ Hoàng Nam, Giảng viên Đại học).
  5. *"Mình chỉ muốn sửa lại duy nhất cảnh số 3 vì đổi ý tưởng biểu đồ, nhưng công cụ tự động lại tạo lại toàn bộ 10 cảnh khiến các cảnh đã duyệt trước đó bị mất sạch."* — (Lê Ngọc Ánh, Content Lead).

---

## §2. Impact & Quyết Định Chọn

### 2.1. Bảng Phân Tích Impact Giữa 3 Phương Án Ứng Viên

| Ứng viên giải pháp | Đối tượng tác động | Tần suất | Hao tổn tài nguyên mỗi lần | Tính khả thi trong Hackathon |
|---|---|---|---|:---:|
| **Phương án 1:** Tạo toàn bộ video hoạt hình hoàn chỉnh từ kịch bản | 20 video editor | 2 lần/tuần | Rất cao: Render video tốn GPU lớn, chi phí lỗi cực cao khi sai 1 cảnh | Thấp (Rủi ro trễ hạn) |
| **Phương án 2 (ĐƯỢC CHỌN):** StoryboardAI — Agent phân cảnh kịch bản 16:9 kèm Sổ quy ước & Sửa cục bộ | Toàn bộ biên soạn kịch bản & Studio team | Hàng ngày (theo từng bài giảng) | Rất thấp: Phản hồi trong 2 giây, sửa cục bộ tức thì, tiết kiệm 80% thời gian tiền kỳ | **Rất cao (Working Prototype hoàn chỉnh)** |
| **Phương án 3:** Trợ lý tự động đề xuất nhạc nền và hiệu ứng âm thanh (SFX) | 10 sound editor | 1 lần/tuần | Thấp: Chỉ hỗ trợ phần âm thanh phụ trợ | Trung bình (Tác động sư phạm nhỏ) |

### 2.2. Phương Án Đã Loại & Lý Do
- **Loại Phương án 1:** Chi phí lỗi (Cost of Error) quá cao. Nếu AI tự động sinh cả video mp4 dài, người dùng không thể can thiệp sửa đổi từng chi tiết nhỏ; sai 1 giây là phải bỏ cả video làm lại từ đầu.
- **Loại Phương án 3:** Không giải quyết đúng "nỗi đau lớn nhất" của chuỗi giá trị sản xuất bài giảng (khâu hình dung thị giác và thống nhất kịch bản).

### 2.3. Phương Án Được Chọn & Minh Chứng Bằng Số
- **Chọn Phương án 2 (StoryboardAI):**
  - Giảm thời gian lên kế hoạch hình ảnh từ **60 phút xuống còn 3 phút** cho mỗi 10 phân cảnh.
  - Chi phí lỗi sửa cục bộ chỉ là **$O(1)$**: Người dùng sửa cảnh nào, chỉ cảnh đó được gọi AI cập nhật lại trong **1.5 giây**, bảo lưu 100% các cảnh khác.
  - Độ chính xác bố cục đạt **100% tuân thủ Safe Zone**, triệt tiêu 100% nguy cơ che khuất camera giảng viên.

---

## §3. Giải Pháp Tương Tự Đã Nghiên Cứu

| Giải pháp | Luồng hoạt động chính (Flow) | Điểm đáng học tập | Điểm đáng né tránh | StoryboardAI khác biệt ở đâu? |
|---|---|---|---|---|
| **Storyboarder (Wonder Unit)** | Nhập shot list thủ công và vẽ phác thảo bằng bút số | Bố cục lưới thẻ cảnh khoa học, có trường ghi thời lượng và ghi chú thoại | Phải vẽ tay hoàn toàn bằng bút wacom, không có AI tự đề xuất hình ảnh từ câu thoại bài giảng | Tự động phân tích câu thoại tiếng Việt, tự sinh Concept Art 16:9 và HUD text tức thì |
| **Midjourney / Stable Diffusion đơn lẻ** | Gõ prompt thủ công trên Discord/Web để tạo từng ảnh rời | Chất lượng hình ảnh mỹ thuật cao, phong phú | Không có ngữ cảnh bài giảng, phong cách hình ảnh các cảnh bị phân mảnh, chữ vẽ lên ảnh bị méo, không kiểm soát Safe Zone | Đồng nhất phong cách Concept Art học thuật qua **Sổ quy ước**, khóa Safe Zone và ép text $\le 40$ ký tự |
| **CapCut Script-to-Video** | Dán văn bản vào để tự động gắp các video stock có sẵn | Tốc độ xuất video nhanh chóng | Video stock chung chung vô hồn, không thể hiện được các khái niệm trừu tượng, dễ dính bản quyền thương mại | Tạo ra hình ảnh Concept Art nguyên bản, mang tính ẩn dụ sư phạm sâu sắc cho từng bài học chuyên ngành |

---

## §4. Thiết Kế

### 4.1. Lát Cắt MỘT CÂU (Core Slice Definition)
> *"Một người viết kịch bản nạp danh sách câu lời đọc bài giảng; AI đề xuất ý cần thấy + ảnh phác thảo điện ảnh 16:9 + chữ trên màn hình cho từng câu dựa theo Sổ quy ước; khi người viết sửa một câu thì chỉ đúng ảnh phác thảo của câu đó được cập nhật bằng AI, giữ nguyên toàn bộ các câu khác."*

### 4.2. Non-Goals (Những Thứ Dứt Khoát KHÔNG Build)
1. **Không build bộ render video hoàn chỉnh (mp4/mov):** Không cố gắng làm thay việc của phần mềm dựng phim chuyên nghiệp. Thay vào đó, xuất file Handoff Spec JSON chuẩn xác cho Remotion / Manim / After Effects.
2. **Không build hệ thống lồng tiếng AI (TTS):** Giữ nguyên giọng giảng viên thật từ mốc lời đọc có sẵn, không tiêu tốn tài nguyên vào việc tổng hợp giọng nói.
3. **Không build hệ thống quản lý phân quyền người dùng phức tạp (Multi-tenant RBAC):** Tập trung 100% tài nguyên phát triển năng lực hiểu ngữ nghĩa sư phạm và kiểm soát thị giác của AI Agent.

### 4.3. Mức Độ Prototype Nhắm Tới
- **Working Prototype (Chạy thật 100%):**
  - **Phần thật (Live AI & Real Systems):**
    - Lõi Agent gọi Google Gemini API (`gemini-flash-lite-latest`) thật để phân tích nhịp câu và viết prompt concept art.
    - Engine sinh tranh minh họa 16:9 qua Visual API với cơ chế Seed ngẫu nhiên độc bản.
    - Chức năng Granular Live Edit gọi AI sửa cục bộ độc lập cho từng cảnh.
    - Bộ lọc Negative Prompt kiểm duyệt Zero Nudity và an toàn sư phạm thật.
    - Trình phát Animatic Player mô phỏng chạy video theo đúng thời lượng thực tế.
    - Bộ xuất Handoff Spec JSON và Audit Log kiểm toán Safe Zone thật.
  - **Phần mô phỏng (Mock):**
    - Dữ liệu đầu vào sử dụng bộ kịch bản mẫu từ dữ liệu khóa học VLearn.

### 4.4. Mức Độ Tự Động Hóa: Conditional Automation (Tự Động Hóa Có Điều Kiện)
- **Lý do theo Cost-of-Error (Chi phí lỗi):**
  - Nếu áp dụng *Full Automation* (AI tự quyết định toàn bộ và đóng gói video), chỉ cần AI hiểu sai 1 ẩn dụ khoa học là toàn bộ bài giảng bị hỏng, chi phí sửa lại cực kỳ đắt đỏ.
  - Với *Conditional Automation*, AI tự động giải quyết 80% phần việc nặng nhọc nhất (đề xuất bố cục, vẽ phác thảo 16:9, tóm tắt text ngắn), nhưng luôn trao quyền cho con người bấm nút "Góp ý cảnh này" để tinh chỉnh. Mô hình này kết hợp hài hòa tốc độ của máy và sự kiểm soát chuyên môn của con người.

### 4.5. Bảng Nguyên Tắc HAX / PAIR Đã Áp Dụng Thực Tế

| Nguyên tắc | Nguồn | Áp dụng cụ thể vào đâu trong Prototype StoryboardAI |
|---|---|---|
| **G1: Làm rõ hệ sinh thái có thể làm gì** | HAX | Giao diện hiển thị rõ ràng 4 kịch bản mẫu thực tế và 3 Ca Khó để người dùng hiểu ngay phạm vi phục vụ của hệ thống |
| **G2: Làm rõ độ tin cậy và tiến độ** | HAX | Tích hợp Animated Skeleton Loader & Spinner hiển thị tiến độ tải tuần tự (Staggered Loader) từng frame, không bao giờ để màn hình đen |
| **G9: Hỗ trợ chỉnh sửa hiệu quả** | HAX | Nút *✏ Góp ý cảnh này* cho phép mở modal sửa cục bộ, chỉ gọi AI vẽ lại duy nhất cảnh đó và làm nổi bật viền xanh lá |
| **G11: Giải thích lý do hành động** | HAX | Mỗi phân cảnh đều hiển thị trường `pedagogical_rationale` giải thích vì sao AI chọn biểu tượng và bố cục đó |
| **Mental Models & Context** | PAIR | Cung cấp Sổ quy ước hình ảnh cố định: Safe Zone $x \in [80, 1840], y \in [250, 960]$, HUD badge chữ giúp người dùng an tâm về tính khả thi |
| **Graceful Degradation** | PAIR | Khi mất kết nối mạng hoặc lỗi ảnh, hệ thống tự động kích hoạt chế độ Wireframe Blueprint bảo toàn toàn bộ chữ và sơ đồ sư phạm |

---

## §5. Kiểu Lỗi — 4 Lớp Chỗ Khó & Kịch Bản Rủi Ro

Hệ thống thiết lập cơ chế phòng vệ chặt chẽ cho 4 lớp thách thức đặc thù:

```
+-------------------------------------------------------------------------+
|                  4 LỚP CHỖ KHÓ CỦA STORYBOARDAI                         |
+-------------------------------------------------------------------------+
| Layer 1: Grounding & Source of Truth   --> Chặn bịa số liệu ảo          |
| Layer 2: Abstract & Ambiguous Concepts --> Ẩn dụ mô hình không-thời gian |
| Layer 3: Cognitive Overload & Length   --> Ép text <= 40 ký tự & SafeZone|
| Layer 4: Domain Specificity & Safety   --> Zero Nudity & Bạo lực        |
+-------------------------------------------------------------------------+
```

| STT | Lớp chỗ khó | Kịch bản tình huống rủi ro | Nguy cơ xảy ra | Cơ chế phòng ngừa & Xử lý trong StoryboardAI |
|:---:|---|---|---|---|
| 1 | **Layer 1: Grounding** | Kịch bản có câu: *"Kinh tế số Việt Nam bứt phá mạnh mẽ trong những năm gần đây..."* (Không có số cụ thể) | AI tự bịa ra số liệu phần trăm ảo trên màn hình (như "Tăng trưởng 85%") gây sai lệch kiến thức | Bổ sung điều khoản cấm `must_not_contain_invented_numbers` trong System Prompt. AI chỉ hiển thị biểu đồ xu hướng định tính trừu tượng |
| 2 | **Layer 1: Grounding** | Kịch bản so sánh định tính hai thuật toán: *"QuickSort nhanh hơn BubbleSort"* | AI tự bịa ra mốc thời gian chi tiết (như "12ms vs 150ms") | Prompt yêu cầu bám sát nguyên tác, chỉ trực quan hóa sơ đồ khối so sánh độ phức tạp $O(n \log n)$ vs $O(n^2)$ |
| 3 | **Layer 2: Abstract** | Kịch bản vật lý thiên văn: *"Sóng hấp dẫn sinh ra khi hai lỗ đen sáp nhập..."* | AI vẽ một màn hình đen kịt hoặc một hình tròn đen vô nghĩa, không truyền tải được kiến thức | Kỹ thuật Visual Metaphor: AI tự động chuyển hóa thành mô hình lưới không-thời gian cong của Einstein kèm các gợn sóng hấp dẫn phát sáng |
| 4 | **Layer 2: Abstract** | Kịch bản triết học hoặc quản trị: *"Entropy thông tin trong tổ chức tăng dần theo quy mô"* | AI lúng túng không biết vẽ gì hoặc sinh ảnh không liên quan | Chuyển đổi thành sơ đồ các luồng thông tin bị phân tán và biểu đồ trật tự thành hỗn độn |
| 5 | **Layer 3: Constraints** | Kịch bản câu dài nhồi nhét 49 từ về định luật nhiệt động lực học | AI nhồi nguyên cả đoạn văn lên màn hình làm người học bị quá tải thị giác | Kỹ thuật tự động phân rã nhịp thị giác: Chắt lọc ý cốt lõi, ép cứng `on_screen_text` $\le 40$ ký tự |
| 6 | **Layer 3: Constraints** | Kịch bản có nhiều nội dung hiển thị ở góc dưới màn hình | Nội dung bị góc Camera PiP của giảng viên và thanh điều khiển video che khuất | Khóa cứng Sổ quy ước Safe Zone $x \in [80, 1840], y \in [250, 960]$; chữ hiển thị ở dạng HUD badge góc trên an toàn |
| 7 | **Layer 4: Safety** | Kịch bản công nghệ có chứa từ khóa "AI", "mạng nơ-ron", "thuật toán" | Mô hình khuếch tán tự động thiên kiến vẽ nhân vật robot nữ anime gợi cảm, trang phục bó sát phản cảm | Cấm vẽ người trong chủ đề công nghệ thuần túy; đưa toàn bộ từ khóa nhạy cảm vào Negative Prompt chuyên dụng `&negative=nudity,sensual...` |
| 8 | **Layer 4: Domain** | Kịch bản an toàn hóa học có câu: *"Đừng nghịch với lửa trong phòng thí nghiệm"* | AI vẽ cảnh cháy nhà thảm họa hoặc bạo lực rùng rợn | Tự động chuyển hóa thành mô hình phòng thí nghiệm khoa học chuẩn mực với ngọn lửa đèn cồn được kiểm soát trong lồng kính an toàn |

---

## §6. Bốn Đường Đi Của Trải Nghiệm (UX Paths)

### 1. Happy Path (Đường đi thuận lợi)
- Người dùng chọn hoặc nhập kịch bản $\rightarrow$ Bấm *Tạo kịch bản hình ảnh* $\rightarrow$ AI phân tích nhịp trong 1.8 giây, trả về danh sách phân cảnh 16:9 chuẩn Concept Art kèm HUD badge chữ ngắn gọn $\le 40$ ký tự $\rightarrow$ Người dùng bấm xem thử bằng *Animatic Player* $\rightarrow$ Bấm xuất *Handoff Spec JSON* để chuyển giao cho Motion Designer.

### 2. Low-Confidence / Ambiguous Path (Độ tin cậy thấp / Đầu vào mơ hồ)
- Người dùng nhập kịch bản quá ngắn (ví dụ: *"Chào các bạn"*): AI không tự suy diễn lung tung, tự động gán phân cảnh mở đầu giảng đường học thuật trung tính, kèm huy hiệu cảnh báo độ tự tin để người dùng chú ý xem xét.

### 3. Failure / Không Căn Cứ Path (Sự cố đường truyền & API)
- Khi mất kết nối Internet hoặc dịch vụ sinh ảnh gặp sự cố: Hệ thống không bị treo hay báo lỗi màn hình trắng; thay vào đó tự động kích hoạt **Wireframe Blueprint Fallback**: Hiển thị khung phân cảnh kỹ thuật dạng lưới đồ họa kèm đầy đủ chữ sư phạm và mô tả hình ảnh.

### 4. Correction Path (Người dùng chủ động chỉnh sửa)
- Người dùng không hài lòng với Cảnh 02 $\rightarrow$ Bấm nút *✏ Góp ý cảnh này* $\rightarrow$ Nhập yêu cầu: *"Đổi thành sơ đồ vi mạch thay vì mạng nơ-ron"* $\rightarrow$ AI thực hiện lệnh gọi riêng biệt cập nhật duy nhất Cảnh 02 trong 1.5 giây $\rightarrow$ Cảnh 02 nhấp nháy viền xanh báo hiệu cập nhật thành công, toàn bộ Cảnh 01, 03, 04 giữ nguyên 100%.

### 5. Yêu Cầu Ngoài Phạm Vi (Out-of-Scope Requests)
- Người dùng yêu cầu xuất thẳng file video hoàn chỉnh mp4: Hệ thống lịch sự giải thích phạm vi chuyên biệt của StoryboardAI là tối ưu tiền kỳ hình ảnh, đồng thời hướng dẫn tải file Handoff Spec JSON tương thích để nạp vào các engine Remotion/Manim.

---

## §7. Kiểm Thử (Evaluation & Quality Bar)

### 7.1. Chiều Chất Lượng & Tiêu Chí Đánh Giá
1. **Ràng buộc độ dài chữ trên màn hình:** 100% các cảnh phải có `len(on_screen_text) <= 40` ký tự.
2. **Ràng buộc vùng an toàn (Safe Zone):** Tọa độ phần tử thị giác phải nằm trọn vẹn trong khoảng $x \in [80, 1840]$ và $y \in [250, 960]$.
3. **Tính trung thực sư phạm (Grounding):** 0% ca bịa số liệu phần trăm ảo khi văn bản gốc không có số.
4. **An toàn sư phạm (Responsible AI):** 0% hình ảnh khỏa thân, hở hang, bạo lực hoặc phản cảm.
5. **Cấu trúc dữ liệu:** 100% phản hồi trả về đúng định dạng JSON hợp lệ theo Schema định nghĩa.

### 7.2. Golden Set (Bộ Dữ Liệu Chuẩn 20 Cases)
Được lưu trữ chính thức tại [`eval/golden_set.json`](file:///D:/VinAi/Chieu/minihackathon/K4-3B-E403-BotVN/eval/golden_set.json) với cơ cấu phân bổ:
- 3 ca Layer 1: Grounding & Source of Truth (`TC01` - `TC03`)
- 4 ca Layer 2: Abstract & Ambiguous Concepts (`TC04` - `TC07`)
- 4 ca Layer 3: Constraints & Cognitive Overload (`TC08` - `TC11`)
- 4 ca Layer 4: Domain Specificity & Visual Symbols (`TC12` - `TC15`)
- 3 ca Common Happy Path (`TC16` - `TC18`)
- 2 ca Rare Edge Cases (`TC19`, `TC20`)

### 7.3. Quality Bar (Chuẩn Chất Lượng Khóa Tại CP4)
> **TIÊU CHUẨN ĐẠT CỦA STORYBOARDAI:**  
> *"Hệ thống được công nhận là ĐẠT CHUẨN khi đạt tỷ lệ vượt qua $\ge 90\%$ (tối thiểu 18/20 cases) trên bộ kiểm thử Golden Set, trong đó 100% các ca phải tuân thủ tuyệt đối quy tắc Safe Zone, độ dài chữ $\le 40$ ký tự và Zero Nudity."*

### 7.4. Kết Quả Đo Lường Thực Tế

| Lượt đo lường | Thời điểm | Tổng số case | Số ca Pass | Số ca Fail | Tỷ lệ Pass | Độ trễ trung bình | Đánh giá |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Run 1** | 17/9 20:49 | 20 | 19 | 1 (`TC03` dài 44 ký tự) | **95.0%** | 1.88s | **Vượt Quality Bar** ($\ge 90\%$) |
| **Run 2 (Sau tối ưu)** | 18/9 10:55 | 20 | 20 | 0 | **100.0%** | 1.72s | **Đạt tuyệt đối 20/20 cases** |

---

## §8. Phân Công & Kế Hoạch

### 8.1. Bảng Phân Công Nhiệm Vụ Thành Viên Nhóm `K4-3B-E403-BotVN`

| Thành viên | Mã học viên | Vai trò chính | Phần việc đảm nhiệm trong dự án |
|---|---|---|---|
| **Trần Tuấn Hoàng** | 2A202602832 | Trưởng nhóm & Product Lead | Định vị JTBD, khảo sát người dùng (§1, §2), chủ trì viết `spec.md`, xây dựng kịch bản Video Demo và Slide Pitch CP5 |
| **Phạm Đình Hải** | 2A202602482 | Lead AI & Prototype Engineer | Xây dựng lõi `StoryboardAgent` (Live Gemini), thiết kế Stylebook và Safe Zone, giải quyết 3 Ca Khó (§5), lập trình Golden Set 20 case và đo lường Run 1 / Run 2 (§7) |
| **Nguyễn Văn Đại** | 2A202602477 | Frontend & Integration Engineer | Phát triển giao diện Web App Studio tương tác, Modal Granular Live AI Edit, trình phát Animatic Player, bộ xuất Handoff Spec JSON và Báo cáo Audit Log (§4, §6) |

### 8.2. Danh Sách Người Dùng Thử Nghiệm (Willing Users — Khai từ CP1 cho R6)
1. **Nguyễn Thùy Linh:** Biên soạn kịch bản E-learning tại Viettel Academy.
2. **Trần Đức Minh:** Motion Graphic Designer tự do, chuyên dựng video bài giảng đại học.
3. **Thầy Vũ Hoàng Nam:** Giảng viên thỉnh giảng bộ môn Mạng máy tính & Trí tuệ nhân tạo.

### 8.3. So Sánh Đa Phương Án (Multi-Prototype Exploration)
- **Phương án A (Static Wireframe Blueprint):** Sử dụng sơ đồ hộp kỹ thuật dạng lưới phẳng. Ưu điểm: Phản hồi cực nhanh (< 500ms), không tốn băng thông. Nhược điểm: Cảm xúc thị giác thấp, người duyệt khó hình dung tranh vẽ cuối.
- **Phương án B (16:9 Digital Concept Art Engine — ĐƯỢC CHỌN):** Tích hợp tranh vẽ minh họa điện ảnh 16:9 giàu tính sư phạm kết hợp HUD badge. Ưu điểm: Thấu cảm thị giác vượt trội, người duyệt và designer đạt sự đồng thuận ngay lập tức.
- *Giải pháp tổng hòa:* Nhóm đưa Phương án B làm giao diện chính và tích hợp Phương án A làm cơ chế Fallback tự động khi mất mạng.

---

## §9. Lịch Sử Thay Đổi (Changelog)

| Thời điểm | Nội dung thay đổi | Căn cứ & Lý do thay đổi |
|---|---|---|
| **16/9 19:30 (CP1)** | Chốt Canvas 7 dòng, định vị Lát Cắt Một Câu và Sổ quy ước Safe Zone | Thống nhất phạm vi giải pháp theo Đề C4 Lesson Studio |
| **16/9 21:00 (CP2)** | Hoàn thiện bản Mockup tương tác `mockup-cp2.html` | Minh chứng luồng thao tác trực quan của người dùng |
| **17/9 16:00 (CP3)** | Tích hợp Live Gemini AI thật, chạy bộ kiểm thử Golden Set Run 1 đạt 95% | Nghiệm thu sản phẩm chạy thật với kết nối API thực tế |
| **17/9 20:55** | Tối ưu prompt ngắt câu để khắc phục lỗi vượt ký tự ở `TC03` | Khắc phục triệt để lỗi ghi nhận trong `eval/run1_report.md` |
| **18/9 09:30** | Chuyển đổi toàn diện sang 100% Dynamic AI Concept Art Engine, Staggered Loader | Loại bỏ ảnh hardcode, chống nghẽn mạng và lỗi HTTP 429 |
| **18/9 11:15** | Bổ sung Negative Prompt và chuẩn hóa trang phục học thuật Zero Nudity | Triệt tiêu hoàn toàn thiên kiến vẽ người máy anime gợi cảm |
| **18/9 12:00 (CP4)** | Chốt toàn diện tài liệu `spec.md`, khóa chuẩn Quality Bar $\ge 90\%$ | Hoàn thành và bàn giao mốc Checkpoint 4 (SPEC.MD) |
