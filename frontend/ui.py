import tkinter as tk
from tkinter import ttk
import time

from backend.m1_pesanan import load_pesanan, Pesanan


class App:
    def __init__(self, root):
        self.root = root

        self.root.title("2EZ4U APP")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

        # =========================
        # LOAD DATA
        # =========================
        self.array, self.linked_list = load_pesanan(
            "data/pesanan.csv"
        )

        # Struktur data aktif
        self.struktur = "Array"

        # Pagination
        self.halaman = 1
        self.data_per_halaman = 100

        # =========================
        # WARNA
        # =========================
        self.bg_sidebar = "#1E293B"
        self.bg_utama = "#F8FAFC"
        self.bg_card = "#FFFFFF"
        self.text_utama = "#0F172A"
        self.text_sidebar = "#E2E8F0"

        self.buat_layout()

    def buat_layout(self):
        # =========================
        # CONTAINER UTAMA
        # =========================
        self.container = tk.Frame(
            self.root,
            bg=self.bg_utama
        )
        self.container.pack(
            fill="both",
            expand=True
        )

        # =========================
        # SIDEBAR
        # =========================
        self.sidebar = tk.Frame(
            self.container,
            width=240,
            bg=self.bg_sidebar
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # =========================
        # LOGO / NAMA APP
        # =========================
        logo = tk.Label(
            self.sidebar,
            text="2EZ4U",
            font=("Arial", 22, "bold"),
            bg=self.bg_sidebar,
            fg="white"
        )
        logo.pack(
            pady=(30, 5)
        )

        sublogo = tk.Label(
            self.sidebar,
            text="Order Management",
            font=("Arial", 9),
            bg=self.bg_sidebar,
            fg=self.text_sidebar
        )
        sublogo.pack(
            pady=(0, 30)
        )

        # =========================
        # LABEL MILESTONE
        # =========================
        label_milestone = tk.Label(
            self.sidebar,
            text="MILESTONE",
            font=("Arial", 9, "bold"),
            bg=self.bg_sidebar,
            fg="#94A3B8"
        )
        label_milestone.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        # =========================
        # MENU M1
        # =========================
        self.tombol_m1 = tk.Button(
            self.sidebar,
            text="  M1  •  Pesanan",
            anchor="w",
            font=("Arial", 11, "bold"),
            bg="#334155",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=10,
            command=self.halaman_m1
        )
        self.tombol_m1.pack(
            fill="x",
            padx=10,
            pady=2
        )

        # M2-M6 sementara
        menu_lain = [
            "  M2  •  Antrean",
            "  M3  •  Laporan",
            "  M4  •  Pencarian",
            "  M5  •  Katalog",
            "  M6  •  Peta"
        ]

        for menu in menu_lain:
            tombol = tk.Button(
                self.sidebar,
                text=menu,
                anchor="w",
                font=("Arial", 11),
                bg=self.bg_sidebar,
                fg="#64748B",
                activebackground=self.bg_sidebar,
                activeforeground="#64748B",
                relief="flat",
                bd=0,
                padx=15,
                pady=10,
                state="disabled"
            )
            tombol.pack(
                fill="x",
                padx=10,
                pady=2
            )

        # =========================
        # PEMISAH
        # =========================
        pemisah = tk.Frame(
            self.sidebar,
            height=1,
            bg="#334155"
        )
        pemisah.pack(
            fill="x",
            padx=20,
            pady=25
        )

                # =========================
        # MENU M1
        # =========================

        self.tombol_pesanan = tk.Button(
            self.sidebar,
            text="  Pesanan",
            anchor="w",
            font=("Arial", 10),
            bg=self.bg_sidebar,
            fg=self.text_sidebar,
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            command=self.halaman_m1
        )
        self.tombol_pesanan.pack(
            fill="x",
            padx=10,
            pady=1
        )

        self.tombol_array = tk.Button(
            self.sidebar,
            text="  Array",
            anchor="w",
            font=("Arial", 10),
            bg=self.bg_sidebar,
            fg=self.text_sidebar,
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            command=self.halaman_array
        )
        self.tombol_array.pack(
            fill="x",
            padx=10,
            pady=1
        )

        self.tombol_linked = tk.Button(
            self.sidebar,
            text="  Linked List",
            anchor="w",
            font=("Arial", 10),
            bg=self.bg_sidebar,
            fg=self.text_sidebar,
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            command=self.halaman_linked_list
        )
        self.tombol_linked.pack(
            fill="x",
            padx=10,
            pady=1
        )

        self.tombol_tambah = tk.Button(
            self.sidebar,
            text="  Tambah Pesanan",
            anchor="w",
            font=("Arial", 10),
            bg=self.bg_sidebar,
            fg=self.text_sidebar,
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            command=self.halaman_tambah
        )
        self.tombol_tambah.pack(
            fill="x",
            padx=10,
            pady=1
        )

        self.tombol_hapus = tk.Button(
            self.sidebar,
            text="  Hapus Pesanan",
            anchor="w",
            font=("Arial", 10),
            bg=self.bg_sidebar,
            fg=self.text_sidebar,
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            command=self.halaman_hapus
        )
        self.tombol_hapus.pack(
            fill="x",
            padx=10,
            pady=1
        )

        # =========================
        # CONTENT AREA
        # =========================
        self.content = tk.Frame(
            self.container,
            bg=self.bg_utama
        )
        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.halaman_m1()

    def halaman_m1(self):
        self._bersihkan_content()

        # =========================
        # HEADER
        # =========================
        header = tk.Frame(
            self.content,
            bg=self.bg_utama
        )
        header.pack(
            fill="x",
            padx=35,
            pady=(30, 20)
        )

        tk.Label(
            header,
            text="M1 — Pesanan",
            font=("Arial", 24, "bold"),
            bg=self.bg_utama,
            fg=self.text_utama
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Implementasi Array dan Linked List",
            font=("Arial", 11),
            bg=self.bg_utama,
            fg="#64748B"
        ).pack(anchor="w", pady=(5, 0))

        # =========================
        # CARD INFORMASI
        # =========================
        frame_card = tk.Frame(
            self.content,
            bg=self.bg_utama
        )
        frame_card.pack(
            fill="x",
            padx=35
        )

        self.buat_card(
            frame_card,
            "TOTAL PESANAN",
            str(self.array.size)
        )

        self.buat_card(
            frame_card,
            "ARRAY",
            str(self.array.size)
        )

        self.buat_card(
            frame_card,
            "LINKED LIST",
            str(self.linked_list.size)
        )

        # =========================
        # AREA INFORMASI
        # =========================
        info = tk.Frame(
            self.content,
            bg=self.bg_card,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        info.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=25
        )

        tk.Label(
            info,
            text="Manajemen Data Pesanan",
            font=("Arial", 16, "bold"),
            bg=self.bg_card,
            fg=self.text_utama
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 10)
        )

        tk.Label(
            info,
            text=(
                "M1 menggunakan dua struktur data untuk mengelola "
                "pesanan, yaitu Array dan Linked List.\n\n"
                "Gunakan menu di sebelah kiri untuk melihat data "
                "atau melakukan operasi pada pesanan."
            ),
            font=("Arial", 11),
            justify="left",
            bg=self.bg_card,
            fg="#475569"
        ).pack(
            anchor="w",
            padx=25
        )

    def halaman_array(self):
        # Hapus isi content
        for widget in self.content.winfo_children():
            widget.destroy()

        # =========================
        # HEADER
        # =========================
        tk.Label(
            self.content,
            text="Array",
            font=("Arial", 24, "bold"),
            bg=self.bg_utama,
            fg=self.text_utama
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        tk.Label(
            self.content,
            text="Data pesanan yang disimpan menggunakan struktur Array",
            font=("Arial", 11),
            bg=self.bg_utama,
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=35
        )

        # =========================
        # INFO
        # =========================
        tk.Label(
            self.content,
            text=f"Jumlah data: {self.array.size}",
            font=("Arial", 12, "bold"),
            bg=self.bg_utama,
            fg=self.text_utama
        ).pack(
            anchor="w",
            padx=35,
            pady=20
        )

        # =========================
        # TEST GET
        # =========================
        frame_get = tk.Frame(
            self.content,
            bg=self.bg_card,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        frame_get.pack(
            fill="x",
            padx=35,
            pady=5
        )

        tk.Label(
            frame_get,
            text="GET PESANAN BERDASARKAN INDEX",
            font=("Arial", 12, "bold"),
            bg=self.bg_card,
            fg=self.text_utama
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        frame_input = tk.Frame(
            frame_get,
            bg=self.bg_card
        )
        frame_input.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        tk.Label(
            frame_input,
            text="Index:",
            bg=self.bg_card
        ).pack(side="left")

        self.input_index_array = tk.Entry(
            frame_input,
            width=15
        )
        self.input_index_array.pack(
            side="left",
            padx=10
        )

        tk.Button(
            frame_input,
            text="GET",
            command=self.get_array
        ).pack(side="left")

        self.label_hasil_array = tk.Label(
            frame_get,
            text="Masukkan index kemudian tekan GET.",
            bg=self.bg_card,
            fg="#475569",
            justify="left"
        )
        self.label_hasil_array.pack(
            anchor="w",
            padx=20,
            pady=(0, 8)
        )

        self.label_waktu_array = tk.Label(
            frame_get,
            text="Waktu proses Array: -",
            font=("Arial", 9, "bold"),
            bg=self.bg_card,
            fg="#2563EB"
        )
        self.label_waktu_array.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

    def get_array(self):
        try:
            index = int(self.input_index_array.get())

            waktu_mulai = time.perf_counter_ns()
            pesanan = self.array.get(index)
            waktu_selesai = time.perf_counter_ns()

            waktu_ms = (waktu_selesai - waktu_mulai) / 1_000_000

            hasil = (
                f"OID        : {pesanan.oid}\n"
                f"Pelanggan  : {pesanan.pelanggan}\n"
                f"Resto      : {pesanan.resto}\n"
                f"Menu       : {pesanan.menu}\n"
                f"Harga      : {pesanan.harga}\n"
                f"Prioritas  : {pesanan.prioritas}\n"
                f"Status     : {pesanan.status}"
            )

            self.label_hasil_array.config(
                text=hasil
            )

            self.label_waktu_array.config(
                text=f"Waktu proses Array: {waktu_ms:.6f} ms"
            )

        except ValueError:
            self.label_hasil_array.config(
                text="Index harus berupa angka."
            )

        except IndexError:
            self.label_hasil_array.config(
                text="Index berada di luar batas data."
            )    

    def halaman_linked_list(self):
        # Hapus isi content
        for widget in self.content.winfo_children():
            widget.destroy()

        # =========================
        # HEADER
        # =========================
        tk.Label(
            self.content,
            text="Linked List",
            font=("Arial", 24, "bold"),
            bg=self.bg_utama,
            fg=self.text_utama
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        tk.Label(
            self.content,
            text="Data pesanan yang disimpan menggunakan struktur Linked List",
            font=("Arial", 11),
            bg=self.bg_utama,
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=35
        )

        # =========================
        # INFO
        # =========================
        tk.Label(
            self.content,
            text=f"Jumlah data: {self.linked_list.size}",
            font=("Arial", 12, "bold"),
            bg=self.bg_utama,
            fg=self.text_utama
        ).pack(
            anchor="w",
            padx=35,
            pady=20
        )

        # =========================
        # TEST GET
        # =========================
        frame_get = tk.Frame(
            self.content,
            bg=self.bg_card,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        frame_get.pack(
            fill="x",
            padx=35,
            pady=5
        )

        tk.Label(
            frame_get,
            text="GET PESANAN BERDASARKAN INDEX",
            font=("Arial", 12, "bold"),
            bg=self.bg_card,
            fg=self.text_utama
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        frame_input = tk.Frame(
            frame_get,
            bg=self.bg_card
        )
        frame_input.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        tk.Label(
            frame_input,
            text="Index:",
            bg=self.bg_card
        ).pack(side="left")

        self.input_index_linked = tk.Entry(
            frame_input,
            width=15
        )
        self.input_index_linked.pack(
            side="left",
            padx=10
        )

        tk.Button(
            frame_input,
            text="GET",
            command=self.get_linked_list
        ).pack(side="left")

        self.label_hasil_linked = tk.Label(
            frame_get,
            text="Masukkan index kemudian tekan GET.",
            bg=self.bg_card,
            fg="#475569",
            justify="left"
        )
        self.label_hasil_linked.pack(
            anchor="w",
            padx=20,
            pady=(0, 8)
        )

        self.label_waktu_linked = tk.Label(
            frame_get,
            text="Waktu proses Linked List: -",
            font=("Arial", 9, "bold"),
            bg=self.bg_card,
            fg="#2563EB"
        )
        self.label_waktu_linked.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

    def get_linked_list(self):
        try:
            index = int(self.input_index_linked.get())

            waktu_mulai = time.perf_counter_ns()
            pesanan = self.linked_list.get(index)
            waktu_selesai = time.perf_counter_ns()

            waktu_ms = (waktu_selesai - waktu_mulai) / 1_000_000

            hasil = (
                f"OID        : {pesanan.oid}\n"
                f"Pelanggan  : {pesanan.pelanggan}\n"
                f"Resto      : {pesanan.resto}\n"
                f"Menu       : {pesanan.menu}\n"
                f"Harga      : {pesanan.harga}\n"
                f"Prioritas  : {pesanan.prioritas}\n"
                f"Status     : {pesanan.status}"
            )

            self.label_hasil_linked.config(
                text=hasil
            )

            self.label_waktu_linked.config(
                text=f"Waktu proses Linked List: {waktu_ms:.6f} ms"
            )

        except ValueError:
            self.label_hasil_linked.config(
                text="Index harus berupa angka."
            )

        except IndexError:
            self.label_hasil_linked.config(
                text="Index berada di luar batas data."
            )


    # ============================================================
    # HALAMAN TAMBAH PESANAN
    # ============================================================

    def halaman_tambah(self):
        self._bersihkan_content()

        self._buat_header(
            "Tambah Pesanan",
            "Tambahkan pesanan baru ke Array dan Linked List."
        )

        card = tk.Frame(
            self.content,
            bg=self.bg_card,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        card.pack(
            fill="x",
            padx=35,
            pady=(10, 20)
        )

        tk.Label(
            card,
            text="Data Pesanan Baru",
            font=("Arial", 14, "bold"),
            bg=self.bg_card,
            fg=self.text_utama
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(20, 15)
        )

        self.input_jenis = ttk.Combobox(
            card,
            values=["REGULER", "PRIORITAS", "VIP"],
            state="readonly",
            width=30
        )
        self.input_jenis.set("REGULER")

        self.input_oid = tk.Entry(card, width=33)
        self.input_pelanggan = tk.Entry(card, width=33)
        self.input_resto = tk.Entry(card, width=33)
        self.input_menu = tk.Entry(card, width=33)
        self.input_harga = tk.Entry(card, width=33)

        fields = [
            ("Jenis Pesanan", self.input_jenis),
            ("OID", self.input_oid),
            ("Pelanggan", self.input_pelanggan),
            ("Restoran", self.input_resto),
            ("Menu", self.input_menu),
            ("Harga", self.input_harga),
        ]

        for row, (label, widget) in enumerate(fields, start=1):
            tk.Label(
                card,
                text=label,
                font=("Arial", 10, "bold"),
                bg=self.bg_card,
                fg="#475569"
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=(25, 15),
                pady=8
            )

            widget.grid(
                row=row,
                column=1,
                sticky="w",
                padx=(0, 25),
                pady=8,
                ipady=4
            )

        self.label_status_tambah = tk.Label(
            card,
            text="",
            font=("Arial", 10),
            bg=self.bg_card,
            fg="#475569",
            justify="left"
        )
        self.label_status_tambah.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(12, 5)
        )

        tk.Button(
            card,
            text="TAMBAH PESANAN",
            font=("Arial", 10, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.tambah_pesanan
        ).grid(
            row=8,
            column=0,
            columnspan=2,
            pady=(10, 25)
        )

    def tambah_pesanan(self):
        jenis = self.input_jenis.get().strip()
        oid = self.input_oid.get().strip()
        pelanggan = self.input_pelanggan.get().strip()
        resto = self.input_resto.get().strip()
        menu = self.input_menu.get().strip()
        harga_text = self.input_harga.get().strip()

        if not all([jenis, oid, pelanggan, resto, menu, harga_text]):
            self.label_status_tambah.config(
                text="Semua field wajib diisi.",
                fg="#DC2626"
            )
            return

        try:
            harga = float(harga_text)
        except ValueError:
            self.label_status_tambah.config(
                text="Harga harus berupa angka.",
                fg="#DC2626"
            )
            return

        # Buat satu object Pesanan, lalu masukkan object yang sama
        # ke kedua struktur agar data tetap sinkron.
        prioritas = jenis
        pesanan_baru = Pesanan(
            oid,
            pelanggan,
            resto,
            menu,
            harga,
            prioritas,
            0,
            None,
            "Menunggu"
        )

        if jenis == "REGULER":
            self.array.tambah_reguler(pesanan_baru)
            self.linked_list.tambah_reguler(pesanan_baru)
        elif jenis == "PRIORITAS":
            self.array.tambah_prioritas(pesanan_baru)
            self.linked_list.tambah_prioritas(pesanan_baru)
        else:
            self.array.tambah_vip(pesanan_baru)
            self.linked_list.tambah_vip(pesanan_baru)

        self.label_status_tambah.config(
            text=(
                f"Pesanan {oid} berhasil ditambahkan sebagai {jenis}.\n"
                f"Total data sekarang: {self.array.size}"
            ),
            fg="#16A34A"
        )

        self._kosongkan_form_tambah()

    def _kosongkan_form_tambah(self):
        for widget in [
            self.input_oid,
            self.input_pelanggan,
            self.input_resto,
            self.input_menu,
            self.input_harga
        ]:
            widget.delete(0, tk.END)

        self.input_jenis.set("REGULER")

    # ============================================================
    # HALAMAN HAPUS PESANAN
    # ============================================================

    def halaman_hapus(self):
        self._bersihkan_content()

        self._buat_header(
            "Hapus Pesanan",
            "Hapus pesanan berdasarkan index dari Array dan Linked List."
        )

        card = tk.Frame(
            self.content,
            bg=self.bg_card,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        card.pack(
            fill="x",
            padx=35,
            pady=(10, 20)
        )

        tk.Label(
            card,
            text="Hapus Data",
            font=("Arial", 14, "bold"),
            bg=self.bg_card,
            fg=self.text_utama
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 15)
        )

        frame_input = tk.Frame(card, bg=self.bg_card)
        frame_input.pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        tk.Label(
            frame_input,
            text="Index:",
            font=("Arial", 10, "bold"),
            bg=self.bg_card,
            fg="#475569"
        ).pack(side="left")

        self.input_index_hapus = tk.Entry(
            frame_input,
            width=15
        )
        self.input_index_hapus.pack(
            side="left",
            padx=12,
            ipady=4
        )

        tk.Button(
            frame_input,
            text="HAPUS PESANAN",
            font=("Arial", 10, "bold"),
            bg="#DC2626",
            fg="white",
            activebackground="#B91C1C",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.hapus_pesanan
        ).pack(side="left")

        self.label_status_hapus = tk.Label(
            card,
            text="Masukkan index yang ingin dihapus.",
            font=("Arial", 10),
            bg=self.bg_card,
            fg="#475569",
            justify="left"
        )
        self.label_status_hapus.pack(
            anchor="w",
            padx=25,
            pady=(0, 25)
        )

    def hapus_pesanan(self):
        try:
            index = int(self.input_index_hapus.get())
        except ValueError:
            self.label_status_hapus.config(
                text="Index harus berupa angka.",
                fg="#DC2626"
            )
            return

        try:
            pesanan = self.array.get(index)
        except IndexError:
            self.label_status_hapus.config(
                text="Index berada di luar batas data.",
                fg="#DC2626"
            )
            return

        oid = pesanan.oid

        # Hapus index yang sama dari kedua struktur.
        self.array.delete(index)
        self.linked_list.delete(index)

        self.label_status_hapus.config(
            text=(
                f"Pesanan {oid} berhasil dihapus.\n"
                f"Total data sekarang: {self.array.size}"
            ),
            fg="#16A34A"
        )

        self.input_index_hapus.delete(0, tk.END)

    # ============================================================
    # HELPER UI
    # ============================================================

    def _bersihkan_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def _buat_header(self, judul, subjudul):
        header = tk.Frame(
            self.content,
            bg=self.bg_utama
        )
        header.pack(
            fill="x",
            padx=35,
            pady=(30, 15)
        )

        tk.Label(
            header,
            text=judul,
            font=("Arial", 24, "bold"),
            bg=self.bg_utama,
            fg=self.text_utama
        ).pack(anchor="w")

        tk.Label(
            header,
            text=subjudul,
            font=("Arial", 11),
            bg=self.bg_utama,
            fg="#64748B"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

    def buat_card(self, parent, judul, nilai):
        card = tk.Frame(
            parent,
            bg=self.bg_card,
            width=200,
            height=90,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 15)
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=judul,
            font=("Arial", 9, "bold"),
            bg=self.bg_card,
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 3)
        )

        tk.Label(
            card,
            text=nilai,
            font=("Arial", 20, "bold"),
            bg=self.bg_card,
            fg=self.text_utama
        ).pack(
            anchor="w",
            padx=15
        )


if __name__ == "__main__":
    root = tk.Tk()

    app = App(root)

    root.mainloop()