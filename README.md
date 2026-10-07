# Final-Project-2EZ4U-APP

**Nama:** Muhammad Rasyha Syauqi Islam  
**NRP:** 5024241066

## Deskripsi Project

**2EZ4U APP** merupakan project final mata kuliah **Struktur Data dan Analisa Algoritma (EC234303)** yang mengimplementasikan berbagai struktur data dan algoritma ke dalam sebuah aplikasi berbasis Python.

Aplikasi ini dirancang sebagai sistem sederhana untuk mengelola data pesanan pada layanan food delivery. Project dikembangkan secara bertahap melalui beberapa milestone (M1–M6), dengan setiap milestone berfokus pada penerapan struktur data dan algoritma yang berbeda.

---

# Milestone 1 - Data Pesanan

Pada Milestone 1, project berfokus pada pengelolaan data pesanan menggunakan dua struktur data, yaitu **Array** dan **Linked List**.

### Fitur M1

- Melihat data pesanan menggunakan Array
- Melihat data pesanan menggunakan Linked List
- Menambahkan pesanan Reguler
- Menambahkan pesanan Prioritas
- Menambahkan pesanan VIP
- Menghapus pesanan
- Membandingkan waktu akses Array dan Linked List
- Memuat data pesanan dari file `pesanan.csv`

Data pesanan memiliki atribut:

- `oid`
- `pelanggan`
- `resto`
- `menu`
- `harga`
- `prioritas`
- `t_masuk_detik`
- `t_selesai_detik`
- `status`

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

---

# Milestone 2 - Antrean dan Stack

Pada Milestone 2, project berfokus pada penerapan **Stack**, **Queue**, sistem kasir menggunakan **postfix**, serta mekanisme **Undo dan Redo**.

### Struktur Data yang Digunakan

**Stack**

Stack digunakan sebagai dasar untuk:

- Operasi `push`
- Operasi `pop`
- Operasi `peek`
- Mengecek kondisi kosong
- Sistem Undo
- Sistem Redo
- Mesin kasir postfix

**Queue**

Terdapat dua implementasi antrean:

- Antrean Naif
- Antrean Melingkar (Circular Queue)

### Fitur M2

#### 1. STACK - POSTFIX (MESIN KASIR)

Digunakan untuk mengubah ekspresi infix menjadi postfix dan menghitung hasil ekspresi menggunakan Stack.

Pengujian mencakup:

- Ekspresi tanpa kurung
- Ekspresi dengan kurung
- Operator `-`
- Operator `/`
- Kurung bersarang
- Bilangan dengan lebih dari satu digit

#### 2. STACK - UNDO

Digunakan untuk membatalkan aksi terakhir pada sistem antrean.

#### 3. STACK - REDO

Digunakan untuk mengulangi kembali aksi yang sebelumnya dibatalkan menggunakan Undo.

#### 4. QUEUE - ENQUEUE

Menambahkan pesanan ke bagian belakang antrean.

#### 5. QUEUE - DEQUEUE NAIF

Mengambil data dari bagian depan antrean dengan menggeser elemen yang tersisa.

Jumlah pergeseran dicatat sebagai bagian dari pengukuran performa.

#### 6. QUEUE - DEQUEUE CIRCULAR

Mengambil data dari bagian depan antrean menggunakan Circular Queue tanpa melakukan pergeseran seluruh elemen.

Circular Queue menggunakan:

- `data`
- `front`
- `rear`
- `count`

Pengujian dilakukan menggunakan kapasitas kecil untuk memastikan pointer dapat berputar dengan benar.

### Statistik M2

Sistem juga mencatat beberapa informasi seperti:

- Panjang antrean
- Kapasitas antrean
- Total pergeseran
- Kedalaman Undo
- Kedalaman Redo

---

# Milestone 3 - Sort & Search

Pada Milestone 3, project berfokus pada penerapan algoritma **sorting** dan **searching** pada data pesanan.

M3 menggunakan empat algoritma utama:

- Insertion Sort
- Merge Sort
- Linear Search
- Binary Search

Setiap algoritma wajib melaporkan **jumlah perbandingan** selain waktu eksekusi.

## Sorting

### Insertion Sort

Insertion Sort digunakan untuk mengurutkan data dengan metode penyisipan.

Karakteristik:

- Bekerja secara in-place
- Stabil
- Kompleksitas waktu `O(n²)`
- Menghitung jumlah perbandingan
- Digunakan untuk pengujian data dalam jumlah terbatas

### Merge Sort

Merge Sort digunakan untuk mengurutkan data dengan metode divide and conquer.

Karakteristik:

- Stabil
- Kompleksitas waktu `O(n log n)`
- Menghitung jumlah perbandingan
- Dapat digunakan untuk mengurutkan seluruh data

Hasil pengujian juga digunakan untuk membandingkan pertumbuhan jumlah perbandingan antara Insertion Sort dan Merge Sort.

## Searching

### Linear Search

Linear Search mencari pesanan dengan memeriksa data satu per satu.

Karakteristik:

- Tidak membutuhkan data yang sudah terurut
- Kompleksitas waktu `O(n)`
- Menghitung jumlah perbandingan
- Pencarian dilakukan berdasarkan `oid`

Hasil pencarian menampilkan informasi pesanan, termasuk:

- `oid`
- `pelanggan`
- `resto`
- `menu`
- `harga`
- `prioritas`
- `masuk`
- `selesai`
- `status`

### Binary Search

Binary Search digunakan untuk mencari pesanan pada data yang sudah terurut.

Karakteristik:

- Membutuhkan data terurut
- Kompleksitas waktu `O(log n)`
- Menghitung jumlah perbandingan
- Pencarian dilakukan berdasarkan `oid`

Sebelum pencarian Binary Search dilakukan, daftar `oid` diurutkan menggunakan Merge Sort. Biaya pembangunan daftar terurut tersebut juga ditampilkan secara terpisah dari biaya pencarian Binary Search.

Hasil pencarian menampilkan informasi pesanan, termasuk:

- `oid`
- `pelanggan`
- `resto`
- `menu`
- `harga`
- `prioritas`
- `masuk`
- `selesai`
- `status`

---

# Teknologi

- Python
- Tkinter
- CSV
- Object-Oriented Programming (OOP)

---

# Struktur Project

```text
Project_Strukdat/
├── app.py
├── backend/
│   ├── m1_pesanan.py
│   ├── m2_antrean.py
│   └── m3_laporan.py
├── frontend/
│   └── ui.py
└── data/
    └── pesanan.csv
