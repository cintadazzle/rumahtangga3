import uuid
from datetime import datetime
from dateutil import parser
from models.database import insert_target_tabungan, get_target_tabungan_by_keluarga, delete_target_tabungan, insert_setoran, get_total_setoran_by_target
from core.app_state import app_state

class SavingsViewModel:
    def __init__(self):
        pass

    def _parse_deadline_date(self, deadline_raw: str):
        if not deadline_raw:
            return None
        deadline_raw = deadline_raw.strip()
        # Coba format standar dan format umum Indonesia
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(deadline_raw, fmt).date()
            except ValueError:
                pass
        # Fallback ke dateutil jika format tidak standar
        try:
            return parser.parse(deadline_raw, dayfirst=True).date()
        except Exception:
            return None

    def get_all_targets(self):
        if not app_state.current_user:
            return []
            
        id_keluarga = app_state.current_user.get('id_keluarga', app_state.current_user['id_user'])
        targets = get_target_tabungan_by_keluarga(id_keluarga)
        result = []
        for t in targets:
            terkumpul = get_total_setoran_by_target(t['id_target'])
            sisa = max(0, t['nominal_target'] - terkumpul)
            
            deadline_date = self._parse_deadline_date(t['deadline'])
            if deadline_date:
                delta = (deadline_date - datetime.now().date()).days
                sisa_hari = max(0, delta)
            else:
                sisa_hari = 0
                print(f"Error parsing date {t['deadline']}")
                
            result.append({
                "id_target": t['id_target'],
                "nama": t['nama_target'],
                "target": t['nominal_target'],
                "terkumpul": terkumpul,
                "sisa": sisa,
                "sisa_hari": sisa_hari,
                "deadline": t['deadline']
            })
        return result

    def add_target(self, nama, nominal, deadline):
        if not nama or nominal <= 0 or not deadline:
            return False, "Data target tidak lengkap"
            
        deadline_date = self._parse_deadline_date(deadline)
        if not deadline_date:
            return False, "Format tanggal salah. Gunakan YYYY-MM-DD atau DD-MM-YYYY"

        deadline_str = deadline_date.strftime("%Y-%m-%d")
        id_target = str(uuid.uuid4())
        
        if not app_state.current_user:
            return False, "Sesi berakhir. Login ulang."
            
        id_keluarga = app_state.current_user.get('id_keluarga', app_state.current_user['id_user'])
        
        try:
            insert_target_tabungan(id_target, nama, nominal, deadline_str, "", id_keluarga)
            return True, "Target berhasil ditambahkan"
        except Exception as e:
            return False, str(e)

    def delete_target(self, id_target):
        try:
            delete_target_tabungan(id_target)
            return True, "Target berhasil dihapus"
        except Exception as e:
            return False, str(e)

    def add_deposit(self, id_target, nominal: float, catatan: str):
        if not nominal or nominal <= 0:
            return False, "Nominal tidak valid"
        
        id_setoran = str(uuid.uuid4())
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            insert_setoran(id_setoran, nominal, date_now, catatan, id_target)
            return True, "Setoran berhasil dicatat"
        except Exception as e:
            return False, str(e)
