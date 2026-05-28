from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from models.database import init_db
from views.auth_screen import AuthScreen
from views.dashboard_screen import DashboardScreen
from views.transaction_screen import TransactionScreen
from views.savings_screen import SavingsScreen
from views.register_screen import RegisterScreen

class FinanceManagerApp(MDApp):
    def build(self):
        # Inisialisasi Database
        init_db()
        
        # Tema Aplikasi (Warna dan Gaya)
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        
        # Setup Screen Manager
        sm = ScreenManager()
        
        # Tambahkan Layar
        sm.add_widget(AuthScreen(name='auth'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(TransactionScreen(name='transaction'))
        sm.add_widget(SavingsScreen(name='savings'))
        
        return sm

if __name__ == '__main__':
    FinanceManagerApp().run()
