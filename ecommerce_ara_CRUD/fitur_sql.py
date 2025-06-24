from mysql_conn import connect_mysql
from datetime import datetime

def tampilkan_produk():
    db = connect_mysql()
    cursor = db.cursor()
    cursor.execute("SELECT id_produk, nama_produk, harga, stok, deskripsi FROM produk")
    data = cursor.fetchall()

    print("\n=== DAFTAR PRODUK ===")
    print(f"{'ID':<4} {'Nama Produk':<30} {'Harga':<10} {'Stok':<6} Deskripsi")
    print("-" * 80)

    for row in data:
        id_produk = row[0]
        nama = row[1][:28] + "..." if len(row[1]) > 28 else row[1]
        harga = f"Rp{int(row[2]):,}".replace(',', '.')
        stok = row[3]
        deskripsi = row[4][:40] + "..." if len(row[4]) > 40 else row[4]
        print(f"{id_produk:<4} {nama:<30} {harga:<10} {stok:<6} {deskripsi}")

    cursor.close()
    db.close()

def tambah_produk():
    db = connect_mysql()
    cursor = db.cursor()

    cursor.execute("SELECT id_kategori, nama_kategori FROM kategori")
    kategori_list = cursor.fetchall()

    print("\n Daftar Kategori:")
    for k in kategori_list:
        print(f"{k[0]}. {k[1]}")

    while True:
        try:
            id_kategori = int(input("Masukkan ID kategori produk: "))
            cursor.execute("SELECT COUNT(*) FROM kategori WHERE id_kategori = %s", (id_kategori,))
            if cursor.fetchone()[0] > 0:
                break
            else:
                print("ID kategori tidak ditemukan. Coba lagi.")
        except ValueError:
            print("Masukkan angka yang valid untuk ID kategori.")

    nama = input("Nama produk: ")
    harga = int(input("Harga: "))
    stok_input = input("Stok (kosongkan untuk 0): ")
    deskripsi_input = input("Deskripsi (kosongkan untuk default): ")

    stok = int(stok_input) if stok_input.strip() else 0
    deskripsi = deskripsi_input.strip() if deskripsi_input.strip() else "Tidak ada deskripsi"

    cursor.execute("""
        INSERT INTO produk (id_kategori, nama_produk, harga, stok, deskripsi)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_kategori, nama, harga, stok, deskripsi))
    
    db.commit()
    print("Produk berhasil ditambahkan.")

    cursor.close()
    db.close()

def update_produk():
    db = connect_mysql()
    cursor = db.cursor()

    id_produk = input("ID produk yang ingin diupdate: ")
    cursor.execute("SELECT * FROM produk WHERE id_produk = %s", (id_produk,))
    if not cursor.fetchone():
        print("Produk tidak ditemukan.")
        return

    nama = input("Nama baru (kosongkan jika tidak diubah): ")
    harga = input("Harga baru (kosongkan jika tidak diubah): ")
    stok = input("Stok baru (kosongkan jika tidak diubah): ")
    deskripsi = input("Deskripsi baru (kosongkan jika tidak diubah): ")

    fields = []
    values = []

    if nama:
        fields.append("nama_produk = %s")
        values.append(nama)
    if harga:
        fields.append("harga = %s")
        values.append(int(harga))
    if stok:
        fields.append("stok = %s")
        values.append(int(stok))
    if deskripsi:
        fields.append("deskripsi = %s")
        values.append(deskripsi)

    if fields:
        query = f"UPDATE produk SET {', '.join(fields)} WHERE id_produk = %s"
        values.append(id_produk)
        cursor.execute(query, tuple(values))
        db.commit()
        print("Produk berhasil diupdate.")
    else:
        print("❕ Tidak ada data yang diubah.")

    cursor.close()
    db.close()

def hapus_produk():
    db = connect_mysql()
    cursor = db.cursor()

    id_produk = input("ID produk yang ingin dihapus: ")
    cursor.execute("SELECT * FROM produk WHERE id_produk = %s", (id_produk,))
    if not cursor.fetchone():
        print("Produk tidak ditemukan.")
        return

    konfirmasi = input(f"Yakin ingin menghapus produk ID {id_produk}? (y/n): ")
    if konfirmasi.lower() == 'y':
        cursor.execute("DELETE FROM produk WHERE id_produk = %s", (id_produk,))
        db.commit()
        print("Produk berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")

    cursor.close()
    db.close()

def tampilkan_laporan_transaksi():
    db = connect_mysql()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM v_laporan_transaksi")
    rows = cursor.fetchall()

    transaksi_dict = {}
    for row in rows:
        id_trans = row[0]
        nama_user = row[1]
        nama_produk = row[4]
        qty = row[5]
        subtotal = row[6]
        metode = row[7]
        status_bayar = row[8]
        status_kirim = row[9]

        if id_trans not in transaksi_dict:
            transaksi_dict[id_trans] = {
                "nama_user": nama_user,
                "metode": metode,
                "status_bayar": status_bayar,
                "status_kirim": status_kirim,
                "produk": []
            }
        transaksi_dict[id_trans]["produk"].append((nama_produk, qty, subtotal))

    print("\n=== LAPORAN TRANSAKSI ===")
    for id_trans, data in transaksi_dict.items():
        print(f"\n Transaksi #{id_trans} | Pelanggan: {data['nama_user']} | "
              f"Pembayaran: {data['metode']} ({data['status_bayar']}) | "
              f"Status Kirim: {data['status_kirim']}")
        for nama_produk, qty, subtotal in data["produk"]:
            subtotal_str = f"Rp{int(subtotal):,}".replace(",", ".")
            print(f"   - {nama_produk} x{qty} = {subtotal_str}")

    cursor.close()
    db.close()
def ambil_diskon_promosi(cursor, id_transaksi, subtotal):
    hari_ini = datetime.today().strftime('%Y-%m-%d')

    # Ambil semua id_produk dalam transaksi
    cursor.execute("""
        SELECT id_produk FROM transaksi_detail
        WHERE id_transaksi = %s
    """, (id_transaksi,))
    id_produk_list = [row[0] for row in cursor.fetchall()]

    if not id_produk_list:
        return 0, None  # Tidak ada produk dalam transaksi

    placeholders = ",".join(["%s"] * len(id_produk_list))

    # Ambil promosi yang masih aktif dan berlaku ke produk dalam transaksi
    cursor.execute(f"""
        SELECT p.nama_promosi, p.diskon
        FROM promosi p
        JOIN promosi_produk pp ON p.id_promosi = pp.id_promosi
        WHERE p.status_promosi = 'Aktif'
        AND p.tanggal_mulai <= %s AND p.tanggal_selesai >= %s
        AND pp.id_produk IN ({placeholders})
    """, [hari_ini, hari_ini] + id_produk_list)

    promos = cursor.fetchall()

    if not promos:
        return 0, None  # Tidak ada promosi yang cocok

    # Ambil promosi dengan diskon tertinggi
    nama_promosi_tertinggi = None
    diskon_tertinggi = 0
    for nama, persen in promos:
        if persen > diskon_tertinggi:
            diskon_tertinggi = persen
            nama_promosi_tertinggi = nama

    total_diskon = int(subtotal * (diskon_tertinggi / 100))
    return total_diskon, nama_promosi_tertinggi


def hitung_total_transaksi(id_trans):
    db = connect_mysql()
    cursor = db.cursor()

    cursor.execute("SELECT status_kirim FROM transaksi WHERE id_transaksi = %s", (id_trans,))
    result = cursor.fetchone()

    if not result:
        print("Transaksi tidak ditemukan.")
        return

    status_kirim = result[0]
    if status_kirim.lower() == "gagal":
        print(f"\nTransaksi #{id_trans} berstatus GAGAL. Tidak perlu menghitung total.")
        return

    cursor.execute("SELECT hitung_total_transaksi(%s)", (id_trans,))
    subtotal_result = cursor.fetchone()

    if subtotal_result and subtotal_result[0] is not None:
        subtotal = subtotal_result[0]
        ongkir = 10000
        diskon, nama_promo = ambil_diskon_promosi(cursor, id_trans, subtotal)
        total_bayar = subtotal + ongkir - diskon

        print(f"\nTotal Transaksi #{id_trans}")
        print("-" * 30)
        print(f"Subtotal produk     : Rp{subtotal:,}".replace(",", "."))
        print(f"Ongkir              : Rp{ongkir:,}".replace(",", "."))
        if nama_promo:
            print(f"Diskon ({nama_promo}) : Rp{diskon:,}".replace(",", "."))
        else:
            print(f"Diskon              : Rp{diskon:,}".replace(",", "."))
        print("-" * 30)
        print(f"Total Bayar         : Rp{total_bayar:,}".replace(",", "."))
    else:
        print("Transaksi tidak memiliki produk.")

    cursor.close()
    db.close()
