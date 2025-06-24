from mysql_conn import connect_mysql

def tampilkan_produk():
    db = connect_mysql()
    cursor = db.cursor()
    cursor.execute("SELECT nama_produk, harga FROM produk")
    for row in cursor.fetchall():
        print(f"{row[0]} - Rp{int(row[1])}")

def tampilkan_laporan_transaksi():
    db = connect_mysql()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM v_laporan_transaksi")
    for row in cursor.fetchall():
        print(f"Transaksi #{row[0]} - {row[1]} beli {row[4]} x{row[5]} = Rp{int(row[6])}")
        print(f"  Bayar via {row[7]} ({row[8]}), Status Kirim: {row[9]}")

def hitung_total_transaksi(id_trans):
    db = connect_mysql()
    cursor = db.cursor()
    cursor.execute("SELECT hitung_total_transaksi(%s)", (id_trans,))
    total = cursor.fetchone()[0]
    print(f"Total transaksi #{id_trans}: Rp{int(total)}")
