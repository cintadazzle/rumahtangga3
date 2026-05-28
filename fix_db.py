import sqlite3
import random
import string

conn = sqlite3.connect('financemanager.db')
cursor = conn.cursor()

# Fix 1: Buat keluarga untuk yang id_keluarga sudah ada di user tapi tidak ada di tabel keluarga
cursor.execute('SELECT id_keluarga FROM user WHERE id_keluarga IS NOT NULL AND id_keluarga != "" GROUP BY id_keluarga')
rows = cursor.fetchall()
for row in rows:
    id_kel = row[0]
    cursor.execute('SELECT * FROM keluarga WHERE id_keluarga = ?', (id_kel,))
    if not cursor.fetchone():
        pin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        cursor.execute('INSERT INTO keluarga (id_keluarga, nama_keluarga, pin_keluarga) VALUES (?, ?, ?)', (id_kel, 'Keluarga', pin))
        print(f"Created keluarga {id_kel} with pin {pin}")

# Fix 2: Buat keluarga dan assign id_keluarga untuk user lama yang id_keluarga-nya masih kosong
cursor.execute("SELECT id_user, nama FROM user WHERE id_keluarga IS NULL OR id_keluarga = ''")
old_users = cursor.fetchall()
for ou in old_users:
    uid = ou[0]
    unm = ou[1]
    pin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    cursor.execute("INSERT OR IGNORE INTO keluarga (id_keluarga, nama_keluarga, pin_keluarga) VALUES (?, ?, ?)", (uid, f"Keluarga {unm}", pin))
    cursor.execute("UPDATE user SET id_keluarga = ? WHERE id_user = ?", (uid, uid))
    print(f"Migrated old user {uid} ({unm}) to their own keluarga")

conn.commit()
print("Done")
