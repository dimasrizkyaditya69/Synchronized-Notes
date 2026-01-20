# 📝 Synchronized Notes

Synchronized Notes adalah aplikasi **desktop pencatatan** yang memungkinkan pengguna mengelola catatan dalam bentuk **workspace** dan **page**, mirip konsep Notion, namun dibuat sederhana dan fokus untuk penggunaan personal.

Aplikasi ini dibangun menggunakan **Python** untuk sisi frontend desktop dan **Supabase** sebagai backend (database + authentication).

---

## ✨ Fitur Utama

- 🔐 **Authentication**
  - Login dan register menggunakan email & password
  - Autentikasi aman berbasis Supabase Auth

- 🗂️ **Workspace Management**
  - Membuat dan menghapus workspace
  - Setiap workspace bersifat personal (non-kolaboratif)

- 📄 **Page / Notes**
  - Membuat, membuka, mengedit, dan menghapus page
  - Page tersimpan langsung ke database
  - Mendukung status page (pending / done)

- 🔍 **Search & Filter**
  - Pencarian page berdasarkan judul
  - Filter berdasarkan status

- 🗑️ **Delete dengan Konfirmasi**
  - Penghapusan workspace dan page dilindungi dialog konfirmasi

---

## 🛠️ Teknologi yang Digunakan

- **Python 3**
- **PySide6** — GUI framework desktop
- **Supabase**
  - PostgreSQL Database
  - Supabase Authentication
  - Row Level Security (RLS)

---

## 📂 Struktur Project

