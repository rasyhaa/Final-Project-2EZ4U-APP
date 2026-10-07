"""
Modul M2 - Struktur Data Antrean dan Stack
2EZ4U APP - EC234303

Implementasi:
- Stack berbasis array dinamis buatan sendiri (tanpa list.pop sebagai struktur stack).
- AntreanNaif: dequeue menggeser elemen dan mencatat jumlah pergeseran.
- AntreanMelingkar: circular queue dengan kapasitas yang dapat bertambah otomatis.
- Konversi infix ke postfix dan evaluasi postfix dengan validasi.
- Riwayat undo/redo berbasis aksi (bukan snapshot seluruh antrean).

Tidak menggunakan dict, set, sorted(), list.sort(), heapq, bisect,
collections, atau dictionary/set comprehension.
"""


class Stack:
    """Stack berbasis array dinamis dengan operasi push, pop, peek, dan kosong."""

    def __init__(self, kapasitas_awal=8):
        if kapasitas_awal < 1:
            kapasitas_awal = 1
        self.kapasitas = kapasitas_awal
        self.data = [None] * self.kapasitas
        self.top = -1

    def _perbesar(self):
        data_baru = [None] * (self.kapasitas * 2)
        for i in range(self.top + 1):
            data_baru[i] = self.data[i]
        self.data = data_baru
        self.kapasitas *= 2

    def push(self, nilai):
        if self.top + 1 >= self.kapasitas:
            self._perbesar()
        self.top += 1
        self.data[self.top] = nilai

    def pop(self):
        if self.kosong():
            return None
        nilai = self.data[self.top]
        self.data[self.top] = None
        self.top -= 1
        return nilai

    def peek(self):
        if self.kosong():
            return None
        return self.data[self.top]

    def kosong(self):
        return self.top == -1

    def ukuran(self):
        return self.top + 1

    def bersihkan(self):
        self.data = [None] * self.kapasitas
        self.top = -1


class AntreanNaif:
    """Antrean array biasa; dequeue menggeser seluruh elemen yang tersisa."""

    def __init__(self):
        self.data = []
        self.total_pergeseran = 0

    def enqueue(self, nilai):
        self.data.append(nilai)
        return True

    def dequeue(self):
        if self.kosong():
            return None
        nilai = self.data[0]
        jumlah_geser = len(self.data) - 1
        for i in range(jumlah_geser):
            self.data[i] = self.data[i + 1]
        if jumlah_geser > 0:
            del self.data[-1]
        else:
            self.data.clear()
        self.total_pergeseran += jumlah_geser
        return nilai

    def enqueue_front(self, nilai):
        """Digunakan untuk pemulihan aksi dequeue saat undo."""
        self.data.insert(0, nilai)

    def dequeue_back(self):
        if self.kosong():
            return None
        return self.data.pop()

    def kosong(self):
        return len(self.data) == 0

    def ukuran(self):
        return len(self.data)

    def tampilkan(self):
        hasil = []
        for nilai in self.data:
            hasil.append(nilai)
        return hasil

    def dequeue_banyak(self, jumlah):
        hasil = []
        batas = jumlah
        if batas < 0:
            batas = 0
        if batas > self.ukuran():
            batas = self.ukuran()
        for _ in range(batas):
            hasil.append(self.dequeue())
        return hasil


