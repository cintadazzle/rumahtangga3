from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from viewmodels.auth_viewmodel import AuthViewModel

class AuthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewmodel = AuthViewModel()
        
        # Background Layout
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), pos_hint={"center_x": .5, "center_y": .5})
        
        # Card Container for Login
        card = MDCard(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(20),
            size_hint=(0.85, None),
            height=dp(350),
            pos_hint={"center_x": .5, "center_y": .5},
            elevation=4,
            radius=[15]
        )
        
        title = MDLabel(
            text="FinanceManager",
            halign="center",
            font_style="H5",
            theme_text_color="Primary",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        
        subtitle = MDLabel(
            text="Silakan masuk ke akun Anda",
            halign="center",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20)
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
        
        btn_layout = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(90))
        
        login_btn = MDRaisedButton(
            text="Masuk",
            font_style="Button",
            pos_hint={"center_x": .5},
            size_hint_x=1,
            on_release=self.do_login
        )
        
        register_btn = MDFlatButton(
            text="Belum punya akun? Daftar",
            theme_text_color="Custom",
            text_color=(0.1, 0.6, 0.8, 1),
            pos_hint={"center_x": .5},
            on_release=lambda x: setattr(self.manager, 'current', 'register')
        )
        
        btn_layout.add_widget(login_btn)
        btn_layout.add_widget(register_btn)
        
        card.add_widget(title)
        card.add_widget(subtitle)
        card.add_widget(self.email_input)
        card.add_widget(self.password_input)
        card.add_widget(MDLabel(size_hint_y=None, height=dp(10))) # Spacer
        card.add_widget(btn_layout)
        
        # Center the card in the screen
        spacer_top = MDBoxLayout()
        spacer_bottom = MDBoxLayout()
        layout.add_widget(spacer_top)
        layout.add_widget(card)
        layout.add_widget(spacer_bottom)
        
        self.add_widget(layout)

    def do_login(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        
        success, msg = self.viewmodel.login(email, password)
        MDSnackbar(MDLabel(text=msg)).open()
        
        if success:
            self.email_input.text = ""
            self.password_input.text = ""
            self.manager.current = 'dashboard'
