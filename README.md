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