class AntreanMelingkar:
    """Circular queue. Kapasitas bertambah dua kali lipat saat penuh."""

    def __init__(self, kapasitas=8):
        if kapasitas < 1:
            raise ValueError("Kapasitas antrean harus minimal 1.")
        self.kapasitas = kapasitas
        self.data = [None] * kapasitas
        self.front = 0
        self.rear = -1
        self.count = 0

    def _perbesar(self):
        kapasitas_baru = self.kapasitas * 2
        data_baru = [None] * kapasitas_baru
        for i in range(self.count):
            indeks_lama = (self.front + i) % self.kapasitas
            data_baru[i] = self.data[indeks_lama]
        self.data = data_baru
        self.kapasitas = kapasitas_baru
        self.front = 0
        if self.count == 0:
            self.rear = -1
        else:
            self.rear = self.count - 1

    def enqueue(self, nilai):
        if self.penuh():
            self._perbesar()
        self.rear = (self.rear + 1) % self.kapasitas
        self.data[self.rear] = nilai
        self.count += 1
        return True

    def dequeue(self):
        if self.kosong():
            return None
        nilai = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.kapasitas
        self.count -= 1
        if self.count == 0:
            self.front = 0
            self.rear = -1
        return nilai

    def dequeue_back(self):
        if self.kosong():
            return None
        nilai = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        if self.count == 0:
            self.front = 0
            self.rear = -1
        else:
            self.rear = (self.rear - 1) % self.kapasitas
        return nilai

    def enqueue_front(self, nilai):
        """Memasukkan elemen di depan; dipakai untuk undo dequeue."""
        if self.penuh():
            self._perbesar()
        self.front = (self.front - 1) % self.kapasitas
        self.data[self.front] = nilai
        self.count += 1
        if self.count == 1:
            self.rear = self.front
        return True

    def kosong(self):
        return self.count == 0

    def penuh(self):
        return self.count == self.kapasitas

    def ukuran(self):
        return self.count

    def tampilkan(self):
        hasil = []
        for i in range(self.count):
            indeks = (self.front + i) % self.kapasitas
            hasil.append(self.data[indeks])
        return hasil

    def dequeue_banyak(self, jumlah):
        hasil = []
        batas = jumlah
        if batas < 0:
            batas = 0
        if batas > self.count:
            batas = self.count
        for _ in range(batas):
            hasil.append(self.dequeue())
        return hasil


def _prioritas(operator):
    if operator == "+" or operator == "-":
        return 1
    if operator == "*" or operator == "/":
        return 2
    if operator == "u-":
        return 3
    return 0


def _tokenisasi(ekspresi):
    """Memecah ekspresi termasuk tanpa spasi, angka multi-digit dan desimal."""
    token = []
    i = 0
    while i < len(ekspresi):
        karakter = ekspresi[i]
        if karakter.isspace():
            i += 1
        elif karakter.isdigit() or karakter == ".":
            angka = ""
            titik = 0
            while i < len(ekspresi) and (
                ekspresi[i].isdigit() or ekspresi[i] == "."
            ):
                if ekspresi[i] == ".":
                    titik += 1
                angka += ekspresi[i]
                i += 1
            if titik > 1 or angka == ".":
                raise ValueError("Format angka tidak valid: " + angka)
            token.append(angka)
        elif karakter in "+-*/()":
            token.append(karakter)
            i += 1
        else:
            raise ValueError("Karakter tidak dikenal: " + karakter)
    return token


def infix_ke_postfix(ekspresi):
    """Mengubah ekspresi infix menjadi postfix dengan algoritma Shunting-yard."""
    token = _tokenisasi(ekspresi)
    if len(token) == 0:
        raise ValueError("Ekspresi tidak boleh kosong.")

    output = []
    operator = Stack()
    sebelumnya_operand = False

    for nilai in token:
        if nilai[0].isdigit() or nilai[0] == ".":
            if sebelumnya_operand:
                raise ValueError("Operator hilang di antara angka.")
            output.append(nilai)
            sebelumnya_operand = True
        elif nilai == "(":
            if sebelumnya_operand:
                raise ValueError("Operator hilang sebelum tanda kurung.")
            operator.push(nilai)
            sebelumnya_operand = False
        elif nilai == ")":
            if not sebelumnya_operand:
                raise ValueError("Isi atau operator sebelum ')' tidak valid.")
            ditemukan_buka = False
            while not operator.kosong():
                atas = operator.pop()
                if atas == "(":
                    ditemukan_buka = True
                    break
                output.append(atas)
            if not ditemukan_buka:
                raise ValueError("Tanda kurung buka tidak ditemukan.")
            sebelumnya_operand = True
        else:
            # Minus unary, misalnya -5 atau 8*(-2).
            op = nilai
            if not sebelumnya_operand:
                if nilai == "-":
                    op = "u-"
                else:
                    raise ValueError("Operator tidak memiliki operand kiri.")
            while (
                not operator.kosong()
                and operator.peek() != "("
                and (
                    _prioritas(operator.peek()) > _prioritas(op)
                    or (
                        _prioritas(operator.peek()) == _prioritas(op)
                        and op != "u-"
                    )
                )
            ):
                output.append(operator.pop())
            operator.push(op)
            sebelumnya_operand = False

    if not sebelumnya_operand:
        raise ValueError("Ekspresi berakhir dengan operator.")

    while not operator.kosong():
        atas = operator.pop()
        if atas == "(":
            raise ValueError("Tanda kurung tutup tidak ditemukan.")
        output.append(atas)

    return " ".join(output)


