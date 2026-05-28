from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.card import MDCard
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from viewmodels.savings_viewmodel import SavingsViewModel

class SavingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewmodel = SavingsViewModel()
        
        self.main_layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Header
        header_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        title = MDLabel(
            text="Target Tabungan",
            font_style="H5",
            theme_text_color="Primary",
            bold=True
        )
        back_btn = MDFlatButton(
            text="Kembali",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            on_release=lambda x: setattr(self.manager, 'current', 'dashboard')
        )
        header_layout.add_widget(title)
        header_layout.add_widget(back_btn)
        
        # Form Buat Target Baru in a Card
        form_card = MDCard(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(200),
            elevation=2,
            radius=[15]
        )
        
        form_title = MDLabel(text="Buat Target Baru", font_style="Subtitle1", bold=True, size_hint_y=None, height=dp(20))
        
        self.nama_target_input = MDTextField(hint_text="Nama Tabungan (Cth: Liburan)", icon_left="wallet-travel", mode="round")
        
        row_inputs = MDBoxLayout(orientation='horizontal', spacing=dp(10))
        self.nominal_target_input = MDTextField(hint_text="Target (Rp)", input_filter="float", icon_left="bullseye", mode="round")
        self.deadline_input = MDTextField(hint_text="Tenggat (YYYY-MM-DD)", icon_left="calendar", mode="round")
        row_inputs.add_widget(self.nominal_target_input)
        row_inputs.add_widget(self.deadline_input)
        
        btn_buat = MDRaisedButton(
            text="Simpan Target",
            md_bg_color=(0.1, 0.7, 0.3, 1),
            pos_hint={"center_x": .5},
            on_release=self.on_buat_target
        )
        
        form_card.add_widget(form_title)
        form_card.add_widget(self.nama_target_input)
        form_card.add_widget(row_inputs)
        form_card.add_widget(MDLabel(size_hint_y=None, height=dp(5)))
        form_card.add_widget(btn_buat)
        
        # ScrollView for Targets
        self.scroll = ScrollView()
        self.targets_list = MDBoxLayout(orientation='vertical', padding=[0, dp(10), 0, dp(10)], spacing=dp(15), size_hint_y=None)
        self.targets_list.bind(minimum_height=self.targets_list.setter('height'))
        self.scroll.add_widget(self.targets_list)
        
        self.main_layout.add_widget(header_layout)
        self.main_layout.add_widget(form_card)
        self.main_layout.add_widget(self.scroll)
        
        self.add_widget(self.main_layout)

    def on_enter(self, *args):
        self.refresh_targets()

    def refresh_targets(self):
        self.targets_list.clear_widgets()
        targets = self.viewmodel.get_all_targets()
        
        if not targets:
            self.targets_list.add_widget(MDLabel(text="Belum ada target tabungan.", halign="center", theme_text_color="Hint"))
            return
            
        for t in targets:
            card = MDCard(
                orientation='vertical',
                padding=dp(20),
                spacing=dp(10),
                size_hint_y=None,
                height=dp(240),
                elevation=3,
                radius=[15]
            )
            
            # Title
            lbl_title = MDLabel(text=f"{t['nama']}", font_style="H6", bold=True, size_hint_y=None, height=dp(30))
            
            # Progress Bar
            progress_percent = 0
            if t['target'] > 0:
                progress_percent = min(100.0, (t['terkumpul'] / t['target']) * 100)
            
            color_pb = (0.1, 0.7, 0.3, 1) if progress_percent >= 100 else (0.1, 0.5, 0.8, 1)
            pb = MDProgressBar(
                value=progress_percent, 
                max=100, 
                color=color_pb,
                size_hint_y=None, 
                height=dp(10)
            )
            
            # Info
            waktu_text = f"{t['sisa_hari']} hari lagi" if t['sisa_hari'] > 0 else "Lewat atau hari ini"
            lbl_info = MDLabel(
                text=f"Terkumpul: Rp {t['terkumpul']:,.0f} / Rp {t['target']:,.0f}\n"
                     f"Sisa: Rp {t['sisa']:,.0f} | Waktu: {waktu_text}\n"
                     f"Deadline: {t.get('deadline', '-')}",
                theme_text_color="Secondary",
                font_style="Caption"
            )
            
            # Actions
            action_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
            
            setoran_input = MDTextField(hint_text="Nominal Setor", input_filter="float", mode="round", size_hint_x=0.5)
            
            btn_setor = MDRaisedButton(
                text="Setor",
                md_bg_color=(0.1, 0.7, 0.3, 1),
                on_release=lambda x, tid=t['id_target'], inp=setoran_input: self.on_setor(tid, inp.text),
                size_hint_x=0.25
            )
            
            btn_hapus = MDFlatButton(
                text="Hapus",
                text_color=(0.9, 0.2, 0.2, 1),
                theme_text_color="Custom",
                on_release=lambda x, tid=t['id_target']: self.on_hapus(tid),
                size_hint_x=0.25
            )
            
            action_layout.add_widget(setoran_input)
            action_layout.add_widget(btn_setor)
            action_layout.add_widget(btn_hapus)
            
            card.add_widget(lbl_title)
            card.add_widget(pb)
            card.add_widget(lbl_info)
            card.add_widget(action_layout)
            
            self.targets_list.add_widget(card)

    def on_buat_target(self, instance):
        nama = self.nama_target_input.text
        try:
            nominal = float(self.nominal_target_input.text)
        except:
            nominal = 0
        deadline = self.deadline_input.text
        
        success, msg = self.viewmodel.add_target(nama, nominal, deadline)
        MDSnackbar(MDLabel(text=msg)).open()
        if success:
            self.nama_target_input.text = ""
            self.nominal_target_input.text = ""
            self.deadline_input.text = ""
            self.refresh_targets()

    def on_setor(self, id_target, nominal_text):
        try:
            nominal = float(nominal_text)
            success, msg = self.viewmodel.add_deposit(id_target, nominal, "")
            MDSnackbar(MDLabel(text=msg)).open()
            if success:
                self.refresh_targets()
        except:
            MDSnackbar(MDLabel(text="Nominal tidak valid")).open()

    def on_hapus(self, id_target):
        success, msg = self.viewmodel.delete_target(id_target)
        MDSnackbar(MDLabel(text=msg)).open()
        if success:
            self.refresh_targets()
