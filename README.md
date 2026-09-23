# Final-Project-2EZ4U-APP

**Nama:** Muhammad Rasyha Syauqi Islam  
**NRP:** 5024241066

## Deskripsi Project

**2EZ4U APP** merupakan project final mata kuliah Struktur Data dan Analisa Algoritma yang mengimplementasikan berbagai struktur data dan algoritma ke dalam sebuah aplikasi sederhana berbasis Python. Aplikasi ini dirancang sebagai sistem backend dan frontend sederhana untuk mengelola data pesanan pada layanan food delivery.

Project ini dikembangkan secara bertahap melalui beberapa milestone (M1–M6), dengan setiap milestone berfokus pada penerapan struktur data dan algoritma yang berbeda.

## Milestone 1 - Data Pesanan

Pada Milestone 1, project berfokus pada pengelolaan data pesanan menggunakan dua struktur data, yaitu **Array** dan **Linked List**.

Fitur yang telah diimplementasikan pada M1 meliputi:

- Melihat data pesanan menggunakan Array dan Linked List
- Menambahkan pesanan Reguler
- Menambahkan pesanan Prioritas
- Menambahkan pesanan VIP
- Menghapus pesanan
- Membandingkan waktu akses data antara Array dan Linked List
- Memuat data pesanan dari file `pesanan.csv`

Data pesanan memiliki beberapa atribut seperti `oid`, `pelanggan`, `resto`, `menu`, `harga`, `prioritas`, `t_masuk_detik`, `t_selesai_detik`, dan `status`.

### Struktur Data yang Digunakan

**Array**

- Akses data berdasarkan indeks
- Penambahan data
- Penyisipan data
- Penghapusan data
- Dynamic resizing ketika kapasitas penuh

**Linked List**

- Node dengan pointer `next`
- Head dan tail
- Akses data melalui traversal
- Penambahan data
- Penyisipan data
- Penghapusan data

## Teknologi

- Python
- Tkinter
- CSV
- Object-Oriented Programming (OOP)

## Struktur Project

```text
Project_Strukdat/
├── app.py
├── backend/
│   └── m1_pesanan.py
├── frontend/
│   └── ui.py
└── data/
    └── pesanan.csv
```
