from models.database import get_transaksi_by_keluarga, get_keluarga_by_id, get_keluarga_by_pin, update_user_keluarga, get_users_by_keluarga
from utils.budget_calculator import calculate_jatah_harian, get_status_pengeluaran
from core.app_state import app_state

class DashboardViewModel:
    def __init__(self):
        pass

    def get_dashboard_data(self):
        pin_keluarga = "-"
        if app_state.current_user:
            user_id = app_state.current_user['id_user']
            id_keluarga = app_state.current_user.get('id_keluarga', user_id)
            
            # Ambil PIN
            keluarga_data = get_keluarga_by_id(id_keluarga)
            if keluarga_data:
                pin_keluarga = keluarga_data['pin_keluarga']
                
            # Filter berdasarkan id_keluarga (karena satu keluarga share saldo)
            transaksi_list = get_transaksi_by_keluarga(id_keluarga)
            anggota_list = get_users_by_keluarga(id_keluarga)
        else:
            transaksi_list = []
            anggota_list = []
        
        total_pemasukan = 0.0
        total_pengeluaran = 0.0
        
        # Hitung saldo
        for t in transaksi_list:
            if t['tipe'] == 'pemasukan':
                total_pemasukan += t['nominal']
            elif t['tipe'] == 'pengeluaran':
                total_pengeluaran += t['nominal']
                
        saldo = total_pemasukan - total_pengeluaran
        
        # Panggil kalkulator jatah harian (Asumsi target tabungan = 0 dan tagihan tetap = 0 untuk mock)
        jatah_harian = calculate_jatah_harian(total_pemasukan, 0, 0, total_pengeluaran)
        
        # Hitung pengeluaran hari ini (Mock simple, asumsikan semua pengeluaran adalah hari ini untuk sementara)
        # Idealnya kita filter berdasarkan tanggal hari ini
        status_warna = get_status_pengeluaran(total_pengeluaran, jatah_harian)
        
        return {
            "saldo": saldo,
            "jatah_harian": jatah_harian,
            "status_warna": status_warna,
            "recent_transactions": transaksi_list[:5], # Ambil 5 terakhir
            "pin_keluarga": pin_keluarga,
            "total_pemasukan": total_pemasukan,
            "total_pengeluaran": total_pengeluaran,
            "anggota_keluarga": anggota_list
        }

    def join_keluarga(self, pin_keluarga):
        if not app_state.current_user:
            return False, "Sesi berakhir. Silakan login ulang."
            
        keluarga = get_keluarga_by_pin(pin_keluarga.strip().upper())
        if not keluarga:
            return False, "Kode tidak ditemukan."
            
        id_keluarga = keluarga['id_keluarga']
        id_user = app_state.current_user['id_user']
        
        try:
            update_user_keluarga(id_user, id_keluarga)
            # Update state agar langsung terasa efeknya
            app_state.current_user['id_keluarga'] = id_keluarga
            app_state.current_user['role'] = 'Member'
            return True, f"Berhasil bergabung dengan {keluarga['nama_keluarga']}"
        except Exception as e:
            return False, f"Terjadi kesalahan: {e}"
