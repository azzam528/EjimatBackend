# EJIMAT Core — Backend

Backend API untuk **EJIMAT Core Desa Cimenyan**, sebuah platform terintegrasi untuk pengelolaan data dan layanan administrasi desa.

Backend dibangun menggunakan **FastAPI** dengan **PostgreSQL** sebagai database dan **SQLAlchemy** sebagai ORM.

---

## 📌 Tentang EJIMAT Core

EJIMAT Core dirancang sebagai **single source of truth** untuk data desa, sehingga berbagai kebutuhan administrasi dan pelayanan dapat menggunakan sumber data yang terpusat.

Sistem mencakup pengelolaan:

- Data kependudukan
- Kartu Keluarga
- Anggota keluarga
- Wilayah administratif
- Layanan administrasi desa
- Pengajuan layanan
- Dokumen pengajuan
- Pengaduan masyarakat
- Informasi desa
- Pembangunan desa
- Manajemen pengguna dan hak akses
- Audit aktivitas

Backend ini berfungsi sebagai lapisan API yang menghubungkan database dengan aplikasi frontend/web dan mobile.

---

## 🏗️ Tech Stack

| Teknologi | Penggunaan |
|---|---|
| Python | Bahasa pemrograman |
| FastAPI | REST API framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Alembic | Database migration |
| Pydantic | Validation & serialization |
| Uvicorn | ASGI server |
| psycopg | PostgreSQL driver |

---

## 📂 Struktur Project

```text
EjimatBackend/
│
├── alembic/
│   └── Database migrations
│
├── app/
│   ├── core/
│   │   └── config.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── users.py
│   │   ├── wilayah.py
│   │   ├── kependudukan.py
│   │   ├── layanan.py
│   │   ├── pengaduan.py
│   │   ├── pembangunan.py
│   │   └── informasi.py
│   │
│   ├── repositories/
│   │   ├── penduduk_repository.py
│   │   ├── kartu_keluarga_repository.py
│   │   ├── anggota_keluarga_repository.py
│   │   ├── dusun_repository.py
│   │   ├── rw_repository.py
│   │   ├── rt_repository.py
│   │   ├── jenis_layanan_repository.py
│   │   └── pengajuan_layanan_repository.py
│   │
│   ├── schemas/
│   │   ├── kependudukan.py
│   │   ├── layanan.py
│   │   ├── users.py
│   │   └── wilayah.py
│   │
│   ├── services/
│   │   ├── penduduk_service.py
│   │   ├── kartu_keluarga_service.py
│   │   ├── anggota_keluarga_service.py
│   │   ├── dusun_service.py
│   │   ├── rw_service.py
│   │   ├── rt_service.py
│   │   ├── jenis_layanan_service.py
│   │   ├── pengajuan_layanan_service.py
│   │   └── duplicate_detection_service.py
│   │
│   ├── routers/
│   │   ├── health.py
│   │   ├── penduduk.py
│   │   ├── kartu_keluarga.py
│   │   ├── anggota_keluarga.py
│   │   ├── dusun.py
│   │   ├── rw.py
│   │   ├── rt.py
│   │   ├── jenis_layanan.py
│   │   ├── pengajuan_layanan.py
│   │   └── duplicate_detection.py
│   │
│   └── main.py
│
├── requirements.txt
├── README.md
└── .env
