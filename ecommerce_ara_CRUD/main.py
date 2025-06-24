from fitur_sql import (
    tampilkan_produk, tambah_produk, update_produk,
    hapus_produk, tampilkan_laporan_transaksi, hitung_total_transaksi
)
from fitur_nosql import tampilkan_feedback

def menu():
    while True:
        print("\n=== MENU UTAMA MERCHANDISE ARA 6.0 ===")
        print("1. Lihat Produk")
        print("2. Tambah Produk")
        print("3. update Produk")
        print("4. Hapus Produk")
        print("5. Lihat Review Produk")
        print("6. Laporan Transaksi")
        print("7. Hitung Total Transaksi")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            tampilkan_produk()
        elif pilihan == "2":
            tambah_produk()
        elif pilihan == "3":
            update_produk()
        elif pilihan == "4":
            hapus_produk()
        elif pilihan == "5":
            tampilkan_feedback()
        elif pilihan == "6":
            tampilkan_laporan_transaksi()
        elif pilihan == "7":
            id_trans = int(input("Masukkan ID transaksi: "))
            hitung_total_transaksi(id_trans)
        elif pilihan == "0":
            break
        else:
            print("Menu tidak valid.")

if __name__ == "__main__":
    menu()
