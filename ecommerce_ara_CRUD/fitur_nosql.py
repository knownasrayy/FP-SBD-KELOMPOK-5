from mongo_conn import connect_mongo

def tampilkan_feedback():
    db = connect_mongo()
    feedback_list = list(db.review.find())

    if not feedback_list:
        print("Belum ada feedback yang tersedia.")
        return

    print("\n=== DAFTAR ULASAN PRODUK ===")
    print("-" * 80)

    for doc in feedback_list:
        id_review = doc.get('id_review', '-')
        id_user = doc.get('id_user', '-')
        username = doc.get('username', 'user')
        tanggal = doc.get('tanggal', '-')
        id_produk = doc.get('id_produk', '-')
        nama_produk = doc.get('nama_produk', '(nama tidak tersedia)')
        variasi = doc.get('variasi_produk', '-')
        rating_num = int(doc.get('rating', 0))
        rating_bintang = "★" * rating_num + "☆" * (5 - rating_num)
        kondisi = doc.get('kondisi', '-')
        fungsi = doc.get('fungsi', '-')
        komentar = doc.get('deskripsi_review', '(tidak ada komentar)')

        print(f"Username     : {username} (user ID: {id_user})")
        print(f"Tanggal      : {tanggal}")
        print(f"Produk       : {nama_produk} (ID: {id_produk})")
        print(f"Varian       : {variasi}")
        print(f"Rating       : {rating_bintang}")
        print(f"Kondisi      : {kondisi}")
        print(f"Fungsi       : {fungsi}")
        print(f"Komentar     : {komentar}")
        print("-" * 80)
