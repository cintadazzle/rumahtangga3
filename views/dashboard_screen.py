from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import MDSnackbar
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from viewmodels.dashboard_viewmodel import DashboardViewModel

class DashboardScreen(Screen):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewmodel = DashboardViewModel()
        
        # Main Layout
        self.main_layout = MDBoxLayout(orientation='vertical', spacing=10)
        
        # --- Top Header (Kode Keluarga & Anggota) ---
        header = MDBoxLayout(orientation='horizontal', padding=[15, 10, 15, 10], spacing=10, size_hint_y=None, height=dp(60))
        self.lbl_kode = MDLabel(text="Kode Keluarga: -", font_style="Subtitle1", bold=True, theme_text_color="Primary", size_hint_x=0.4)
        
        self.btn_anggota = MDFlatButton(text="Anggota: 0", on_release=self.show_anggota_dialog, size_hint_x=0.2)
        btn_gabung = MDRaisedButton(text="Gabung", md_bg_color="blue", on_release=self.show_join_dialog, size_hint_x=0.2)
        btn_logout = MDFlatButton(text="Keluar", on_release=self.do_logout, text_color=(1,0,0,1), size_hint_x=0.2)
        
        header.add_widget(self.lbl_kode)
        header.add_widget(self.btn_anggota)
        header.add_widget(btn_gabung)
        header.add_widget(btn_logout)
        
        # --- Balance & Progress Bar Card ---
        card_layout = MDBoxLayout(orientation='vertical', padding=[15, 0, 15, 0], size_hint_y=None, height=dp(250))
        balance_card = MDCard(orientation='vertical', padding=20, spacing=15, elevation=3, radius=[15])
        
        title = MDLabel(text="Total Saldo Saat Ini", halign="center", font_style="Subtitle1", theme_text_color="Secondary", size_hint_y=None, height=dp(20))
        self.saldo_label = MDLabel(text="Rp 0", halign="center", font_style="H4", theme_text_color="Primary", bold=True, size_hint_y=None, height=dp(40))
        self.jatah_label = MDLabel(text="Jatah Harian: Rp 0", halign="center", font_style="Subtitle2", size_hint_y=None, height=dp(20))
        
        # Grafik Pemasukan vs Pengeluaran menggunakan MDProgressBar
        grafik_box = MDBoxLayout(orientation='vertical', spacing=10)
        
        # Pemasukan
        box_pem = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20))
        self.lbl_pem = MDLabel(text="Pemasukan", theme_text_color="Custom", text_color=(0.1, 0.7, 0.3, 1), size_hint_x=0.4)
        self.pb_pem = MDProgressBar(value=0, color=(0.1, 0.7, 0.3, 1), size_hint_x=0.6, pos_hint={"center_y": .5})
        box_pem.add_widget(self.lbl_pem)
        box_pem.add_widget(self.pb_pem)
        
        # Pengeluaran
        box_pen = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20))
        self.lbl_pen = MDLabel(text="Pengeluaran", theme_text_color="Custom", text_color=(0.9, 0.2, 0.2, 1), size_hint_x=0.4)
        self.pb_pen = MDProgressBar(value=0, color=(0.9, 0.2, 0.2, 1), size_hint_x=0.6, pos_hint={"center_y": .5})
        box_pen.add_widget(self.lbl_pen)
        box_pen.add_widget(self.pb_pen)
        
        grafik_box.add_widget(box_pem)
        grafik_box.add_widget(box_pen)
        
        balance_card.add_widget(title)
        balance_card.add_widget(self.saldo_label)
        balance_card.add_widget(self.jatah_label)
        balance_card.add_widget(grafik_box)
        card_layout.add_widget(balance_card)
        
        # --- Bottom Navigation (Menu Transaksi & Tabungan) ---
        menu_layout = MDBoxLayout(orientation='horizontal', padding=[15, 10, 15, 0], spacing=15, size_hint_y=None, height=dp(60))
        btn_transaksi = MDRaisedButton(text="+ Catat Transaksi", size_hint_x=0.5, md_bg_color=(0.1, 0.6, 0.8, 1), on_release=lambda x: setattr(self.manager, 'current', 'transaction'))
        btn_tabungan = MDRaisedButton(text="Target Tabungan", size_hint_x=0.5, md_bg_color=(0.1, 0.8, 0.4, 1), on_release=lambda x: setattr(self.manager, 'current', 'savings'))
        menu_layout.add_widget(btn_transaksi)
        menu_layout.add_widget(btn_tabungan)
        
        # --- Recent Transactions List ---
        tx_title_box = MDBoxLayout(orientation='horizontal', padding=[15, 10, 15, 0], size_hint_y=None, height=dp(40))
        tx_title_box.add_widget(MDLabel(text="Riwayat Terakhir", font_style="Subtitle1", bold=True))
        
        self.scroll = ScrollView()
        self.tx_list = MDBoxLayout(orientation='vertical', padding=[15, 5, 15, 15], spacing=10, size_hint_y=None)
        self.tx_list.bind(minimum_height=self.tx_list.setter('height'))
        self.scroll.add_widget(self.tx_list)
        
        # Assemble
        self.main_layout.add_widget(header)
        self.main_layout.add_widget(card_layout)
        self.main_layout.add_widget(menu_layout)
        self.main_layout.add_widget(tx_title_box)
        self.main_layout.add_widget(self.scroll)
        
        self.add_widget(self.main_layout)

    def on_enter(self, *args):
        self.refresh_dashboard()

    def refresh_dashboard(self):
        self.data = self.viewmodel.get_dashboard_data()
        
        # Header
        self.lbl_kode.text = f"Kode: {self.data.get('pin_keluarga', '-')}"
        
        anggota = self.data.get('anggota_keluarga', [])
        self.btn_anggota.text = f"Anggota: {len(anggota)}"
        
        # Saldo & Jatah
        self.saldo_label.text = f"Rp {self.data['saldo']:,.0f}"
        self.jatah_label.text = f"Jatah Harian: Rp {self.data['jatah_harian']:,.0f}"
        
        if self.data['status_warna'] == 'hijau':
            self.jatah_label.theme_text_color = "Custom"
            self.jatah_label.text_color = (0.1, 0.7, 0.3, 1)
        elif self.data['status_warna'] == 'kuning':
            self.jatah_label.theme_text_color = "Custom"
            self.jatah_label.text_color = (0.8, 0.6, 0, 1)
        else:
            self.jatah_label.theme_text_color = "Custom"
            self.jatah_label.text_color = (0.9, 0.2, 0.2, 1)

        # Update Chart (Progress Bar)
        pem = self.data.get('total_pemasukan', 0)
        pen = self.data.get('total_pengeluaran', 0)
        max_val = max(pem, pen, 1)
        
        self.pb_pem.value = (pem / max_val) * 100
        self.lbl_pem.text = f"Masuk: Rp {pem:,.0f}"
        
        self.pb_pen.value = (pen / max_val) * 100
        self.lbl_pen.text = f"Keluar: Rp {pen:,.0f}"

        # Update Transaction List
        self.tx_list.clear_widgets()
        recent = self.data.get('recent_transactions', [])
        if not recent:
            self.tx_list.add_widget(MDLabel(text="Belum ada transaksi.", halign="center", theme_text_color="Hint"))
        else:
            for tx in recent:
                tx_card = MDCard(orientation='horizontal', padding=15, spacing=10, size_hint_y=None, height=dp(70), elevation=1)
                
                # Detail Transaksi
                info_box = MDBoxLayout(orientation='vertical')
                info_box.add_widget(MDLabel(text=f"{tx['kategori']}", font_style="Subtitle2"))
                info_box.add_widget(MDLabel(text=f"{tx['tanggal'][:10]} | {tx['keterangan']}", font_style="Caption", theme_text_color="Hint"))
                
                # Nominal
                sign = "+" if tx['tipe'] == 'pemasukan' else "-"
                color = (0.1, 0.7, 0.3, 1) if tx['tipe'] == 'pemasukan' else (0.9, 0.2, 0.2, 1)
                nominal_lbl = MDLabel(text=f"{sign}Rp {tx['nominal']:,.0f}", halign="right", font_style="Subtitle2", theme_text_color="Custom", text_color=color)
                
                tx_card.add_widget(info_box)
                tx_card.add_widget(nominal_lbl)
                self.tx_list.add_widget(tx_card)

    def show_join_dialog(self, instance):
        if not self.dialog:
            self.join_input = MDTextField(hint_text="Masukkan Kode Keluarga", mode="rectangle")
            self.dialog = MDDialog(
                title="Gabung Keluarga",
                type="custom",
                content_cls=self.join_input,
                buttons=[
                    MDFlatButton(text="Batal", on_release=lambda x: self.dialog.dismiss()),
                    MDRaisedButton(text="Gabung", on_release=self.process_join)
                ]
            )
        self.join_input.text = ""
        self.dialog.open()

    def process_join(self, instance):
        kode = self.join_input.text
        if not kode:
            return
            
        success, msg = self.viewmodel.join_keluarga(kode)
        MDSnackbar(MDLabel(text=msg)).open()
        if success:
            self.dialog.dismiss()
            self.refresh_dashboard()

    def show_anggota_dialog(self, instance):
        anggota = getattr(self, 'data', {}).get('anggota_keluarga', [])
        
        content = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        for a in anggota:
            lbl = MDLabel(text=f"- {a['nama']} ({a['email']})", size_hint_y=None, height=dp(30))
            content.add_widget(lbl)
            
        scroll = ScrollView(size_hint=(1, None), height=dp(150))
        scroll.add_widget(content)
        
        d = MDDialog(
            title=f"Anggota Keluarga ({len(anggota)})",
            type="custom",
            content_cls=scroll,
            buttons=[
                MDFlatButton(text="Tutup", on_release=lambda x: d.dismiss())
            ]
        )
        d.open()

    def do_logout(self, instance):
        self.manager.current = 'auth'
