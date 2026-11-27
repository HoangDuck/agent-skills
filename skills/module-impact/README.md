# `/module-impact`

Hỏi bằng lời xem một module, field, API, màn hình hay luồng ảnh hưởng tới đâu, cả trong module lẫn sang module khác. Kết quả viết dễ đọc; file và số dòng để ở phụ lục.

## Cài

Từ thư mục gốc của repo agent-skills:

```bash
./install.sh module-impact                    # cho mọi dự án trên máy
./install.sh module-impact --repo ../my-app   # vào một repo, để chia sẻ cho team qua git
```

Mở lại phiên Claude Code. Nếu repo gitignore `.claude/`, dùng `git add -f .claude/skills/module-impact`.

**Nâng cấp từ bản cũ:** xoá `.claude/commands/module-impact.md` và `.claude/skills/module-data-impact/`. File cấu hình `.claude/module-impact.project.md` vẫn dùng được như cũ.

Cần `git`, `python3` và `bash` (không cần cài thêm gói).

## Dùng

Chỉ một lệnh, hỏi bằng lời:

```
/module-impact checkout
/module-impact thiếu currency thì báo cáo bị gì
/module-impact api /api/orders/ còn được gọi không
/module-impact flow thanh toán trong module checkout
```

Không nói gì thêm thì skill kiểm rộng và đủ. Muốn hẹp hơn thì nói luôn trong câu:

| Nói thêm | Tác dụng |
|---|---|
| "nhanh" | trả lời ngắn, chỉ đếm, không mở hết |
| "trong module" / "liên module" | chỉ một phía |
| "chỉ backend" / tên repo | chỉ các repo đó |
| "trên nhánh dev" | đọc nhánh đó, không chuyển nhánh |
| "lưu file" | ghi báo cáo vào `docs/impact/` |

Gõ mỗi tên module là kiểm toàn bộ module, tốn token nhất, và tự ghi báo cáo ra file.

## Nên làm với dự án nhiều repo

Chép `project.template.md` thành `.claude/module-impact.project.md` trong repo rồi điền danh sách repo, vai trò người dùng, chỗ định nghĩa menu và route. Không có file này thì skill chỉ kiểm repo hiện tại và ghi rõ phần chưa kiểm.

## Giới hạn

- Phân tích tĩnh: không chạy app hay test, không đọc dữ liệu thật.
- Script xác nhận đoạn code nằm đúng `file:dòng`; còn "đang dùng" hay "không mở được" là phán đoán của agent, nên soát lại các chỗ quan trọng.
- Có hướng dẫn riêng cho Django, Go, Laravel, Strapi, Flutter (GetX, Bloc, Riverpod, GoRouter), Next.js / React và SwiftUI. Stack khác chạy theo quy trình chung; ghi quy ước riêng vào file cấu hình.

## Thành phần

| File | Vai trò |
|---|---|
| `SKILL.md` | Chọn việc từ câu hỏi, quy tắc chung |
| `references/trace.md` | Lần đường gọi, nhận biết code chết theo từng stack |
| `references/flow.md` | Ảnh hưởng giữa các bước trong module |
| `references/field.md` | Field thiếu hoặc đổi |
| `references/module.md` | Báo cáo toàn module, danh mục phụ thuộc |
| `references/output.md` | Cách trình bày |
| `references/relations.md` | Định dạng hàng quan hệ, cách chạy script |
| `scripts/relations.py` | Kiểm hàng, sinh ma trận và bản đồ, ingest |
| `scripts/cochange.sh` | File hay đổi cùng module theo lịch sử git |
| `project.template.md` | Mẫu cấu hình dự án |
