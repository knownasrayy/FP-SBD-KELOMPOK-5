

CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

CREATE TABLE user (
    id_user INT PRIMARY KEY,
    nama_user VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    alamat_user TEXT NOT NULL,
    no_telepon VARCHAR(15) UNIQUE NOT NULL,
    role ENUM('Pembeli', 'Admin') NOT NULL
);

CREATE TABLE kategori (
    id_kategori INT PRIMARY KEY,
    nama_kategori VARCHAR(100) NOT NULL
);

CREATE TABLE produk (
    id_produk INT PRIMARY KEY,
    id_kategori INT,
    nama_produk VARCHAR(100) NOT NULL,
    harga INT NOT NULL,
    stok INT,
    deskripsi TEXT,
    FOREIGN KEY(id_kategori) REFERENCES kategori(id_kategori)
);

CREATE TABLE promosi (
    id_promosi INT PRIMARY KEY,
    nama_promosi VARCHAR(100) NOT NULL,
    diskon DECIMAL(5,2) NOT NULL,
    deskripsi TEXT,
    tanggal_mulai DATE NOT NULL,
    tanggal_selesai DATE NOT NULL,
    status_promosi ENUM ('Aktif', 'Berakhir') DEFAULT 'Aktif'
);

CREATE TABLE promosi_produk (
    id_produk INT,
    id_promosi INT,
    PRIMARY KEY (id_produk, id_promosi),
    FOREIGN KEY (id_produk) REFERENCES produk(id_produk),
    FOREIGN KEY (id_promosi) REFERENCES promosi(id_promosi)
);

CREATE TABLE transaksi (
    id_transaksi INT PRIMARY KEY,
    id_user INT NOT NULL,
    tanggal_transaksi DATETIME,
    total INT NOT NULL,
    FOREIGN KEY (id_user) REFERENCES user(id_user)
);

CREATE TABLE transaksi_detail (
    id_detail INT PRIMARY KEY,
    id_transaksi INT NOT NULL,
    id_produk INT NOT NULL,
    jumlah INT NOT NULL,
    subtotal INT NOT NULL,
    FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi),
    FOREIGN KEY (id_produk) REFERENCES produk(id_produk)
);

CREATE TABLE pembayaran (
    id_pembayaran INT PRIMARY KEY,
    id_transaksi INT NOT NULL,
    metode_pembayaran ENUM('QRIS', 'Debit','Tunai') DEFAULT 'Tunai',
    status_pembayaran ENUM('Gagal', 'Pending', 'Selesai') DEFAULT 'Pending',
    tanggal_bayar DATETIME,
    FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi)
);

CREATE TABLE tracking (
    id_tracking INT PRIMARY KEY,
    id_transaksi INT NOT NULL,
    alamat_user TEXT NOT NULL,
    status ENUM('Diproses', 'Dikirim', 'Selesai', 'Gagal') DEFAULT 'Diproses',
    waktu_realtime DATETIME,
    FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi)
);


-- =====================================
-- INSERT DATA
-- =====================================

INSERT INTO user VALUES
(1, 'Tiara fattimah', 'titifafa@gmail.com', 'joderenak1', 'Jalan wisma permai II no 27, Mulyosari', '08123456789', 'Pembeli'),
(2, 'Erlinda Annisa', 'erlin99@gmail.com', 'ilovekampis', 'Jalan Klampis Aji Tengah no 33, Klampis', '0811223344', 'Pembeli'),
(3, 'Aslam', 'salamlam@gmail.com', 'tsunderekelaskakap', 'Blok J no 10, Keputih', '08198765432', 'Pembeli'),
(4, 'Rayhan Agnan', 'rehanheker@gmail.com', 'sepuhcoding01', 'KTT Gg. 1 no 16, Keputih', '0882638432', 'Pembeli'),
(5, 'Maritza Adelia', 'adeljkt48@gmail.com', 'fansnyanunung22', 'Bumi Marina Emas Gg 1 no 30, Keputih', '08123445389', 'Pembeli'),
(6, 'ARA ITS', 'araits@gmail.com', 'araits6', 'Jalan Raya ITS No 1', '08987656789', 'Admin');

INSERT INTO kategori VALUES
(1, 'Sticker'),
(2, 'Keychain'),
(3, 'Totebag'),
(4, 'Topi'),
(5, 'Lanyard'),
(6, 'Strap'),
(7, 'T-Shirt');

