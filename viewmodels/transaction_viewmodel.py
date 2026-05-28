import uuid
from models.database import insert_transaksi
from core.app_state import app_state

class TransactionViewModel:
    def __init__(self):
        # Dependencies bisa diinject di sini, seperti repository untuk DB
        pass

    def add_manual_transaction(self, nominal: float, kategori: str, tipe: str, keterangan: str, date: str, foto_struk: str = ""):
        """
        Logika untuk menyimpan transaksi manual ke database lokal
        """
        # Validasi anti-kosong
        if not nominal or nominal <= 0:
            return False, "Nominal tidak boleh kosong atau nol"
            
        id_transaksi = str(uuid.uuid4())
        
        if app_state.current_user:
            user_id = app_state.current_user['id_user']
        else:
            return False, "Sesi Anda telah berakhir, silakan login ulang."
        
        try:
            insert_transaksi(
                id_transaksi=id_transaksi,
                nominal=nominal,
                kategori=kategori,
                tipe=tipe,
                foto_struk=foto_struk,
                keterangan=keterangan,
                tanggal=date,
                id_user=user_id
            )
            return True, "Transaksi berhasil disimpan"
        except Exception as e:
            print(f"Error DB: {e}")
            return False, "Gagal menyimpan ke database"

    def process_receipt_ocr(self, image_path: str):
        """
        Meneruskan path gambar ke ocr_processor
        """
        from utils.ocr_processor import extract_total_from_receipt
        
        amount, confidence = extract_total_from_receipt(image_path)
        
        if amount is None or confidence < 0.3:
            return False, "Struk tidak terbaca jelas. Silakan input manual.", 0.0
            
        return True, "Nominal ditemukan", amount
