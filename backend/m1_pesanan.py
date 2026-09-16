import csv


class Pesanan:
    def __init__(
        self,
        oid,
        pelanggan,
        resto,
        menu,
        harga,
        prioritas,
        t_masuk_detik,
        t_selesai_detik,
        status
    ):
        self.oid = oid
        self.pelanggan = pelanggan
        self.resto = resto
        self.menu = menu
        self.harga = harga
        self.prioritas = prioritas
        self.t_masuk_detik = t_masuk_detik
        self.t_selesai_detik = t_selesai_detik
        self.status = status


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Array:
    def __init__(self, kapasitas_awal=4):
        self.data = [None] * kapasitas_awal
        self.size = 0
        self.capacity = kapasitas_awal

    def _resize(self):
        new_capacity = self.capacity * 2
        new_data = [None] * new_capacity

        for i in range(self.size):
            new_data[i] = self.data[i]

        self.data = new_data
        self.capacity = new_capacity

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index di luar batas")

        return self.data[index]

    def append(self, value):
        if self.size == self.capacity:
            self._resize()

        self.data[self.size] = value
        self.size += 1

    def insert(self, index, value):
        if index < 0 or index > self.size:
            raise IndexError("Index di luar batas")

        if self.size == self.capacity:
            self._resize()

        # Geser data ke kanan
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]

        self.data[index] = value
        self.size += 1

    def delete(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index di luar batas")

        removed = self.data[index]

        # Geser data ke kiri
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]

        self.data[self.size - 1] = None
        self.size -= 1

        return removed

    def tambah_reguler(self, pesanan):
        # REGULER masuk paling belakang
        self.append(pesanan)

    def tambah_prioritas(self, pesanan):
        # PRIORITAS masuk ke tengah barisan
        index = self.size // 2
        self.insert(index, pesanan)

    def tambah_vip(self, pesanan):
        # VIP masuk paling depan
        self.insert(0, pesanan)


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index di luar batas")

        current = self.head

        for _ in range(index):
            current = current.next

        return current.data

    def append(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def insert(self, index, value):
        if index < 0 or index > self.size:
            raise IndexError("Index di luar batas")

        new_node = Node(value)

        # Insert di paling depan
        if index == 0:
            new_node.next = self.head
            self.head = new_node

            if self.size == 0:
                self.tail = new_node

        # Insert di posisi lain
        else:
            current = self.head

            for _ in range(index - 1):
                current = current.next

            new_node.next = current.next
            current.next = new_node

            # Jika masuk di paling belakang
            if index == self.size:
                self.tail = new_node

        self.size += 1

    def delete(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index di luar batas")

        # Hapus node pertama
        if index == 0:
            removed = self.head
            self.head = self.head.next

            if self.size == 1:
                self.tail = None

        # Hapus node lainnya
        else:
            current = self.head

            for _ in range(index - 1):
                current = current.next

            removed = current.next
            current.next = removed.next

            # Jika yang dihapus adalah node terakhir
            if index == self.size - 1:
                self.tail = current

        self.size -= 1

        return removed.data

    def tambah_reguler(self, pesanan):
        # REGULER masuk paling belakang
        self.append(pesanan)

    def tambah_prioritas(self, pesanan):
        # PRIORITAS masuk ke tengah barisan
        index = self.size // 2
        self.insert(index, pesanan)

    def tambah_vip(self, pesanan):
        # VIP masuk paling depan
        self.insert(0, pesanan)


def load_pesanan(nama_file):
    array = Array()
    linked_list = LinkedList()

    with open(nama_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        # Lewati header
        next(reader)

        for row in reader:
            if row[7] == "":
                t_selesai = None
            else:
                t_selesai = float(row[7])

            pesanan = Pesanan(
                row[0],
                row[1],
                row[2],
                row[3],
                int(row[4]),
                int(row[5]),
                int(row[6]),
                t_selesai,
                row[8]
            )

            # Data yang sama dimasukkan ke Array
            array.append(pesanan)

            # Data yang sama dimasukkan ke Linked List
            linked_list.append(pesanan)

    return array, linked_list