import calendar
from datetime import datetime

def calculate_jatah_harian(pemasukan: float, target_tabungan: float, tagihan_tetap: float, total_pengeluaran_saat_ini: float) -> float:
    """
    Rumus Utama Kalkulasi Jatah Harian:
    Jatah Harian = ((Pemasukan - Target Tabungan - Tagihan Tetap) - Total Pengeluaran Saat Ini) / Sisa Hari di Bulan Ini
    """
    now = datetime.now()
    _, last_day = calendar.monthrange(now.year, now.month)
    
    # +1 to include today, but let's assume we want days remaining including today
    sisa_hari = last_day - now.day + 1
    
    if sisa_hari <= 0:
        sisa_hari = 1 # Prevent division by zero, edge case for end of month calculation errors
        
    dana_tersedia = pemasukan - target_tabungan - tagihan_tetap
    sisa_dana = dana_tersedia - total_pengeluaran_saat_ini
    
    jatah_harian = sisa_dana / sisa_hari
    
    # Return 0 if negative to avoid suggesting they can spend negative amounts
    return max(0.0, jatah_harian)

def get_status_pengeluaran(pengeluaran_hari_ini: float, jatah_harian: float) -> str:
    """
    Status AMAN (Hijau): < 80% dari jatah
    Status PERINGATAN (Kuning): 80% - 100% dari jatah
    Status BAHAYA (Merah): > 100% dari jatah
    """
    if jatah_harian <= 0:
        return 'merah' if pengeluaran_hari_ini > 0 else 'hijau'
        
    persentase = pengeluaran_hari_ini / jatah_harian
    
    if persentase < 0.80:
        return 'hijau'
    elif persentase <= 1.0:
        return 'kuning'
    else:
        return 'merah'
