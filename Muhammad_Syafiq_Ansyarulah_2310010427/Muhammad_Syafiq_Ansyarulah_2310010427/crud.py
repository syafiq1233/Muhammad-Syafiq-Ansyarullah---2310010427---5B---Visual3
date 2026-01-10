import os
import mysql.connector

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors


class crud_app:
    """
    Struktur CRUD mengikuti contoh dosen:
    - tambahX, gantiX, kurangX, dataX, filterX, cetakX
    """

    def __init__(self):
        self.koneksi = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_2310010427",
        )

    def tambahClient(self, nama_client, email, no_hp, alamat):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "INSERT INTO client (nama_client, email, no_hp, alamat) VALUES (%s, %s, %s, %s)",
            (nama_client, email, no_hp, alamat),
        )
        self.koneksi.commit()
        aksi.close()

    def gantiClient(self, id_client, nama_client, email, no_hp, alamat):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "UPDATE client SET nama_client=%s, email=%s, no_hp=%s, alamat=%s WHERE id_client=%s",
            (nama_client, email, no_hp, alamat, id_client),
        )
        self.koneksi.commit()
        aksi.close()

    def kurangClient(self, id_client):
        aksi = self.koneksi.cursor()
        aksi.execute("DELETE FROM client WHERE id_client=%s", (id_client,))
        self.koneksi.commit()
        aksi.close()

    def dataClient(self):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute("SELECT * FROM client ORDER BY id_client ASC")
        return aksi.fetchall()

    def filterClient(self, cari):
        aksi = self.koneksi.cursor(dictionary=True)
        like = f"%{cari}%"
        aksi.execute(
            "SELECT * FROM client WHERE id_client LIKE %s OR nama_client LIKE %s OR email LIKE %s OR no_hp LIKE %s ORDER BY id_client ASC",
            (like, like, like, like),
        )
        return aksi.fetchall()

    def cetakClient(self, filename="Laporan Client.pdf"):
        aksi = self.koneksi.cursor()
        aksi.execute("SELECT id_client, nama_client, email, no_hp, alamat FROM client ORDER BY id_client ASC")
        data = aksi.fetchall()
        baris = [["ID", "Nama", "Email", "No HP", "Alamat"]] + [list(r) for r in data]
        self._cetak_pdf(filename, baris, landscape_mode=True)

    def tambahPaket(self, nama_paket, harga, deskripsi):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "INSERT INTO paket (nama_paket, harga, deskripsi) VALUES (%s, %s, %s)",
            (nama_paket, harga, deskripsi),
        )
        self.koneksi.commit()
        aksi.close()

    def gantiPaket(self, id_paket, nama_paket, harga, deskripsi):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "UPDATE paket SET nama_paket=%s, harga=%s, deskripsi=%s WHERE id_paket=%s",
            (nama_paket, harga, deskripsi, id_paket),
        )
        self.koneksi.commit()
        aksi.close()

    def kurangPaket(self, id_paket):
        aksi = self.koneksi.cursor()
        aksi.execute("DELETE FROM paket WHERE id_paket=%s", (id_paket,))
        self.koneksi.commit()
        aksi.close()

    def dataPaket(self):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute("SELECT * FROM paket ORDER BY id_paket ASC")
        return aksi.fetchall()

    def filterPaket(self, cari):
        aksi = self.koneksi.cursor(dictionary=True)
        like = f"%{cari}%"
        aksi.execute(
            "SELECT * FROM paket WHERE id_paket LIKE %s OR nama_paket LIKE %s ORDER BY id_paket ASC",
            (like, like),
        )
        return aksi.fetchall()

    def cetakPaket(self, filename="Laporan Paket.pdf"):
        aksi = self.koneksi.cursor()
        aksi.execute("SELECT id_paket, nama_paket, harga, deskripsi FROM paket ORDER BY id_paket ASC")
        data = aksi.fetchall()
        baris = [["ID", "Nama Paket", "Harga", "Deskripsi"]] + [list(r) for r in data]
        self._cetak_pdf(filename, baris, landscape_mode=True)

    def tambahKriteria(self, nama_kriteria, bobot, sifat):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "INSERT INTO kriteria (nama_kriteria, bobot, sifat) VALUES (%s, %s, %s)",
            (nama_kriteria, bobot, sifat),
        )
        self.koneksi.commit()
        aksi.close()

    def gantiKriteria(self, id_kriteria, nama_kriteria, bobot, sifat):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "UPDATE kriteria SET nama_kriteria=%s, bobot=%s, sifat=%s WHERE id_kriteria=%s",
            (nama_kriteria, bobot, sifat, id_kriteria),
        )
        self.koneksi.commit()
        aksi.close()

    def kurangKriteria(self, id_kriteria):
        aksi = self.koneksi.cursor()
        aksi.execute("DELETE FROM kriteria WHERE id_kriteria=%s", (id_kriteria,))
        self.koneksi.commit()
        aksi.close()

    def dataKriteria(self):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute("SELECT * FROM kriteria ORDER BY id_kriteria ASC")
        return aksi.fetchall()

    def filterKriteria(self, cari):
        aksi = self.koneksi.cursor(dictionary=True)
        like = f"%{cari}%"
        aksi.execute(
            "SELECT * FROM kriteria WHERE id_kriteria LIKE %s OR nama_kriteria LIKE %s OR sifat LIKE %s ORDER BY id_kriteria ASC",
            (like, like, like),
        )
        return aksi.fetchall()

    def cetakKriteria(self, filename="Laporan Kriteria.pdf"):
        aksi = self.koneksi.cursor()
        aksi.execute("SELECT id_kriteria, nama_kriteria, bobot, sifat FROM kriteria ORDER BY id_kriteria ASC")
        data = aksi.fetchall()
        baris = [["ID", "Nama Kriteria", "Bobot", "Sifat"]] + [list(r) for r in data]
        self._cetak_pdf(filename, baris, col_widths=[50, 240, 80, 80])

    def tambahPenilaian(self, id_client, id_paket, id_kriteria, nilai):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "INSERT INTO penilaian (id_client, id_paket, id_kriteria, nilai) VALUES (%s, %s, %s, %s)",
            (id_client, id_paket, id_kriteria, nilai),
        )
        self.koneksi.commit()
        aksi.close()

    def gantiPenilaian(self, id_penilaian, id_client, id_paket, id_kriteria, nilai):
        aksi = self.koneksi.cursor()
        aksi.execute(
            "UPDATE penilaian SET id_client=%s, id_paket=%s, id_kriteria=%s, nilai=%s WHERE id_penilaian=%s",
            (id_client, id_paket, id_kriteria, nilai, id_penilaian),
        )
        self.koneksi.commit()
        aksi.close()

    def kurangPenilaian(self, id_penilaian):
        aksi = self.koneksi.cursor()
        aksi.execute("DELETE FROM penilaian WHERE id_penilaian=%s", (id_penilaian,))
        self.koneksi.commit()
        aksi.close()

    def dataPenilaian(self):
        aksi = self.koneksi.cursor(dictionary=True)
        aksi.execute(
            """
            SELECT
              p.id_penilaian,
              p.id_client, c.nama_client,
              p.id_paket, pk.nama_paket,
              p.id_kriteria, k.nama_kriteria,
              p.nilai
            FROM penilaian p
            LEFT JOIN client c ON p.id_client = c.id_client
            LEFT JOIN paket pk ON p.id_paket = pk.id_paket
            LEFT JOIN kriteria k ON p.id_kriteria = k.id_kriteria
            ORDER BY p.id_penilaian ASC
            """
        )
        return aksi.fetchall()

    def filterPenilaian(self, cari):
        aksi = self.koneksi.cursor(dictionary=True)
        like = f"%{cari}%"
        aksi.execute(
            """
            SELECT
              p.id_penilaian,
              p.id_client, c.nama_client,
              p.id_paket, pk.nama_paket,
              p.id_kriteria, k.nama_kriteria,
              p.nilai
            FROM penilaian p
            LEFT JOIN client c ON p.id_client = c.id_client
            LEFT JOIN paket pk ON p.id_paket = pk.id_paket
            LEFT JOIN kriteria k ON p.id_kriteria = k.id_kriteria
            WHERE
              p.id_penilaian LIKE %s OR
              c.nama_client LIKE %s OR
              pk.nama_paket LIKE %s OR
              k.nama_kriteria LIKE %s
            ORDER BY p.id_penilaian ASC
            """,
            (like, like, like, like),
        )
        return aksi.fetchall()

    def cetakPenilaian(self, filename="Laporan Penilaian.pdf"):
        aksi = self.koneksi.cursor()
        aksi.execute(
            """
            SELECT
              p.id_penilaian,
              c.nama_client,
              pk.nama_paket,
              k.nama_kriteria,
              p.nilai
            FROM penilaian p
            LEFT JOIN client c ON p.id_client = c.id_client
            LEFT JOIN paket pk ON p.id_paket = pk.id_paket
            LEFT JOIN kriteria k ON p.id_kriteria = k.id_kriteria
            ORDER BY p.id_penilaian ASC
            """
        )
        data = aksi.fetchall()
        baris = [["ID", "Client", "Paket", "Kriteria", "Nilai"]] + [list(r) for r in data]
        self._cetak_pdf(filename, baris, landscape_mode=True)

    def _cetak_pdf(self, filename, baris_data, col_widths=None, landscape_mode=False):
        path = os.path.join(os.getcwd(), filename)
        pagesize = landscape(A4) if landscape_mode else A4
        pdf = SimpleDocTemplate(path, pagesize=pagesize)
        tabel = Table(baris_data, colWidths=col_widths)
        tabel.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        pdf.build([tabel])
