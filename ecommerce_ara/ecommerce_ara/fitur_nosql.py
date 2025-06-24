# fitur_nosql.py
from mongo_conn import connect_mongo

def tampilkan_feedback():
    db = connect_mongo()
    for doc in db.review.find():
        print(f"User {doc['id_user']} beri rating {doc['rating']} ke produk {doc['id_produk']}")
