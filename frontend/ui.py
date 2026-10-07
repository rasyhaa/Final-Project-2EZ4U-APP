import tkinter as tk
from tkinter import ttk
import time

from backend.m3_laporan import insertion_sort, merge_sort, linear_search, binary_search

from backend.m1_pesanan import load_pesanan, Pesanan
from backend.m2_antrean import (
    Stack,
    AntreanNaif,
    AntreanMelingkar,
    RiwayatUndoRedo,
    infix_ke_postfix,
    evaluasi_postfix,
    hitung_postfix_dengan_langkah
)


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

        # =========================
        # M2 - ANTREAN
        # =========================
        self.stack_m2 = Stack()
        self._m2_last_rows = []
        self._m2_table_heading = "DATA PESANAN TERKAIT OPERASI"
        self._m2_view_kind = "enqueue"
        self._m2_last_action = ""

        self.antrean_naif = AntreanNaif()
        # Kapasitas awal kecil; circular queue akan memperbesar kapasitas
        # otomatis sesuai aturan backend ketika penuh.
        self.antrean_melingkar = AntreanMelingkar(128)

        # Brief meminta kedua antrean memulai dari data pesanan yang sama.
        # Simpan OID agar antrean tetap ringan walaupun CSV berisi banyak baris.
        for indeks in range(self.array.size):
            pesanan_awal = self.array.get(indeks)
            # Brief M2 menetapkan data awal hanya pesanan berstatus ANTRE.
            if str(getattr(pesanan_awal, "status", "")).upper() == "ANTRE":
                self.antrean_naif.enqueue(pesanan_awal.oid)
                self.antrean_melingkar.enqueue(pesanan_awal.oid)

        self.riwayat_antrean = RiwayatUndoRedo(
            self.antrean_melingkar,
            self.antrean_naif
        )

        # Pagination
        self.halaman = 1
        self.data_per_halaman = 100
        self._m3_data_urut_oid = None
        self._m3_waktu_bangun_oid = 0.0
        self._m3_perbandingan_bangun_oid = 0

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

        menu_window = canvas.create_window(
            (0, 0),
            window=menu_frame,
            anchor="nw"
        )

        # Lebar menu mengikuti lebar canvas agar tidak terpotong.
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                menu_window,
                width=event.width
            )
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

        # Scroll mouse untuk Linux/Fedora dan Windows.
        def _scroll_menu(event):
            if getattr(event, "num", None) == 4:       # Linux: scroll up
                canvas.yview_scroll(-3, "units")
            elif getattr(event, "num", None) == 5:     # Linux: scroll down
                canvas.yview_scroll(3, "units")
            elif getattr(event, "delta", 0):           # Windows/macOS
                arah = -1 if event.delta > 0 else 1
                canvas.yview_scroll(arah * 3, "units")

        def _aktifkan_scroll(event=None):
            canvas.bind_all("<MouseWheel>", _scroll_menu)
            canvas.bind_all("<Button-4>", _scroll_menu)
            canvas.bind_all("<Button-5>", _scroll_menu)

        def _matikan_scroll(event=None):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        canvas.bind("<Enter>", _aktifkan_scroll)
        canvas.bind("<Leave>", _matikan_scroll)
        menu_frame.bind("<Enter>", _aktifkan_scroll)
        menu_frame.bind("<Leave>", _matikan_scroll)

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

        # ============================================================
        # M2 - ANTREAN
        # ============================================================
        tk.Label(
            menu_frame,
            text="M2 - ANTREAN",
            font=("Arial", 9, "bold"),
            bg=self.bg_sidebar,
            fg="#8A8196"
        ).pack(anchor="w", padx=12, pady=(12, 5))

        # Menu M2 dibuat persis mengikuti brief.
        self._buat_menu_button(
            menu_frame,
            "STACK - POSTFIX (MESIN KASIR)",
            self.halaman_kalkulator
        )
        self._buat_menu_button(
            menu_frame,
            "STACK - UNDO",
            self.menu_undo_m2
        )
        self._buat_menu_button(
            menu_frame,
            "STACK - REDO",
            self.menu_redo_m2
        )
        self._buat_menu_button(
            menu_frame,
            "QUEUE - ENQUEUE",
            self.menu_enqueue_m2
        )
        self._buat_menu_button(
            menu_frame,
            "QUEUE - DEQUEUE NAIF",
            self.menu_dequeue_naif_m2
        )
        self._buat_menu_button(
            menu_frame,
            "QUEUE - DEQUEUE CIRCULAR",
            self.menu_dequeue_circular_m2
        )

        # ============================================================
        # M3 - LAPORAN TERURUT
        # ============================================================
        tk.Label(
            menu_frame,
            text="M3 - LAPORAN TERURUT",
            font=("Arial", 9, "bold"),
            bg=self.bg_sidebar,
            fg="#8A8196"
        ).pack(anchor="w", padx=12, pady=(12, 5))

        self._buat_menu_button(menu_frame, "INSERTION SORT", self.halaman_m3_insertion)
        self._buat_menu_button(menu_frame, "MERGE SORT", self.halaman_m3_merge)
        self._buat_menu_button(menu_frame, "LINEAR SEARCH", self.halaman_m3_linear)
        self._buat_menu_button(menu_frame, "BINARY SEARCH", self.halaman_m3_binary)

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
    # M2 - ANTREAN
    # ============================================================

    def menu_undo_m2(self):
        self.halaman_m2_undo()

    def menu_redo_m2(self):
        self.halaman_m2_redo()

    def menu_enqueue_m2(self):
        self.halaman_m2_enqueue()

    def menu_dequeue_naif_m2(self):
        self.halaman_m2_dequeue_naif()

    def menu_dequeue_circular_m2(self):
        self.halaman_m2_dequeue_circular()

    def _halaman_m2_operasi(self, judul, deskripsi, jenis):
        """Halaman operasi M2 dengan komponen/tabel yang khusus untuk tiap menu."""
        self._bersihkan_content()
        self._m2_view_kind = jenis
        self._m2_last_action = ""
        self._m2_last_rows = []
        self._m2_table_heading = ""
        self._buat_header(judul, deskripsi)

        control = tk.Frame(self.content, bg=self.bg_card,
                           highlightbackground="#E7DEEE", highlightthickness=1)
        control.pack(fill="x", padx=22, pady=(4, 8))
        tk.Label(control, text=judul, font=("Arial", 11, "bold"),
                 bg=self.bg_card, fg=self.text_utama).pack(anchor="w", padx=14, pady=(8, 4))

        if jenis == "enqueue":
            tk.Label(control, text="Nama / ID pesanan baru:", bg=self.bg_card,
                     fg=self.text_utama).pack(anchor="w", padx=14)
            self.input_antrean = tk.Entry(control, width=32, font=("Arial", 10))
            self.input_antrean.pack(anchor="w", padx=14, pady=4)
            tk.Button(control, text="ENQUEUE", bg="#D8CBEA", fg=self.text_utama,
                      relief="flat", padx=18, command=self.enqueue_circular
                      ).pack(anchor="w", padx=14, pady=(0, 8))
            self._m2_table_heading = "Data pesanan yang ditambahkan ke belakang kedua antrean"
            self._m2_table_columns = ("kolom", "isi")
            headings = (("kolom", "kolom", 160), ("isi", "isi", 500))
        elif jenis in ("naif", "circular"):
            tk.Label(control, text=("Dequeue naif menghapus elemen depan lalu menggeser semua sisa elemen."
                                   if jenis == "naif" else
                                   "Circular queue memajukan front dengan modulo; elemen lain tidak digeser."),
                     bg=self.bg_card, fg="#6B6478", wraplength=850,
                     justify="left").pack(anchor="w", padx=14, pady=(0, 5))
            row = tk.Frame(control, bg=self.bg_card); row.pack(anchor="w", padx=14, pady=(0, 8))
            tk.Label(row, text="Jumlah dequeue:", bg=self.bg_card).pack(side="left")
            field = tk.Entry(row, width=8)
            field.insert(0, "1")
            field.pack(side="left", padx=8)
            if jenis == "naif":
                self.input_jumlah_naif = field
                command, btn = self.dequeue_naif, "JALANKAN DEQUEUE NAIF"
                self._m2_table_heading = "Pesanan yang keluar dari antrean naif"
                self._m2_table_columns = ("nomor", "oid", "pelanggan", "resto", "menu", "masuk")
                headings = (("nomor", "#", 40), ("oid", "oid", 95), ("pelanggan", "pelanggan", 125),
                            ("resto", "resto", 120), ("menu", "menu", 110), ("masuk", "masuk", 85))
            else:
                self.input_jumlah_circular = field
                command, btn = self.dequeue_circular, "JALANKAN DEQUEUE CIRCULAR"
                self._m2_table_heading = "Pesanan yang keluar dari circular queue"
                self._m2_table_columns = ("nomor", "oid", "pelanggan", "resto", "menu", "masuk")
                headings = (("nomor", "#", 40), ("oid", "oid", 95), ("pelanggan", "pelanggan", 125),
                            ("resto", "resto", 120), ("menu", "menu", 110), ("masuk", "masuk", 85))
            tk.Button(row, text=btn, bg="#D8CBEA" if jenis == "circular" else "#2C4260",
                      fg=self.text_utama if jenis == "circular" else "white",
                      relief="flat", padx=12, command=command).pack(side="left", padx=5)
        elif jenis in ("undo", "redo"):
            label = ("Undo membatalkan aksi antrean terakhir dan memulihkan data yang terkena aksi."
                     if jenis == "undo" else
                     "Redo menjalankan kembali aksi yang sebelumnya dibatalkan.")
            tk.Label(control, text=label, bg=self.bg_card, fg="#6B6478",
                     wraplength=850, justify="left").pack(anchor="w", padx=14, pady=(0, 6))
            tk.Button(control, text="UNDO" if jenis == "undo" else "REDO",
                      bg="#2C4260", fg="white", relief="flat", padx=24,
                      command=self.undo_antrean if jenis == "undo" else self.redo_antrean
                      ).pack(anchor="w", padx=14, pady=(0, 8))
            self._m2_table_heading = "Data pesanan yang dipulihkan" if jenis == "undo" else "Data pesanan yang dijalankan ulang"
            self._m2_table_columns = ("nomor", "oid", "pelanggan", "resto", "menu")
            headings = (("nomor", "#", 40), ("oid", "oid", 95), ("pelanggan", "pelanggan", 125),
                        ("resto", "resto", 120), ("menu", "menu", 110))
        else:
            self._m2_table_heading = "Hasil operasi"
            self._m2_table_columns = ("nomor", "hasil")
            headings = (("nomor", "#", 40), ("hasil", "hasil", 500))

        self.label_status_antrean = tk.Label(
            self.content, text="Siap menjalankan operasi.", bg="#F7F4E8",
            fg=self.text_utama, justify="left", anchor="w", wraplength=900,
            padx=10, pady=6
        )
        self.label_status_antrean.pack(fill="x", padx=22, pady=(0, 6))

        table_card = tk.Frame(self.content, bg=self.bg_card,
                              highlightbackground="#E7DEEE", highlightthickness=1)
        table_card.pack(fill="both", expand=True, padx=22, pady=(0, 6))
        self.label_m2_table_title = tk.Label(table_card, text=self._m2_table_heading,
                                             font=("Arial", 10, "bold"),
                                             bg=self.bg_card, fg=self.text_utama)
        self.label_m2_table_title.pack(anchor="w", padx=10, pady=(6, 3))
        wrap = tk.Frame(table_card, bg=self.bg_card)
        wrap.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        cols = self._m2_table_columns
        self.tree_m2_hasil = ttk.Treeview(wrap, columns=cols, show="headings", height=9)
        for col, heading, width in headings:
            self.tree_m2_hasil.heading(col, text=heading)
            self.tree_m2_hasil.column(col, width=width, minwidth=45,
                                      anchor="center" if col == "nomor" else "w", stretch=True)
        ys = ttk.Scrollbar(wrap, orient="vertical", command=self.tree_m2_hasil.yview)
        xs = ttk.Scrollbar(wrap, orient="horizontal", command=self.tree_m2_hasil.xview)
        self.tree_m2_hasil.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)
        self.tree_m2_hasil.grid(row=0, column=0, sticky="nsew")
        ys.grid(row=0, column=1, sticky="ns")
        xs.grid(row=1, column=0, sticky="ew")
        wrap.grid_rowconfigure(0, weight=1); wrap.grid_columnconfigure(0, weight=1)

        # Status ringkas ala contoh brief: jumlah data, kapasitas, pergeseran, dan stack.
        self.label_status_ringkas_m2 = tk.Label(
            self.content, text="", bg=self.bg_card, fg=self.text_utama,
            justify="left", anchor="w", wraplength=900, padx=10, pady=5
        )
        self.label_status_ringkas_m2.pack(fill="x", padx=22, pady=(0, 4))
        cmd = tk.Frame(self.content, bg=self.bg_card,
                       highlightbackground="#E7DEEE", highlightthickness=1)
        cmd.pack(fill="x", padx=22, pady=(0, 8))
        tk.Label(cmd, text="COMMAND / RIWAYAT OPERASI", font=("Arial", 8, "bold"),
                 bg=self.bg_card, fg=self.text_utama).pack(anchor="w", padx=8, pady=(4, 1))
        self.text_m2_command = tk.Text(cmd, height=4, wrap="none", font=("Courier", 8),
                                       bg="#FFFFFF", fg="#4A4458", relief="flat")
        self.text_m2_command.pack(fill="x", padx=6, pady=(0, 5))
        self._render_tabel_m2()
        self.perbarui_antrean()

    def _cari_data_pesanan_m2(self, oid):
        """Cari detail pesanan berdasarkan OID tanpa memakai dictionary/hash map."""
        for i in range(self.array.size):
            item = self.array.get(i)
            if str(getattr(item, "oid", "")) == str(oid):
                return item
        return None

    def _render_tabel_m2(self):
        if not hasattr(self, "tree_m2_hasil"):
            return
        for item in self.tree_m2_hasil.get_children():
            self.tree_m2_hasil.delete(item)
        if hasattr(self, "label_m2_table_title"):
            self.label_m2_table_title.config(text=getattr(self, "_m2_table_heading", "Hasil operasi"))
        kind = getattr(self, "_m2_view_kind", "enqueue")
        rows = getattr(self, "_m2_last_rows", [])
        if kind == "enqueue":
            oid = rows[0] if rows else "-"
            data = self._cari_data_pesanan_m2(oid)
            if data is not None:
                detail = [
                    ("oid", getattr(data, "oid", oid)),
                    ("pelanggan", getattr(data, "pelanggan", "-")),
                    ("resto", getattr(data, "resto", "-")),
                    ("menu", getattr(data, "menu", "-")),
                    ("harga", getattr(data, "harga", "-")),
                    ("masuk", getattr(data, "masuk", getattr(data, "waktu_masuk", "-"))),
                    ("status", "ANTRE")
                ]
            else:
                detail = [("oid / nama", oid), ("lokasi", "Belakang antrean naif dan circular"),
                          ("status", "ANTRE")]
            for key, value in detail:
                self.tree_m2_hasil.insert("", "end", values=(key, value))
            return

        for nomor, oid in enumerate(rows, start=1):
            data = self._cari_data_pesanan_m2(oid)
            if data is None:
                oid_val, pelanggan, resto, menu, masuk = str(oid), "-", "-", "-", "-"
            else:
                oid_val = getattr(data, "oid", oid)
                pelanggan = getattr(data, "pelanggan", "-")
                resto = getattr(data, "resto", "-")
                menu = getattr(data, "menu", "-")
                masuk = getattr(data, "masuk", getattr(data, "waktu_masuk",
                         getattr(data, "jam_masuk", getattr(data, "waktu", "-"))))
            if kind == "naif":
                values = (nomor, oid_val, pelanggan, resto, menu, masuk)
            elif kind == "circular":
                values = (nomor, oid_val, pelanggan, resto, menu, masuk)
            elif kind in ("undo", "redo"):
                values = (nomor, oid_val, pelanggan, resto, menu)
            else:
                values = (nomor, oid_val, pelanggan, resto, menu, masuk, "-")
            self.tree_m2_hasil.insert("", "end", values=values)

    def halaman_m2_enqueue(self):
        self._halaman_m2_operasi("QUEUE - ENQUEUE", "Menambahkan pesanan ke belakang kedua antrean untuk perbandingan yang adil.", "enqueue")

    def halaman_m2_dequeue_naif(self):
        self._halaman_m2_operasi("QUEUE - DEQUEUE NAIF", "Dequeue dengan larik biasa: elemen tersisa digeser ke kiri.", "naif")

    def halaman_m2_dequeue_circular(self):
        self._halaman_m2_operasi("QUEUE - DEQUEUE CIRCULAR", "Dequeue dengan circular queue: front bergerak secara melingkar tanpa pergeseran elemen.", "circular")

    def halaman_m2_undo(self):
        self._halaman_m2_operasi("STACK - UNDO", "Batalkan aksi antrean terakhir menggunakan stack riwayat.", "undo")

    def halaman_m2_redo(self):
        self._halaman_m2_operasi("STACK - REDO", "Ulangi aksi yang sebelumnya dibatalkan menggunakan stack redo.", "redo")

    def halaman_antrean(self):
        # Kompatibilitas dengan pemanggilan lama: arahkan ke menu enqueue.
        self.halaman_m2_enqueue()

    def enqueue_circular(self):
        nilai = self.input_antrean.get().strip()
        if not nilai:
            self.label_status_antrean.config(text="Isi ID/nama pesanan terlebih dahulu.", fg="#D98B8B")
            return
        mulai = time.perf_counter()
        berhasil = self.riwayat_antrean.enqueue(nilai)
        durasi = (time.perf_counter() - mulai) * 1000
        self.input_antrean.delete(0, tk.END)
        if berhasil:
            self._m2_view_kind = "enqueue"
            self._m2_last_rows = [nilai]
            self._m2_table_heading = "ENQUEUE — PESANAN BARU DI BELAKANG KEDUA ANTREAN"
        self.label_status_antrean.config(
            text=(f"{nilai} ditambahkan ke KEDUA antrean.\n"
                  f"Enqueue: naif O(1) append dan circular O(1) amortized | waktu gabungan {durasi:.3f} ms"),
            fg="#78A889" if berhasil else "#D98B8B"
        )
        self.perbarui_antrean()

    def dequeue_circular(self):
        try:
            jumlah = max(1, int(self.input_jumlah_circular.get()))
        except (ValueError, AttributeError):
            jumlah = 1
        mulai = time.perf_counter()
        keluar = []
        for _ in range(jumlah):
            nilai = self.riwayat_antrean.dequeue_circular()
            if nilai is None:
                break
            keluar.append(nilai)
        durasi = (time.perf_counter() - mulai) * 1000
        if keluar:
            self._m2_view_kind = "circular"
            self._m2_last_rows = list(keluar)
            self._m2_table_heading = "Pesanan yang keluar dari circular queue"
            self._m2_front_after = self.antrean_melingkar.front
            self.label_status_antrean.config(
                text=(f"{len(keluar)} pesanan keluar dari circular queue: {', '.join(str(x) for x in keluar[:8])}"
                      f"{' ...' if len(keluar) > 8 else ''}\nPergeseran elemen: 0 | Waktu: {durasi:.3f} ms"),
                fg="#78A889"
            )
        else:
            self.label_status_antrean.config(text="Circular queue kosong.", fg="#D98B8B")
        self.perbarui_antrean()

    def _uraikan_aksi_riwayat(self, aksi, undo=True):
        if aksi is None:
            return "Tidak ada aksi."
        jenis = aksi[0]
        nilai = aksi[1]
        if jenis == "ENQUEUE":
            if undo:
                return (f"Pembatalan ENQUEUE: {nilai} dikeluarkan dari BELAKANG "
                        "kedua antrean (naif dan circular).")
            return (f"REDO ENQUEUE: {nilai} ditambahkan kembali ke BELAKANG "
                    "kedua antrean (naif dan circular).")
        if jenis == "DEQUEUE":
            daftar = ", ".join(str(x) for x in nilai)
            if undo:
                return f"Pembatalan DEQUEUE: {len(nilai)} pesanan ({daftar}) dipulihkan ke DEPAN kedua antrean."
            return f"REDO DEQUEUE: {len(nilai)} pesanan ({daftar}) dikeluarkan lagi dari kedua antrean."
        if jenis == "DEQUEUE_NAIF":
            daftar = ", ".join(str(x) for x in nilai)
            if undo:
                return f"Pembatalan DEQUEUE NAIF: {len(nilai)} pesanan ({daftar}) dipulihkan ke DEPAN antrean naif."
            return f"REDO DEQUEUE NAIF: {len(nilai)} pesanan ({daftar}) dikeluarkan lagi dari antrean naif."
        if jenis == "DEQUEUE_CIRCULAR":
            daftar = ", ".join(str(x) for x in nilai)
            if undo:
                return f"Pembatalan DEQUEUE CIRCULAR: {len(nilai)} pesanan ({daftar}) dipulihkan ke DEPAN circular queue."
            return f"REDO DEQUEUE CIRCULAR: {len(nilai)} pesanan ({daftar}) dikeluarkan lagi dari circular queue."
        return "Aksi riwayat tidak dikenali."

    def undo_antrean(self):
        aksi = self.riwayat_antrean.undo_stack.peek()
        if aksi is None:
            self.label_status_antrean.config(
                text="Stack undo kosong; tidak ada aksi yang dapat dibatalkan.",
                fg="#D98B8B"
            )
            self.perbarui_antrean()
            return
        mulai = time.perf_counter()
        berhasil = self.riwayat_antrean.undo()
        durasi = (time.perf_counter() - mulai) * 1000
        if berhasil:
            self._m2_view_kind = "undo"
            self._m2_last_action = aksi
            self._m2_last_rows = list(aksi[1]) if isinstance(aksi[1], list) else [aksi[1]]
            self._m2_table_heading = "STACK UNDO — AKSI YANG DIBATALKAN"
            self.label_status_antrean.config(
                text=self._uraikan_aksi_riwayat(aksi, undo=True) +
                     f"\nWaktu undo: {durasi:.3f} ms | Stack undo: {self.riwayat_antrean.ukuran_undo()} | Stack redo: {self.riwayat_antrean.ukuran_redo()}",
                fg="#78A889"
            )
        self.perbarui_antrean()

    def redo_antrean(self):
        aksi = self.riwayat_antrean.redo_stack.peek()
        if aksi is None:
            self.label_status_antrean.config(
                text="Stack redo kosong; tidak ada aksi yang dapat diulang.",
                fg="#D98B8B"
            )
            self.perbarui_antrean()
            return
        mulai = time.perf_counter()
        berhasil = self.riwayat_antrean.redo()
        durasi = (time.perf_counter() - mulai) * 1000
        if berhasil:
            self._m2_view_kind = "redo"
            self._m2_last_action = aksi
            self._m2_last_rows = list(aksi[1]) if isinstance(aksi[1], list) else [aksi[1]]
            self._m2_table_heading = "STACK REDO — AKSI YANG DIULANG"
            self.label_status_antrean.config(
                text=self._uraikan_aksi_riwayat(aksi, undo=False) +
                     f"\nWaktu redo: {durasi:.3f} ms | Stack undo: {self.riwayat_antrean.ukuran_undo()} | Stack redo: {self.riwayat_antrean.ukuran_redo()}",
                fg="#78A889"
            )
        self.perbarui_antrean()

    def perbarui_antrean(self):
        if hasattr(self, "label_status_ringkas_m2"):
            self.label_status_ringkas_m2.config(
                text=(f"Antrean naif: {self.antrean_naif.ukuran():,} | "
                      f"Circular: {self.antrean_melingkar.ukuran():,} | "
                      f"Kapasitas circular: {self.antrean_melingkar.kapasitas:,} | "
                      f"Total pergeseran naif: {self.antrean_naif.total_pergeseran:,} | "
                      f"Undo: {self.riwayat_antrean.ukuran_undo()} | "
                      f"Redo: {self.riwayat_antrean.ukuran_redo()}")
            )
        if hasattr(self, "text_m2_command"):
            self.text_m2_command.delete("1.0", tk.END)
            undo_data = self.riwayat_antrean.undo_stack
            redo_data = self.riwayat_antrean.redo_stack
            entries = []
            for i in range(min(4, undo_data.ukuran())):
                action = undo_data.data[undo_data.top-i]
                entries.append(f"UNDO-STACK  | {action[0]} | {str(action[1])[:50]}")
            for i in range(min(3, redo_data.ukuran())):
                action = redo_data.data[redo_data.top-i]
                entries.append(f"REDO-STACK  | {action[0]} | {str(action[1])[:50]}")
            if not entries:
                entries = ["Belum ada riwayat aksi antrean."]
            self.text_m2_command.insert("1.0", "\\n".join(entries))
        self._render_tabel_m2()

    def enqueue_naif(self):
        # Enqueue selalu dilakukan ke kedua antrean agar dataset pembanding tetap sama.
        self.enqueue_circular()

    def dequeue_naif(self):
        try:
            jumlah = max(1, int(self.input_jumlah_naif.get()))
        except (ValueError, AttributeError):
            jumlah = 1
        mulai = time.perf_counter()
        keluar = []
        geser_awal = self.antrean_naif.total_pergeseran
        for _ in range(jumlah):
            nilai = self.riwayat_antrean.dequeue_naif()
            if nilai is None:
                break
            keluar.append(nilai)
        durasi = (time.perf_counter() - mulai) * 1000
        geser = self.antrean_naif.total_pergeseran - geser_awal
        if keluar:
            self._m2_view_kind = "naif"
            self._m2_last_rows = list(keluar)
            self._m2_table_heading = "Pesanan yang keluar dari antrean naif"
            self._m2_shift_count = geser
            self.label_status_antrean.config(
                text=(f"{len(keluar)} pesanan keluar dari antrean naif: {', '.join(str(x) for x in keluar[:8])}"
                      f"{' ...' if len(keluar) > 8 else ''}\nElemen digeser: {geser:,} | Waktu: {durasi:.3f} ms"),
                fg="#78A889"
            )
        else:
            self.label_status_antrean.config(text="Antrean naif kosong.", fg="#D98B8B")
        self.perbarui_antrean()

    def halaman_kalkulator(self):
        self._bersihkan_content()
        self._buat_header("M2 — Stack: Hitung Struk Lewat Postfix",
                          "Konversi infix ke postfix menggunakan stack operator, lalu evaluasi postfix dengan stack angka.")
        control = tk.Frame(self.content, bg=self.bg_card,
                           highlightbackground="#E7DEEE", highlightthickness=1)
        control.pack(fill="x", padx=22, pady=(4, 8))
        tk.Label(control, text="Struk belanja (infix)", font=("Arial", 10, "bold"),
                 bg=self.bg_card, fg=self.text_utama).pack(anchor="w", padx=14, pady=(8, 3))
        self.input_ekspresi = tk.Entry(control, font=("Arial", 11), width=55)
        self.input_ekspresi.pack(anchor="w", padx=14, pady=(0, 5))
        self.input_ekspresi.insert(0, "(3 * 12000) + (2 * 8500) - 5000")
        tk.Button(control, text="HITUNG", bg="#2C4260", fg="white",
                  relief="flat", padx=22, command=self.hitung_kalkulator
                  ).pack(anchor="w", padx=14, pady=(0, 8))
        self.label_hasil_kalkulator = tk.Label(
            self.content, text="Postfix: - | TOTAL: -",
            bg="#F7F4E8", fg=self.text_utama, justify="left",
            anchor="w", padx=10, pady=6
        )
        self.label_hasil_kalkulator.pack(fill="x", padx=22, pady=(0, 6))
        card = tk.Frame(self.content, bg=self.bg_card,
                        highlightbackground="#E7DEEE", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=22, pady=(0, 7))
        tk.Label(card, text="LANGKAH STACK (infix → postfix → evaluasi)",
                 font=("Arial", 10, "bold"), bg=self.bg_card,
                 fg=self.text_utama).pack(anchor="w", padx=10, pady=(6, 3))
        wrap = tk.Frame(card, bg=self.bg_card); wrap.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        cols=("langkah","token","tindakan","stack","output")
        self.tree_kasir = ttk.Treeview(wrap, columns=cols, show="headings", height=13)
        for col, title, width in [
            ("langkah","langkah",65),("token","token",80),("tindakan","tindakan",230),
            ("stack","stack",180),("output","output / stack angka",230)]:
            self.tree_kasir.heading(col,text=title)
            self.tree_kasir.column(col,width=width,minwidth=50,anchor="w",stretch=True)
        ys=ttk.Scrollbar(wrap,orient="vertical",command=self.tree_kasir.yview)
        xs=ttk.Scrollbar(wrap,orient="horizontal",command=self.tree_kasir.xview)
        self.tree_kasir.configure(yscrollcommand=ys.set,xscrollcommand=xs.set)
        self.tree_kasir.grid(row=0,column=0,sticky="nsew"); ys.grid(row=0,column=1,sticky="ns")
        xs.grid(row=1,column=0,sticky="ew")
        wrap.grid_rowconfigure(0,weight=1); wrap.grid_columnconfigure(0,weight=1)
        self.text_m2_command = tk.Text(self.content, height=3, wrap="none",
                                       font=("Courier",8), bg="white", fg=self.text_utama,
                                       relief="flat")
        self.text_m2_command.pack(fill="x", padx=22, pady=(0, 8))
        self.text_m2_command.insert("1.0","stack_postfix  → M2 → stack")

    def hitung_kalkulator(self):
        ekspresi = self.input_ekspresi.get().strip()
        for item in self.tree_kasir.get_children():
            self.tree_kasir.delete(item)
        try:
            postfix = infix_ke_postfix(ekspresi)
            hasil, langkah_eval = hitung_postfix_dengan_langkah(postfix)
            # Tokenizer sederhana untuk menampilkan jejak konversi sesuai alur stack.
            tokens=[]
            i=0
            while i < len(ekspresi):
                ch=ekspresi[i]
                if ch.isspace():
                    i+=1
                elif ch.isdigit() or ch==".":
                    token=ch; i+=1
                    while i<len(ekspresi) and (ekspresi[i].isdigit() or ekspresi[i]=="."):
                        token+=ekspresi[i]; i+=1
                    tokens.append(token)
                elif ch in "+-*/()":
                    tokens.append(ch); i+=1
                else:
                    raise ValueError("Karakter tidak didukung: "+ch)
            opstack=[]
            output=[]
            step=0
            def addrow(token, action, stackval, outval):
                nonlocal step
                step+=1
                self.tree_kasir.insert("","end",values=(step,token,action,
                    " ".join(opstack) if opstack else "kosong",
                    " ".join(output) if output else "kosong"))
            def prioritas(op):
                if op == "+" or op == "-":
                    return 1
                if op == "*" or op == "/":
                    return 2
                return 0
            for token in tokens:
                if token.replace(".","",1).isdigit():
                    output.append(token); addrow(token,"operand, langsung ke output",opstack,output)
                elif token=="(":
                    opstack.append(token); addrow(token,"push ( ke stack",opstack,output)
                elif token==")":
                    while opstack and opstack[-1]!="(":
                        output.append(opstack.pop()); addrow(token,"pop operator ke output",opstack,output)
                    if not opstack: raise ValueError("Kurung tidak berpasangan")
                    opstack.pop(); addrow(token,"buang tanda (",opstack,output)
                else:
                    while opstack and opstack[-1]!="(" and prioritas(opstack[-1])>=prioritas(token):
                        output.append(opstack.pop()); addrow(token,"pop operator prioritas >= token",opstack,output)
                    opstack.append(token); addrow(token,"push operator",opstack,output)
            while opstack:
                if opstack[-1]=="(": raise ValueError("Kurung tidak berpasangan")
                output.append(opstack.pop()); addrow("akhir","pop sisa operator",opstack,output)
            # Tampilkan proses evaluasi postfix memakai stack angka di kolom output.
            nums=[]
            for token in postfix.split():
                if token.replace(".","",1).isdigit():
                    nums.append(float(token))
                    addrow(token,"push angka ke stack evaluasi",opstack,[" ".join(str(x) for x in nums)])
                else:
                    b=nums.pop(); a=nums.pop()
                    if token=="+": res=a+b
                    elif token=="-": res=a-b
                    elif token=="*": res=a*b
                    elif token=="/": res=a/b
                    nums.append(res)
                    addrow(token,f"pop {a} dan {b}; hitung {a} {token} {b}",opstack,[str(x) for x in nums])
            if isinstance(hasil,float) and hasil.is_integer(): hasil=int(hasil)
            self.label_hasil_kalkulator.config(text=f"Struk: {ekspresi}    |    Postfix: {postfix}    |    TOTAL: Rp {hasil:,}".replace(",","."),
                                               fg=self.text_utama)
            self.text_m2_command.delete("1.0",tk.END)
            self.text_m2_command.insert("1.0",f"stack_postfix  → M2 → stack     {hasil}")
        except Exception as error:
            self.label_hasil_kalkulator.config(text=f"Ekspresi tidak valid: {error}",fg="#D98B8B")

    # ============================================================
    # M3 - LAPORAN TERURUT
    # ============================================================

    def _data_m3(self):
        return [self.array.get(i) for i in range(self.array.size)]

    def _halaman_m3_base(self, judul, deskripsi):
        self._bersihkan_content()
        self._buat_header(judul, deskripsi)
        card = tk.Frame(self.content, bg=self.bg_card,
                        highlightbackground="#E7DEEE", highlightthickness=1)
        card.pack(fill="x", padx=22, pady=(4, 10))
        return card

    def _tabel_m3(self, parent, data, batas=200):
        frame = tk.Frame(parent, bg=self.bg_card)
        frame.pack(fill="both", expand=True, padx=22, pady=(0, 10))
        cols = ("nomor", "oid", "pelanggan", "resto", "menu", "harga")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        for col, heading, width in (
            ("nomor", "#", 45), ("oid", "oid", 110), ("pelanggan", "pelanggan", 150),
            ("resto", "resto", 140), ("menu", "menu", 160), ("harga", "harga", 100)
        ):
            tree.heading(col, text=heading)
            tree.column(col, width=width, anchor="center" if col == "nomor" else "w")
        ys = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        xs = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)
        tree.grid(row=0, column=0, sticky="nsew")
        ys.grid(row=0, column=1, sticky="ns")
        xs.grid(row=1, column=0, sticky="ew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        for i in range(len(data)):
            if i >= batas:
                break
            item = data[i]
            tree.insert("", "end", values=(
                i + 1, item.oid, item.pelanggan, item.resto, item.menu,
                f"Rp {int(item.harga):,}".replace(",", ".")
            ))
        return tree

    def _tabel_m3_search(self, parent, item):
        """Tabel hasil pencarian dengan seluruh atribut pesanan untuk M3."""
        frame = tk.Frame(parent, bg=self.bg_card)
        frame.pack(fill="both", expand=True, padx=22, pady=(0, 10))
        cols = ("nomor", "oid", "pelanggan", "resto", "menu", "harga",
                "prioritas", "masuk", "selesai", "status")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=5)
        headings = (
            ("nomor", "#", 45),
            ("oid", "oid", 110),
            ("pelanggan", "pelanggan", 145),
            ("resto", "resto", 135),
            ("menu", "menu", 150),
            ("harga", "harga", 100),
            ("prioritas", "prioritas", 85),
            ("masuk", "masuk", 120),
            ("selesai", "selesai", 120),
            ("status", "status", 110),
        )
        for col, heading, width in headings:
            tree.heading(col, text=heading)
            tree.column(col, width=width, anchor="center" if col in ("nomor", "prioritas") else "w")
        ys = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        xs = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)
        tree.grid(row=0, column=0, sticky="nsew")
        ys.grid(row=0, column=1, sticky="ns")
        xs.grid(row=1, column=0, sticky="ew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        masuk = getattr(item, "t_masuk_detik", None)
        selesai = getattr(item, "t_selesai_detik", None)
        masuk = "-" if masuk is None else f"{masuk} detik"
        selesai = "-" if selesai is None else f"{selesai} detik"
        tree.insert("", "end", values=(
            1, item.oid, item.pelanggan, item.resto, item.menu,
            f"Rp {int(item.harga):,}".replace(",", "."),
            item.prioritas, masuk, selesai, item.status
        ))
        return tree

    def _halaman_m3_sort(self, algoritma):
        judul = "M3 — " + ("Insertion Sort" if algoritma == "insertion" else "Merge Sort")
        card = self._halaman_m3_base(
            judul,
            "Urutkan data pesanan berdasarkan harga atau OID dan amati perbandingan serta waktu proses."
        )
        row = tk.Frame(card, bg=self.bg_card)
        row.pack(anchor="w", padx=15, pady=12)
        tk.Label(row, text="Kunci:", bg=self.bg_card).pack(side="left")
        pilihan = ttk.Combobox(row, values=("harga", "oid"), state="readonly", width=12)
        pilihan.set("harga")
        pilihan.pack(side="left", padx=8)
        tk.Label(row, text="Jumlah data (0 = semua):", bg=self.bg_card).pack(side="left", padx=(12, 0))
        jumlah = tk.Entry(row, width=12)
        jumlah.insert(0, "2000")
        jumlah.pack(side="left", padx=8)
        status = tk.Label(card, text="Belum ada proses sorting.", bg=self.bg_card,
                          fg=self.text_utama, justify="left", wraplength=900)
        status.pack(anchor="w", padx=15, pady=(0, 10))
        holder = tk.Frame(self.content, bg=self.bg_utama)
        holder.pack(fill="both", expand=True)

        def jalankan():
            try:
                n = int(jumlah.get())
                if n < 0:
                    raise ValueError
            except ValueError:
                status.config(text="Jumlah harus bilangan bulat >= 0.", fg="#D98B8B")
                return
            total = self.array.size
            if n == 0:
                n = total
            if n > total:
                status.config(text=f"Jumlah melebihi data tersedia ({total}).", fg="#D98B8B")
                return
            if algoritma == "insertion" and n > 20000:
                status.config(text="DITOLAK: batas Insertion Sort adalah 20.000 baris. Gunakan Merge Sort untuk data penuh.",
                              fg="#D98B8B")
                return
            data = [self.array.get(i) for i in range(n)]
            if algoritma == "insertion":
                hasil, perbandingan, durasi = insertion_sort(data, pilihan.get())
                nama = "Insertion Sort"
            else:
                hasil, perbandingan, durasi = merge_sort(data, pilihan.get())
                nama = "Merge Sort"
            status.config(text=f"{n:,} pesanan terurut berdasarkan {pilihan.get()} | "
                               f"{perbandingan:,} perbandingan | {durasi:.3f} ms".replace(",", "."),
                          fg=self.text_utama)
            for widget in holder.winfo_children():
                widget.destroy()
            self._tabel_m3(holder, hasil)

        tk.Button(row, text="JALANKAN SORT", bg="#D8CBEA", fg=self.text_utama,
                  relief="flat", padx=14, command=jalankan).pack(side="left", padx=8)

    def halaman_m3_insertion(self):
        self._halaman_m3_sort("insertion")

    def halaman_m3_merge(self):
        self._halaman_m3_sort("merge")

    def _halaman_m3_search(self, binary=False):
        judul = "M3 — Binary Search" if binary else "M3 — Linear Search"
        card = self._halaman_m3_base(
            judul,
            "Cari pesanan berdasarkan OID. Binary Search membangun daftar terurut OID dengan Merge Sort satu kali."
        )
        row = tk.Frame(card, bg=self.bg_card)
        row.pack(anchor="w", padx=15, pady=12)
        tk.Label(row, text="OID:", bg=self.bg_card).pack(side="left")
        entry = tk.Entry(row, width=24)
        entry.pack(side="left", padx=8)
        status = tk.Label(card, text="Masukkan OID lalu tekan CARI.", bg=self.bg_card,
                          fg=self.text_utama, justify="left", wraplength=900)
        status.pack(anchor="w", padx=15, pady=(0, 12))
        holder = tk.Frame(self.content, bg=self.bg_utama)
        holder.pack(fill="both", expand=True)

        def cari():
            target = entry.get().strip()
            if not target:
                status.config(text="OID wajib diisi.", fg="#D98B8B")
                return
            data = self._data_m3()
            if binary:
                if self._m3_data_urut_oid is None or len(self._m3_data_urut_oid) != len(data):
                    mulai = time.perf_counter()
                    terurut, cmp_bangun, durasi_bangun = merge_sort(data, "oid")
                    self._m3_data_urut_oid = terurut
                    self._m3_perbandingan_bangun_oid = cmp_bangun
                    self._m3_waktu_bangun_oid = durasi_bangun
                idx, cmp_cari, durasi_cari = binary_search(self._m3_data_urut_oid, target)
                found_data = self._m3_data_urut_oid[idx] if idx >= 0 else None
                teks = (f"Daftar terurut OID dibangun dengan Merge Sort: "
                        f"{self._m3_perbandingan_bangun_oid:,} perbandingan, "
                        f"{self._m3_waktu_bangun_oid:.3f} ms.\n".replace(",", "."))
                teks += (f"Ditemukan di baris {idx + 1} | {cmp_cari} perbandingan | "
                         f"{durasi_cari:.6f} ms" if idx >= 0 else
                         f"OID tidak ditemukan | {cmp_cari} perbandingan | {durasi_cari:.6f} ms")
            else:
                idx, cmp_cari, durasi_cari = linear_search(data, target)
                found_data = data[idx] if idx >= 0 else None
                teks = (f"Ditemukan di indeks {idx} | {cmp_cari:,} perbandingan | "
                        f"{durasi_cari:.6f} ms".replace(",", ".") if idx >= 0 else
                        f"OID tidak ditemukan | {cmp_cari:,} perbandingan | "
                        f"{durasi_cari:.6f} ms".replace(",", "."))
            status.config(text=teks, fg=self.text_utama if found_data is not None else "#D98B8B")
            for widget in holder.winfo_children():
                widget.destroy()
            if found_data is not None:
                self._tabel_m3_search(holder, found_data)

        tk.Button(row, text="CARI", bg="#D8CBEA", fg=self.text_utama,
                  relief="flat", padx=18, command=cari).pack(side="left", padx=8)

    def halaman_m3_linear(self):
        self._halaman_m3_search(False)

    def halaman_m3_binary(self):
        self._halaman_m3_search(True)

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