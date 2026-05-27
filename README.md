# Anh Ba Vote - Python Flask

Website vote public bằng Python Flask.

## Chạy local

```bash
pip install -r requirements.txt
python app.py
```

Mở trình duyệt:

```text
http://127.0.0.1:5000
```

## Cấu trúc file

```text
anh_ba_vote_python/
├── app.py
├── requirements.txt
├── Procfile
├── templates/
│   └── index.html
└── static/
    └── anh_ba_vote_image.jpg
```

## Public online

Có thể deploy lên Render, Railway hoặc VPS.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn app:app
```

Lưu ý: bản này dùng SQLite. Nếu host không giữ persistent disk, dữ liệu vote có thể mất khi redeploy/restart server. Nếu cần chạy nghiêm túc, nên đổi sang PostgreSQL hoặc Supabase.
