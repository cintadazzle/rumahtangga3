import re
import uuid
import random
import string
from models.database import create_user, get_user_by_email, create_keluarga, get_keluarga_by_pin
from core.app_state import app_state

class AuthViewModel:
    def __init__(self):
        pass

    def login(self, email, password):
        if not email or not password:
            return False, "Email dan Password tidak boleh kosong"
            
        try:
            user = get_user_by_email(email)
            if not user:
                return False, "Email tidak terdaftar"
                
            if user['password'] != password:
                return False, "Password salah"
                
            # Set state global
            app_state.set_user(dict(user))
            return True, "Login berhasil"
            
        except Exception as e:
            print(f"Login error: {e}")
            return False, "Terjadi kesalahan sistem"

    def register(self, nama, email, password, confirm_password, kode_keluarga=""):
        if not nama or not email or not password or not confirm_password:
            return False, "Semua kolom utama harus diisi"
            
        # Validasi Email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Format email tidak valid"
            
        # Validasi Password
        if len(password) < 6:
            return False, "Password minimal 6 karakter"
            
        if password != confirm_password:
            return False, "Konfirmasi password tidak cocok"
            
        try:
            existing = get_user_by_email(email)
            if existing:
                return False, "Email sudah terdaftar"
                
            id_user = str(uuid.uuid4())
            role = "Parent"
            
            if kode_keluarga:
                # Coba gabung ke keluarga yang ada
                keluarga = get_keluarga_by_pin(kode_keluarga.strip().upper())
                if not keluarga:
                    return False, "Kode Keluarga tidak ditemukan"
                id_keluarga = keluarga['id_keluarga']
                role = "Member"
            else:
                # Buat keluarga baru
                id_keluarga = id_user
                pin_keluarga = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                create_keluarga(id_keluarga, f"Keluarga {nama}", pin_keluarga)
            
            create_user(id_user, nama, email, password, role, id_keluarga)
            return True, "Registrasi berhasil. Silakan login."
            
        except Exception as e:
            print(f"Register error: {e}")
            return False, "Gagal mendaftar ke sistem"
