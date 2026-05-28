import os

from kivy.app import App
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.image import AsyncImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.card import MDCard
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.utils import platform
from viewmodels.transaction_viewmodel import TransactionViewModel
from datetime import datetime

class TransactionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewmodel = TransactionViewModel()
        
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Header
        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        title = MDLabel(
            text="Catat Transaksi",
            font_style="H5",
            theme_text_color="Primary",
            bold=True
        )
        back_btn = MDFlatButton(
            text="Batal",
            theme_text_color="Error",
            on_release=lambda x: setattr(self.manager, 'current', 'dashboard')
        )
        header.add_widget(title)
        header.add_widget(back_btn)
        
        # Card Container
        card = MDCard(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None,
            height=dp(560),
            elevation=2,
            radius=[15]
        )
        
        # Tipe Transaksi Toggle
        self.tipe_transaksi = "pengeluaran"
        tipe_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(45))
        
        self.btn_pengeluaran = MDRaisedButton(
            text="Pengeluaran",
            md_bg_color=(0.9, 0.2, 0.2, 1),
            size_hint_x=0.5,
            on_release=lambda x: self.set_tipe("pengeluaran")
        )
        
        self.btn_pemasukan = MDRaisedButton(
            text="Pemasukan",
            md_bg_color=(0.8, 0.8, 0.8, 1),
            text_color=(0,0,0,1),
            size_hint_x=0.5,
            on_release=lambda x: self.set_tipe("pemasukan")
        )
        tipe_layout.add_widget(self.btn_pengeluaran)
        tipe_layout.add_widget(self.btn_pemasukan)
        
        self.current_receipt_path = ""
        self.receipt_image = AsyncImage(
            source="",
            size_hint_y=None,
            height=dp(180),
            allow_stretch=True,
            keep_ratio=True,
            opacity=0
        )
        
        # Inputs
        self.nominal_input = MDTextField(
            hint_text="Nominal (Rp)",
            input_filter="float",
            icon_left="cash",
            mode="rectangle"
        )
        
        # Spinner Kategori
        kategori_box = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=dp(50))
        kategori_lbl = MDLabel(text="Kategori:", size_hint_x=0.3)
        self.kategori_spinner = Spinner(
            text="Makan/Minum",
            values=("Makan/Minum", "Transportasi", "Tagihan", "Lainnya"),
            size_hint_x=0.7,
            background_color=(0.1, 0.6, 0.8, 1)
        )
        kategori_box.add_widget(kategori_lbl)
        kategori_box.add_widget(self.kategori_spinner)
        
        self.keterangan_input = MDTextField(
            hint_text="Keterangan / Catatan",
            icon_left="pencil",
            mode="rectangle"
        )
        
        card.add_widget(tipe_layout)
        card.add_widget(self.receipt_image)
        card.add_widget(self.nominal_input)
        card.add_widget(kategori_box)
        card.add_widget(self.keterangan_input)
        
        # Action Buttons
        btn_layout = MDBoxLayout(orientation='horizontal', spacing=dp(15), size_hint_y=None, height=dp(50))
        
        save_btn = MDRaisedButton(
            text="Simpan Manual",
            md_bg_color=(0.1, 0.7, 0.3, 1),
            size_hint_x=0.5,
            on_release=self.on_save_manual
        )
        
        ocr_btn = MDRaisedButton(
            text="Scan Struk (OCR)",
            md_bg_color=(0.1, 0.5, 0.8, 1),
            size_hint_x=0.5,
            on_release=self.on_scan_ocr
        )
        
        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(ocr_btn)
        
        layout.add_widget(header)
        layout.add_widget(card)
        layout.add_widget(btn_layout)
        layout.add_widget(MDBoxLayout()) # Spacer
        
        self.add_widget(layout)

    def set_tipe(self, tipe):
        self.tipe_transaksi = tipe
        if tipe == "pengeluaran":
            self.btn_pengeluaran.md_bg_color = (0.9, 0.2, 0.2, 1)
            self.btn_pengeluaran.text_color = (1,1,1,1)
            self.btn_pemasukan.md_bg_color = (0.8, 0.8, 0.8, 1)
            self.btn_pemasukan.text_color = (0,0,0,1)
            self.kategori_spinner.values = ("Makan/Minum", "Transportasi", "Tagihan", "Lainnya")
            self.kategori_spinner.text = "Makan/Minum"
        else:
            self.btn_pengeluaran.md_bg_color = (0.8, 0.8, 0.8, 1)
            self.btn_pengeluaran.text_color = (0,0,0,1)
            self.btn_pemasukan.md_bg_color = (0.1, 0.7, 0.3, 1)
            self.btn_pemasukan.text_color = (1,1,1,1)
            self.kategori_spinner.values = ("Gaji", "Bonus", "Investasi", "Lainnya")
            self.kategori_spinner.text = "Gaji"

    def on_save_manual(self, instance):
        nominal_text = self.nominal_input.text
        keterangan = self.keterangan_input.text
        
        if not nominal_text:
            MDSnackbar(MDLabel(text="Nominal tidak boleh kosong")).open()
            return
            
        try:
            nominal = float(nominal_text)
        except ValueError:
            MDSnackbar(MDLabel(text="Nominal harus berupa angka")).open()
            return

        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success, msg = self.viewmodel.add_manual_transaction(
            nominal=nominal,
            kategori=self.kategori_spinner.text,
            tipe=self.tipe_transaksi,
            keterangan=keterangan,
            date=date_now,
            foto_struk=self.current_receipt_path
        )
        
        MDSnackbar(MDLabel(text=msg)).open()
        
        if success:
            self.nominal_input.text = ""
            self.keterangan_input.text = ""
            self.current_receipt_path = ""
            self.receipt_image.source = ""
            self.receipt_image.opacity = 0
            self.manager.current = 'dashboard'

    def on_scan_ocr(self, instance):
        if platform == 'android':
            MDSnackbar(MDLabel(text="Membuka kamera...")).open()
            self.open_camera_for_ocr()
        else:
            MDSnackbar(MDLabel(text="Membuka file manager... (Windows/Desktop) ")).open()
            self.open_filechooser_for_ocr()

    def open_filechooser_for_ocr(self):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self.handle_ocr_selection)
        except Exception as e:
            print(f"FileChooser Error: {e}")
            MDSnackbar(MDLabel(text="File manager tidak tersedia. Pastikan plyer terpasang.")).open()

    def open_camera_for_ocr(self):
        try:
            from plyer import camera
            app = App.get_running_app()
            save_path = os.path.join(app.user_data_dir, 'ocr_receipt.jpg')
            camera.take_picture(filename=save_path, on_complete=self.handle_camera_capture)
        except Exception as e:
            print(f"Camera Error: {e}")
            MDSnackbar(MDLabel(text="Kamera tidak tersedia. Coba pilih gambar manual.")).open()
            self.open_filechooser_for_ocr()

    def handle_camera_capture(self, image_path):
        if not image_path or not os.path.exists(image_path):
            MDSnackbar(MDLabel(text="Gagal mengambil foto. Silakan coba lagi.")).open()
            return
        self.handle_ocr_selection([image_path])

    def update_receipt_preview(self, image_path):
        self.current_receipt_path = image_path
        self.receipt_image.source = image_path
        self.receipt_image.opacity = 1
        try:
            self.receipt_image.reload()
        except Exception:
            pass

    def handle_ocr_selection(self, selection):
        if not selection:
            MDSnackbar(MDLabel(text="Batal memilih gambar")).open()
            return
            
        image_path = selection[0]
        self.update_receipt_preview(image_path)
        MDSnackbar(MDLabel(text="Memproses struk, harap tunggu...")).open()
        
        success, msg, amount = self.viewmodel.process_receipt_ocr(image_path)
        if success and amount > 0:
            self.nominal_input.text = str(amount)
            MDSnackbar(MDLabel(text="Nominal berhasil didapatkan!")).open()
        else:
            MDSnackbar(MDLabel(text=msg)).open()
