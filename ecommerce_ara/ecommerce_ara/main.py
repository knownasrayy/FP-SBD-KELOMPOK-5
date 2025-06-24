# main.py
from fitur_sql import tampilkan_produk, tampilkan_laporan_transaksi, hitung_total_transaksi
from fitur_nosql import tampilkan_feedback

print("=== Daftar Produk ===")
tampilkan_produk()
print()

print("=== Feedback Produk ===")
tampilkan_feedback()
print()

print("=== Laporan Transaksi ===")
tampilkan_laporan_transaksi()
print()

print("=== Total Transaksi ID 1 ===")
hitung_total_transaksi(1)