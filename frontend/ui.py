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
        self.bg_sidebar = "#E9E1F5"
        self.bg_utama = "#FFF9F4"
        self.bg_card = "#FFFFFF"
        self.text_utama = "#4A4458"
        self.text_sidebar = "#5E5870"

        self.buat_layout()

    def buat_layout(self):
        # ============================================================
        # CONTAINER UTAMA
        # ============================================================
        self.container = tk.Frame(
            self.root,
            bg=self.bg_utama
        )
        self.container.pack(
            fill="both",
            expand=True
        )

        # ============================================================
        # SIDEBAR KIRI - M1 SAJA
        # ============================================================
        self.sidebar = tk.Frame(
            self.container,
            width=300,
            bg=self.bg_sidebar
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )
        self.sidebar.pack_propagate(False)

        # Header aplikasi
        header_sidebar = tk.Frame(
            self.sidebar,
            bg="#D8CBEA",
            height=70
        )
        header_sidebar.pack(fill="x")
        header_sidebar.pack_propagate(False)

        tk.Label(
            header_sidebar,
            text="2EZ4U Food Delivery",
            font=("Arial", 14, "bold"),
            bg="#D8CBEA",
            fg="#4A4458"
        ).pack(
            anchor="w",
            padx=15,
            pady=(17, 0)
        )

        tk.Label(
            header_sidebar,
            text="M1 • DATA PESANAN",
            font=("Arial", 8),
            bg="#D8CBEA",
            fg="#7A6E86"
        ).pack(
            anchor="w",
            padx=15,
            pady=(1, 0)
        )

        # Area menu dibuat scrollable
        menu_container = tk.Frame(
            self.sidebar,
            bg=self.bg_sidebar
        )
        menu_container.pack(
            fill="both",
            expand=True
        )

        canvas = tk.Canvas(
            menu_container,
            bg=self.bg_sidebar,
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            menu_container,
            orient="vertical",
            command=canvas.yview
        )
        menu_frame = tk.Frame(
            canvas,
            bg=self.bg_sidebar
        )

        menu_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=menu_frame,
            anchor="nw",
            width=280
        )
        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ============================================================
        # DATA
        # ============================================================
        tk.Label(
            menu_frame,
            text="DATA",
            font=("Arial", 9, "bold"),
            bg=self.bg_sidebar,
            fg="#8A8196"
        ).pack(
            anchor="w",
            padx=12,
            pady=(12, 5)
        )

        self._buat_menu_button(
            menu_frame,
            "Load",
            self.muat_data
        )

        # ============================================================
        # M1 - DATA PESANAN
        # ============================================================
        tk.Label(
            menu_frame,
            text="M1 - DATA PESANAN",
            font=("Arial", 9, "bold"),
            bg=self.bg_sidebar,
            fg="#8A8196"
        ).pack(
            anchor="w",
            padx=12,
            pady=(12, 5)
        )

        self._buat_menu_button(
            menu_frame,
            "ARRAY - LIHAT PESANAN",
            self.halaman_array
        )
        self._buat_menu_button(
            menu_frame,
            "ARRAY - TAMBAH PESANAN REGULER",
            lambda: self.halaman_tambah("REGULER")
        )
        self._buat_menu_button(
            menu_frame,
            "ARRAY - TAMBAH PESANAN PRIORITAS",
            lambda: self.halaman_tambah("PRIORITAS")
        )
        self._buat_menu_button(
            menu_frame,
            "ARRAY - TAMBAH PESANAN VIP",
            lambda: self.halaman_tambah("VIP")
        )
        self._buat_menu_button(
            menu_frame,
            "ARRAY - HAPUS PESANAN",
            self.halaman_hapus
        )

        self._buat_menu_button(
            menu_frame,
            "LINKED LIST - LIHAT PESANAN",
            self.halaman_linked_list
        )
        self._buat_menu_button(
            menu_frame,
            "LINKED LIST - TAMBAH PESANAN REGULER",
            lambda: self.halaman_tambah("REGULER")
        )
        self._buat_menu_button(
            menu_frame,
            "LINKED LIST - TAMBAH PESANAN PRIORITAS",
            lambda: self.halaman_tambah("PRIORITAS")
        )
        self._buat_menu_button(
            menu_frame,
            "LINKED LIST - TAMBAH PESANAN VIP",
            lambda: self.halaman_tambah("VIP")
        )
        self._buat_menu_button(
            menu_frame,
            "LINKED LIST - HAPUS PESANAN",
            self.halaman_hapus
        )

        # M2-M6 belum ditampilkan karena brief/detail-nya belum diberikan.

        # ============================================================
        # CONTENT AREA
        # ============================================================
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

    def _buat_menu_button(self, parent, text, command):
        button = tk.Button(
            parent,
            text=text,
            anchor="w",
            font=("Arial", 9),
            bg="#FDFBFF",
            fg="#5E5870",
            activebackground="#EADFF3",
            activeforeground="#4A4458",
            relief="solid",
            bd=1,
            padx=8,
            pady=6,
            cursor="hand2",
            command=command
        )
        button.pack(
            fill="x",
            padx=10,
            pady=1
        )
        return button

    def muat_data(self):
        self.array, self.linked_list = load_pesanan(
            "data/pesanan.csv"
        )
        self.halaman = 1
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
            fg="#8A8196"
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
            highlightbackground="#E7DEEE",
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
            fg="#6B6478"
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
            fg="#8A8196"
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
            highlightbackground="#E7DEEE",
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
            bg="#D8CBEA",
            fg="#4A4458",
            activebackground="#CBB8E0",
            relief="flat",
            bd=0,
            padx=14,
            pady=5,
            cursor="hand2",
            command=self.get_array
        ).pack(side="left")

        self.label_hasil_array = tk.Label(
            frame_get,
            text="Masukkan index kemudian tekan GET.",
            bg=self.bg_card,
            fg="#6B6478",
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
            fg="#9B7EBD"
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
            fg="#8A8196"
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
            highlightbackground="#E7DEEE",
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
            bg="#D8CBEA",
            fg="#4A4458",
            activebackground="#CBB8E0",
            relief="flat",
            bd=0,
            padx=14,
            pady=5,
            cursor="hand2",
            command=self.get_linked_list
        ).pack(side="left")

        self.label_hasil_linked = tk.Label(
            frame_get,
            text="Masukkan index kemudian tekan GET.",
            bg=self.bg_card,
            fg="#6B6478",
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
            fg="#9B7EBD"
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

    def halaman_tambah(self, jenis_awal=None):
        self._bersihkan_content()

        self._buat_header(
            "Tambah Pesanan",
            "Tambahkan pesanan baru ke Array dan Linked List."
        )

        card = tk.Frame(
            self.content,
            bg=self.bg_card,
            highlightbackground="#E7DEEE",
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
        if jenis_awal in ["REGULER", "PRIORITAS", "VIP"]:
            self.input_jenis.set(jenis_awal)
        else:
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
                fg="#6B6478"
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
            fg="#6B6478",
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
            bg="#B79ACB",
            fg="white",
            activebackground="#9F82B5",
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
                fg="#D98B8B"
            )
            return

        try:
            harga = float(harga_text)
        except ValueError:
            self.label_status_tambah.config(
                text="Harga harus berupa angka.",
                fg="#D98B8B"
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
            fg="#78A889"
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
            highlightbackground="#E7DEEE",
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
            fg="#6B6478"
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
            bg="#D98B8B",
            fg="white",
            activebackground="#C87575",
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
            fg="#6B6478",
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
                fg="#D98B8B"
            )
            return

        try:
            pesanan = self.array.get(index)
        except IndexError:
            self.label_status_hapus.config(
                text="Index berada di luar batas data.",
                fg="#D98B8B"
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
            fg="#78A889"
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
            fg="#8A8196"
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
            highlightbackground="#E7DEEE",
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
            fg="#8A8196"
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