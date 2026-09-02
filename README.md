# EJIMAT Core — Backend

Backend REST API untuk **EJIMAT Core Desa Cimenyan**, sebuah platform terpusat untuk pengelolaan dan integrasi data desa.

Backend ini menyediakan layanan API yang digunakan oleh aplikasi web dan mobile untuk mengakses serta mengelola data kependudukan, wilayah, layanan desa, pengaduan, pembangunan, informasi desa, dan aktivitas sistem.

## 🚀 Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Uvicorn

## 📁 Project Structure

```text
EjimatBackend/
├── alembic/
├── app/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   └── main.py
├── venv/
├── .env
├── .gitignore
├── alembic.ini
└── requirements.txt