def evaluasi_postfix(ekspresi):
    """Mengevaluasi ekspresi postfix dan memvalidasi jumlah operand."""
    stack = Stack()
    token = ekspresi.split()
    if len(token) == 0:
        raise ValueError("Ekspresi postfix tidak boleh kosong.")

    for nilai in token:
        if nilai == "u-":
            a = stack.pop()
            if a is None:
                raise ValueError("Operand kurang pada operator unary.")
            stack.push(-a)
        elif nilai in ("+", "-", "*", "/"):
            b = stack.pop()
            a = stack.pop()
            if a is None or b is None:
                raise ValueError("Operand kurang pada ekspresi postfix.")
            if nilai == "+":
                hasil = a + b
            elif nilai == "-":
                hasil = a - b
            elif nilai == "*":
                hasil = a * b
            else:
                if b == 0:
                    raise ZeroDivisionError("Tidak dapat membagi dengan nol.")
                hasil = a / b
            stack.push(hasil)
        else:
            try:
                stack.push(float(nilai))
            except ValueError:
                raise ValueError("Token postfix tidak valid: " + nilai)

    if stack.ukuran() != 1:
        raise ValueError("Ekspresi postfix tidak valid: operand tersisa.")
    return stack.pop()


def hitung_postfix_dengan_langkah(ekspresi):
    """Menghasilkan nilai akhir dan daftar langkah operasi untuk UI."""
    stack = Stack()
    langkah = []
    token = ekspresi.split()

    for nilai in token:
        if nilai == "u-":
            a = stack.pop()
            if a is None:
                raise ValueError("Operand kurang pada operator unary.")
            hasil = -a
            stack.push(hasil)
            langkah.append(("NEGASI", a, None, hasil))
        elif nilai in ("+", "-", "*", "/"):
            b = stack.pop()
            a = stack.pop()
            if a is None or b is None:
                raise ValueError("Operand kurang pada ekspresi postfix.")
            if nilai == "+":
                hasil = a + b
            elif nilai == "-":
                hasil = a - b
            elif nilai == "*":
                hasil = a * b
            else:
                if b == 0:
                    raise ZeroDivisionError("Tidak dapat membagi dengan nol.")
                hasil = a / b
            stack.push(hasil)
            langkah.append((nilai, a, b, hasil))
        else:
            try:
                stack.push(float(nilai))
            except ValueError:
                raise ValueError("Token postfix tidak valid: " + nilai)

    if stack.ukuran() != 1:
        raise ValueError("Ekspresi postfix tidak valid: operand tersisa.")
    return stack.pop(), langkah


