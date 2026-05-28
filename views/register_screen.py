from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from viewmodels.auth_viewmodel import AuthViewModel

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewmodel = AuthViewModel()
        
        # Background Layout
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), pos_hint={"center_x": .5, "center_y": .5})
        
        # Card Container for Register
        card = MDCard(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(15),
            size_hint=(0.9, None),
            height=dp(520),
            pos_hint={"center_x": .5, "center_y": .5},
            elevation=4,
            radius=[15]
        )
        
        title = MDLabel(
            text="Buat Akun",
            halign="center",
            font_style="H5",
            theme_text_color="Primary",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        
        subtitle = MDLabel(
            text="Bergabung dan kelola keuangan bersama",
            halign="center",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20)
        )
        
        self.nama_input = MDTextField(
            hint_text="Nama Lengkap",
            icon_left="account",
            mode="round",
            size_hint_x=1
        )
        
        self.email_input = MDTextField(
            hint_text="Email",
            icon_left="email",
            mode="round",
            size_hint_x=1
        )
        
        self.password_input = MDTextField(
            hint_text="Password",
            icon_left="key-variant",
            mode="round",
            password=True,
            size_hint_x=1
        )
        
        self.confirm_password_input = MDTextField(
            hint_text="Konfirmasi Password",
            icon_left="key-variant",
            mode="round",
            password=True,
            size_hint_x=1
        )
        
        self.kode_keluarga_input = MDTextField(
            hint_text="Kode Undangan (Opsional)",
            icon_left="account-group",
            mode="round",
            size_hint_x=1
        )
        
        btn_layout = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(90))
        
        register_btn = MDRaisedButton(
            text="Daftar",
            pos_hint={"center_x": .5},
            size_hint_x=1,
            on_release=self.do_register
        )
        
        back_btn = MDFlatButton(
            text="Kembali ke Login",
            pos_hint={"center_x": .5},
            on_release=lambda x: setattr(self.manager, 'current', 'auth')
        )
        
        btn_layout.add_widget(register_btn)
        btn_layout.add_widget(back_btn)
        
        card.add_widget(title)
        card.add_widget(subtitle)
        card.add_widget(self.nama_input)
        card.add_widget(self.email_input)
        card.add_widget(self.password_input)
        card.add_widget(self.confirm_password_input)
        card.add_widget(self.kode_keluarga_input)
        card.add_widget(MDLabel(size_hint_y=None, height=dp(10))) # Spacer
        card.add_widget(btn_layout)
        
        # Center the card
        spacer_top = MDBoxLayout()
        spacer_bottom = MDBoxLayout()
        layout.add_widget(spacer_top)
        layout.add_widget(card)
        layout.add_widget(spacer_bottom)
        
        self.add_widget(layout)

    def do_register(self, instance):
        nama = self.nama_input.text
        email = self.email_input.text
        password = self.password_input.text
        confirm = self.confirm_password_input.text
        kode = self.kode_keluarga_input.text
        
        success, msg = self.viewmodel.register(nama, email, password, confirm, kode)
        MDSnackbar(MDLabel(text=msg)).open()
        
        if success:
            self.nama_input.text = ""
            self.email_input.text = ""
            self.password_input.text = ""
            self.confirm_password_input.text = ""
            self.kode_keluarga_input.text = ""
            self.manager.current = 'auth'
