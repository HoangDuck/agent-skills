# Agent skills

Bộ skill cho Claude Code của Duc. Mỗi skill là một thư mục trong `skills/`.

## Danh sách

| Skill | Dùng để | Gọi |
|---|---|---|
| [module-impact](skills/module-impact/README.md) | Kiểm ảnh hưởng của module, field, API, màn hình, flow: trong module và liên module | `/module-impact <hỏi bằng lời>` |
| [walkthrough](skills/walkthrough/README.md) (V1) | Giải thích code (nhất là thay đổi AI vừa viết) theo business, implementation và usage flow | `/walkthrough <nhánh, PR, tính năng…>` |

## Cài

```bash
git clone <url repo này> agent-skills && cd agent-skills
./install.sh --list                          # xem có gì
./install.sh module-impact                   # cài cho mọi dự án (~/.claude/skills)
./install.sh module-impact --repo ../my-app  # cài vào một repo, để chia sẻ cho team qua git
./install.sh --all                           # cài tất cả
```

Mở lại phiên Claude Code để nhận skill. Cập nhật: `git pull` rồi chạy lại `install.sh` (có hỏi trước khi ghi đè).

## Thêm skill mới

1. Tạo `skills/<tên-skill>/SKILL.md`. Frontmatter có `name: <tên-skill>` (trùng tên thư mục) và `description` bắt đầu bằng "Use when…", kèm câu kích hoạt tiếng Việt nếu cần.
2. Tài liệu chi tiết để trong `references/`, script trong `scripts/`, hướng dẫn cho người trong `README.md` của skill.
3. Chạy `scripts/check.sh` cho tới khi in `OK`.
4. Thêm một dòng vào bảng **Danh sách** ở trên, rồi commit.

Quy ước: tên thư mục dạng `kebab-case`, không chứa "claude" hay "anthropic"; giữ `SKILL.md` ngắn, phần nặng để ở `references/`.