class RiwayatUndoRedo:
    """
    Undo/redo berbasis catatan aksi.
    Dapat mengelola antrean melingkar dan antrean naif jika keduanya diberikan.
    """

    def __init__(self, antrean, antrean_naif=None):
        self.antrean = antrean
        self.antrean_naif = antrean_naif
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def _catat_aksi_baru(self, aksi):
        self.undo_stack.push(aksi)
        self.redo_stack.bersihkan()

    def enqueue(self, nilai):
        # Simpan aksi dan lakukan ke antrean yang dikelola.
        self.antrean.enqueue(nilai)
        if self.antrean_naif is not None:
            self.antrean_naif.enqueue(nilai)
        self._catat_aksi_baru(("ENQUEUE", nilai))
        return True

    def dequeue(self):
        if self.antrean.kosong():
            return None
        nilai = self.antrean.dequeue()
        if self.antrean_naif is not None and not self.antrean_naif.kosong():
            self.antrean_naif.dequeue()
        self._catat_aksi_baru(("DEQUEUE", [nilai]))
        return nilai

    def dequeue_naif(self):
        if self.antrean_naif is None or self.antrean_naif.kosong():
            return None
        nilai = self.antrean_naif.dequeue()
        # Catatan bertipe khusus agar undo memulihkan antrean naif.
        self._catat_aksi_baru(("DEQUEUE_NAIF", [nilai]))
        return nilai

    def dequeue_circular(self):
        """Dequeue hanya pada circular queue, untuk benchmark independen."""
        if self.antrean.kosong():
            return None
        nilai = self.antrean.dequeue()
        self._catat_aksi_baru(("DEQUEUE_CIRCULAR", [nilai]))
        return nilai

    def _pulihkan_dequeue(self, antrean, nilai_list):
        # Pulihkan urutan ke bagian depan dengan memasukkan dari belakang.
        for i in range(len(nilai_list) - 1, -1, -1):
            antrean.enqueue_front(nilai_list[i])

    def _terapkan_aksi(self, aksi, untuk_undo):
        jenis = aksi[0]
        nilai = aksi[1]

        if jenis == "ENQUEUE":
            if untuk_undo:
                if not self.antrean.kosong():
                    self.antrean.dequeue_back()
                if self.antrean_naif is not None and not self.antrean_naif.kosong():
                    self.antrean_naif.dequeue_back()
            else:
                self.antrean.enqueue(nilai)
                if self.antrean_naif is not None:
                    self.antrean_naif.enqueue(nilai)

        elif jenis == "DEQUEUE":
            if untuk_undo:
                self._pulihkan_dequeue(self.antrean, nilai)
                if self.antrean_naif is not None:
                    self._pulihkan_dequeue(self.antrean_naif, nilai)
            else:
                for _ in range(len(nilai)):
                    self.antrean.dequeue()
                    if self.antrean_naif is not None and not self.antrean_naif.kosong():
                        self.antrean_naif.dequeue()

        elif jenis == "DEQUEUE_NAIF" and self.antrean_naif is not None:
            if untuk_undo:
                self._pulihkan_dequeue(self.antrean_naif, nilai)
            else:
                for _ in range(len(nilai)):
                    self.antrean_naif.dequeue()

        elif jenis == "DEQUEUE_CIRCULAR":
            if untuk_undo:
                self._pulihkan_dequeue(self.antrean, nilai)
            else:
                for _ in range(len(nilai)):
                    self.antrean.dequeue()

    def undo(self):
        if self.undo_stack.kosong():
            return False
        aksi = self.undo_stack.pop()
        self._terapkan_aksi(aksi, True)
        self.redo_stack.push(aksi)
        return True

    def redo(self):
        if self.redo_stack.kosong():
            return False
        aksi = self.redo_stack.pop()
        self._terapkan_aksi(aksi, False)
        self.undo_stack.push(aksi)
        return True

    def ukuran_undo(self):
        return self.undo_stack.ukuran()

    def ukuran_redo(self):
        return self.redo_stack.ukuran()


def muat_data_antrean(daftar_pesanan, antrean_naif, antrean_melingkar):
    """
    Memuat data pesanan yang sama ke dua antrean untuk perbandingan.
    Setiap elemen boleh berupa objek Pesanan atau ID/string biasa.
    """
    jumlah = 0
    for pesanan in daftar_pesanan:
        if hasattr(pesanan, "id_pesanan"):
            nilai = pesanan.id_pesanan
        elif hasattr(pesanan, "id"):
            nilai = pesanan.id
        else:
            nilai = pesanan
        antrean_naif.enqueue(nilai)
        antrean_melingkar.enqueue(nilai)
        jumlah += 1
    return jumlah


def statistik_antrean(antrean_naif, antrean_melingkar,
                      riwayat=None):
    """Mengembalikan statistik ringkas untuk ditampilkan oleh frontend."""
    kedalaman_undo = 0
    kedalaman_redo = 0
    if riwayat is not None:
        kedalaman_undo = riwayat.ukuran_undo()
        kedalaman_redo = riwayat.ukuran_redo()

    return (
        ("Panjang antrean naif", antrean_naif.ukuran()),
        ("Panjang antrean melingkar", antrean_melingkar.ukuran()),
        ("Kapasitas antrean melingkar", antrean_melingkar.kapasitas),
        ("Total pergeseran antrean naif", antrean_naif.total_pergeseran),
        ("Kedalaman undo", kedalaman_undo),
        ("Kedalaman redo", kedalaman_redo),
    )
