import sqlite3
import os
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = 'financemanager.db'
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Tabel Keluarga
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keluarga (
                id_keluarga TEXT PRIMARY KEY,
                nama_keluarga TEXT NOT NULL,
                pin_keluarga TEXT NOT NULL
            )
        ''')
        
        # Tabel User
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id_user TEXT PRIMARY KEY,
                nama TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                id_keluarga TEXT,
                FOREIGN KEY (id_keluarga) REFERENCES keluarga(id_keluarga)
            )
        ''')
        
        # Coba tambahkan kolom password jika tabel sudah terlanjur ada sebelumnya
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN password TEXT NOT NULL DEFAULT ''")
        except:
            pass
        
        # Tabel Transaksi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaksi (
                id_transaksi TEXT PRIMARY KEY,
                nominal REAL NOT NULL,
                kategori TEXT NOT NULL,
                tipe TEXT NOT NULL, -- 'pengeluaran' atau 'pemasukan'
                foto_struk TEXT,
                keterangan TEXT,
                tanggal TEXT NOT NULL,
                id_user TEXT,
                FOREIGN KEY (id_user) REFERENCES user(id_user)
            )
        ''')
        
        # Tabel Target Tabungan
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS target_tabungan (
                id_target TEXT PRIMARY KEY,
                nama_target TEXT NOT NULL,
                nominal_target REAL NOT NULL,
                deadline TEXT NOT NULL,
                deskripsi TEXT,
                id_keluarga TEXT,
                FOREIGN KEY (id_keluarga) REFERENCES keluarga(id_keluarga)
            )
        ''')
        
        # Tabel Setoran
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS setoran (
                id_setoran TEXT PRIMARY KEY,
                jumlah REAL NOT NULL,
                tanggal TEXT NOT NULL,
                catatan TEXT,
                id_target TEXT,
                FOREIGN KEY (id_target) REFERENCES target_tabungan(id_target)
            )
        ''')
        
        # Tabel Tagihan Tetap
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tagihan_tetap (
                id_tagihan TEXT PRIMARY KEY,
                nama TEXT NOT NULL,
                nominal REAL NOT NULL,
                tgl_jatuh_tempo TEXT NOT NULL,
                id_keluarga TEXT,
                FOREIGN KEY (id_keluarga) REFERENCES keluarga(id_keluarga)
            )
        ''')
        
        # Migrasi data: Untuk user lama yang belum punya id_keluarga, buatkan keluarga untuknya
        cursor.execute("SELECT id_user, nama FROM user WHERE id_keluarga IS NULL OR id_keluarga = ''")
        old_users = cursor.fetchall()
        import random
        import string
        for ou in old_users:
            uid = ou['id_user']
            unm = ou['nama']
            pin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            
            # Buat record keluarga baru
            cursor.execute(
                "INSERT OR IGNORE INTO keluarga (id_keluarga, nama_keluarga, pin_keluarga) VALUES (?, ?, ?)",
                (uid, f"Keluarga {unm}", pin)
            )
            # Update user dengan id_keluarga barunya
            cursor.execute(
                "UPDATE user SET id_keluarga = ? WHERE id_user = ?",
                (uid, uid)
            )

        conn.commit()

# --- CRUD Functions (Keluarga) ---
def create_keluarga(id_keluarga, nama_keluarga, pin_keluarga):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO keluarga (id_keluarga, nama_keluarga, pin_keluarga) VALUES (?, ?, ?)",
            (id_keluarga, nama_keluarga, pin_keluarga)
        )
        conn.commit()

def get_keluarga_by_pin(pin_keluarga):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM keluarga WHERE pin_keluarga = ?", (pin_keluarga,))
        return cursor.fetchone()

def get_keluarga_by_id(id_keluarga):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM keluarga WHERE id_keluarga = ?", (id_keluarga,))
        return cursor.fetchone()

# --- CRUD Functions Example (User) ---
def create_user(id_user, nama, email, password, role, id_keluarga):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user (id_user, nama, email, password, role, id_keluarga) VALUES (?, ?, ?, ?, ?, ?)",
            (id_user, nama, email, password, role, id_keluarga)
        )
        conn.commit()

def update_user_keluarga(id_user, id_keluarga):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE user SET id_keluarga = ?, role = 'Member' WHERE id_user = ?", (id_keluarga, id_user))
        conn.commit()

def get_user_by_email(email):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        return cursor.fetchone()

def get_users_by_keluarga(id_keluarga):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_user, nama, email, role FROM user WHERE id_keluarga = ?", (id_keluarga,))
        return [dict(row) for row in cursor.fetchall()]

# --- CRUD Functions (Transaksi) ---
def insert_transaksi(id_transaksi, nominal, kategori, tipe, foto_struk, keterangan, tanggal, id_user):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transaksi (id_transaksi, nominal, kategori, tipe, foto_struk, keterangan, tanggal, id_user) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (id_transaksi, nominal, kategori, tipe, foto_struk, keterangan, tanggal, id_user)
        )
        conn.commit()

def get_all_transaksi():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transaksi ORDER BY tanggal DESC")
        return [dict(row) for row in cursor.fetchall()]

def get_transaksi_by_user(id_user):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transaksi WHERE id_user = ? ORDER BY tanggal DESC", (id_user,))
        return [dict(row) for row in cursor.fetchall()]

def get_transaksi_by_keluarga(id_keluarga):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.* FROM transaksi t
            JOIN user u ON t.id_user = u.id_user
            WHERE u.id_keluarga = ?
            ORDER BY t.tanggal DESC
        ''', (id_keluarga,))
        return [dict(row) for row in cursor.fetchall()]

# --- CRUD Functions (Target Tabungan) ---
def insert_target_tabungan(id_target, nama_target, nominal_target, deadline, deskripsi, id_keluarga):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO target_tabungan (id_target, nama_target, nominal_target, deadline, deskripsi, id_keluarga) VALUES (?, ?, ?, ?, ?, ?)",
            (id_target, nama_target, nominal_target, deadline, deskripsi, id_keluarga)
        )
        conn.commit()

def get_all_target_tabungan():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM target_tabungan ORDER BY deadline ASC")
        return [dict(row) for row in cursor.fetchall()]

def get_target_tabungan_by_keluarga(id_keluarga):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM target_tabungan WHERE id_keluarga = ? ORDER BY deadline ASC", (id_keluarga,))
        return [dict(row) for row in cursor.fetchall()]

def delete_target_tabungan(id_target):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Delete related setoran first
        cursor.execute("DELETE FROM setoran WHERE id_target = ?", (id_target,))
        cursor.execute("DELETE FROM target_tabungan WHERE id_target = ?", (id_target,))
        conn.commit()

# --- CRUD Functions (Setoran) ---
def insert_setoran(id_setoran, jumlah, tanggal, catatan, id_target):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO setoran (id_setoran, jumlah, tanggal, catatan, id_target) VALUES (?, ?, ?, ?, ?)",
            (id_setoran, jumlah, tanggal, catatan, id_target)
        )
        conn.commit()

def get_total_setoran_by_target(id_target):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(jumlah) as total FROM setoran WHERE id_target = ?", (id_target,))
        result = cursor.fetchone()
        return result['total'] if result and result['total'] else 0.0

# (We will add more CRUD operations as needed by ViewModels)

if __name__ == '__main__':
    # Initialize DB for testing
    init_db()
    print("Database initialized successfully.")
