# `/walkthrough` (V1, prototype)

AI viết code rất nhiều, đọc tay không kịp. Skill này dẫn bạn đi qua code theo ba góc nhìn, kèm vài chỗ đáng tự đọc:

- **Business flow:** làm gì cho ai, các bước nghiệp vụ, quy tắc, kết quả.
- **Implementation flow:** code chạy qua những lớp nào, dữ liệu đi đâu, lỗi được xử lý ra sao (kèm sequence diagram).
- **Usage flow:** tìm tính năng ở đâu, gọi API thế nào, cần cấu hình gì, thử bằng tay ra sao.

## Dùng

```
/walkthrough                      # nhánh hiện tại so với nhánh chính
/walkthrough nhánh feature/cart
/walkthrough thay đổi chưa commit
/walkthrough luồng checkout       # tính năng có sẵn, không phải diff
/walkthrough nhánh này, nhanh     # chỉ tổng quan
```

Với một thay đổi, skill còn cho biết: bước nào MỚI / ĐỔI / BỎ; phần mới đã được nối vào app chưa; và rà các lỗi hay gặp ở code AI (code không ai gọi, trùng helper, hard-code, nuốt lỗi, lệch field client và server, thiếu kiểm quyền…).

Kết quả dài thì ghi vào `docs/walkthrough/<tên>-<ngày>.md`, trong chat chỉ có bản ngắn.

## Cài

```bash
./install.sh walkthrough                    # cho mọi dự án
./install.sh walkthrough --repo ../my-app   # vào một repo
```

## Thành phần

| File | Vai trò |
|---|---|
| `SKILL.md` | Nhận biết thay đổi hay tính năng, các bước làm |
| `references/flows.md` | Cách dựng ba luồng, failure walk, quy tắc lần code |
| `references/change.md` | Xác định range, before/after, checklist code AI |
| `references/output.md` | Bố cục câu trả lời |
| `scripts/diffmap.sh` | Bản đồ thay đổi theo thư mục, ẩn file sinh tự động và lock |

## Giới hạn V1

- Đọc tĩnh, không chạy app.
- "PR số N" cần nhánh của PR đã có ở máy; chưa tự kéo từ GitHub/GitLab.
- Chưa chạy thử trên dự án thật; góp ý sau lần dùng đầu để làm V2.