INSERT INTO produk VALUES
(1, 1, 'Sticker Stiker Agents', 12000, 150, 'Sticker tema Agents'),
(2, 2, 'Keychain CTF', 12000, 80, 'Keychain CTF edition'),
(3, 2, 'Keychain Cysec', 12000, 60, 'Keychain CYSEC edition'),
(4, 2, 'Keychain Console', 12000, 100, 'Keychain Console edition'),
(5, 3, 'Totebag A Renewal Agents', 45000, 50, 'Totebag Renewal Agents edition'),
(6, 3, 'Totebag The Future', 45000, 70, 'Totebag Future edition'),
(7, 4, 'Topi Future Fusion', 45000, 40, 'Topi Future Fusion'),
(8, 5, 'Lanyard Colorful Future', 12000, 90, 'Lanyard Colorful Future edition'),
(9, 6, 'Strap Arlo Fusion', 12000, 85, 'Strap Arlo Fusion edition'),
(10, 7, 'T-shirt Glow in the dark', 90000, 30, 'Kaos Glow in the Dark'),
(11, 7, 'T-shirt The Agents', 90000, 25, 'Kaos The Agents Edition');

INSERT INTO promosi VALUES
(1, 'GAJIANTIME', 15.00, 'Diskon spesial akhir bulan khusus pembelian T-Shirt', '2025-06-20', '2025-06-30', 'Aktif');

INSERT INTO promosi_produk VALUES
(5, 1),
(6, 1);

INSERT INTO transaksi VALUES
(1, 1, '2025-05-08 10:00:00', 240000),
(2, 2, '2025-06-09 11:30:00', 450000),
(3, 3, '2025-06-09 12:00:00', 69000),
(4, 4, '2025-06-01 13:00:00', 90000);

INSERT INTO transaksi_detail VALUES
(1, 1, 1, 1, 12000),
(2, 1, 2, 1, 12000),
(3, 2, 5, 1, 45000),
(4, 3, 2, 2, 24000),
(5, 3, 6, 1, 45000),
(6, 4, 10, 1, 90000);

INSERT INTO pembayaran VALUES
(1, 1, 'QRIS', 'Selesai', '2025-05-08 10:00:00'),
(2, 2, 'Debit', 'Selesai', '2025-06-09 11:30:00'),
(3, 3, 'QRIS', 'Selesai', '2025-06-09 12:00:00'),
(4, 4, 'Tunai', 'Gagal', '2025-06-01 13:00:00');

INSERT INTO tracking VALUES
(1, 1, 'Jalan wisma permai II no 27, Mulyosari', 'Selesai', '2025-05-15 12:00:00'),
(2, 2, 'Jalan Klampis Aji Tengah no 33, Klampis', 'Diproses', '2025-06-13 12:30:00'),
(3, 3, 'Blok I no 10, Keputih', 'Dikirim', '2025-06-13 13:00:00'),
(4, 4, 'KTT Gg. 1 no 16, Keputih', 'Gagal', '2025-06-03 14:00:00');



DELIMITER $$
CREATE FUNCTION hitung_total_transaksi(id_trans INT) RETURNS DOUBLE
DETERMINISTIC
BEGIN
    DECLARE total DOUBLE;
    SELECT SUM(subtotal) INTO total
    FROM transaksi_detail
    WHERE id_transaksi = id_trans;
    RETURN total;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER kurangi_stok
AFTER INSERT ON transaksi_detail
FOR EACH ROW
BEGIN
    UPDATE produk
    SET stok = stok - NEW.jumlah
    WHERE id_produk = NEW.id_produk;
END $$
DELIMITER ;

-- =====================================
-- VIEW
-- =====================================

CREATE VIEW v_laporan_transaksi AS
SELECT t.id_transaksi, u.nama_user, t.tanggal_transaksi, t.total,
       p.nama_produk, td.jumlah, td.subtotal,
       b.metode_pembayaran, b.status_pembayaran,
       tr.status AS status_pengiriman
FROM transaksi t
JOIN user u ON t.id_user = u.id_user
JOIN transaksi_detail td ON t.id_transaksi = td.id_transaksi
JOIN produk p ON td.id_produk = p.id_produk
JOIN pembayaran b ON t.id_transaksi = b.id_transaksi
JOIN tracking tr ON t.id_transaksi = tr.id_transaksi;
