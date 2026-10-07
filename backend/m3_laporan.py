"""M3 - Laporan Terurut: sorting dan searching manual sesuai brief 2EZ4U.

Tidak menggunakan sorted(), list.sort(), bisect, dictionary, set, atau heapq.
"""
import time


def _nilai_kunci(pesanan, kunci):
    if kunci == "harga":
        return getattr(pesanan, "harga", 0)
    return str(getattr(pesanan, "oid", ""))


def insertion_sort(data, kunci="harga"):
    """Stable insertion sort. Mengembalikan (data_terurut, perbandingan, durasi_ms)."""
    hasil = list(data)
    perbandingan = 0
    mulai = time.perf_counter()
    for i in range(1, len(hasil)):
        nilai = hasil[i]
        j = i - 1
        while j >= 0:
            perbandingan += 1
            if _nilai_kunci(hasil[j], kunci) > _nilai_kunci(nilai, kunci):
                hasil[j + 1] = hasil[j]
                j -= 1
            else:
                break
        hasil[j + 1] = nilai
    durasi = (time.perf_counter() - mulai) * 1000
    return hasil, perbandingan, durasi


def merge_sort(data, kunci="harga"):
    """Stable merge sort manual. Mengembalikan (data_terurut, perbandingan, durasi_ms)."""
    sumber = list(data)
    perbandingan = [0]

    def urutkan(bagian):
        if len(bagian) <= 1:
            return bagian
        tengah = len(bagian) // 2
        kiri = urutkan(bagian[:tengah])
        kanan = urutkan(bagian[tengah:])
        gabung = []
        i = 0
        j = 0
        while i < len(kiri) and j < len(kanan):
            perbandingan[0] += 1
            # <= menjaga kestabilan: item kiri tetap di depan jika kunci sama.
            if _nilai_kunci(kiri[i], kunci) <= _nilai_kunci(kanan[j], kunci):
                gabung.append(kiri[i])
                i += 1
            else:
                gabung.append(kanan[j])
                j += 1
        while i < len(kiri):
            gabung.append(kiri[i])
            i += 1
        while j < len(kanan):
            gabung.append(kanan[j])
            j += 1
        return gabung

    mulai = time.perf_counter()
    hasil = urutkan(sumber)
    durasi = (time.perf_counter() - mulai) * 1000
    return hasil, perbandingan[0], durasi


def linear_search(data, oid):
    """Mencari OID secara linear; hasil (index, jumlah_perbandingan, durasi_ms)."""
    perbandingan = 0
    mulai = time.perf_counter()
    for i in range(len(data)):
        perbandingan += 1
        if str(getattr(data[i], "oid", "")) == str(oid):
            return i, perbandingan, (time.perf_counter() - mulai) * 1000
    return -1, perbandingan, (time.perf_counter() - mulai) * 1000


def binary_search(data_terurut_oid, oid):
    """Binary search pada data yang sudah terurut berdasarkan OID."""
    kiri = 0
    kanan = len(data_terurut_oid) - 1
    perbandingan = 0
    target = str(oid)
    mulai = time.perf_counter()
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        nilai = str(getattr(data_terurut_oid[tengah], "oid", ""))
        perbandingan += 1
        if nilai == target:
            return tengah, perbandingan, (time.perf_counter() - mulai) * 1000
        if nilai < target:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return -1, perbandingan, (time.perf_counter() - mulai) * 1000
