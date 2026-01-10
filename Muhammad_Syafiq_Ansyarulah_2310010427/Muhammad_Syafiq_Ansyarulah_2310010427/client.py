# This Python file uses the following encoding: utf-8
import os

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox

from crud import crud_app


def ui_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)


class form_client(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        filenya = QFile(ui_path("client.ui"))
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formclient = muatfile.load(filenya, self)
        filenya.close()

        self.setWindowTitle(self.formclient.windowTitle())
        self.resize(self.formclient.size())

        self.aksi = crud_app()
        self._cache_rows = []

        self.formclient.BtnSimpan.clicked.connect(self.simpan)
        self.formclient.BtnUbah.clicked.connect(self.ubah)
        self.formclient.BtnHapus.clicked.connect(self.hapus)
        self.formclient.BtnBersih.clicked.connect(self.bersih)
        self.formclient.lineCari.textChanged.connect(self.cari)
        self.formclient.btnCetak.clicked.connect(self.cetak)
        self.formclient.tblClient.cellClicked.connect(self.pilih_baris)

        self.tampil()

    def bersih(self):
        self.formclient.EditId.clear()
        self.formclient.EditNama.clear()
        self.formclient.EditEmail.clear()
        self.formclient.EditNoHP.clear()
        self.formclient.EditAlamat.clear()
        self.formclient.EditNama.setFocus()

    def validasi(self, untuk_update=False) -> bool:
        if untuk_update and not self.formclient.EditId.text().strip():
            QMessageBox.information(self, "Informasi", "Pilih data dulu (klik tabel) untuk diubah/dihapus.")
            return False
        if not self.formclient.EditNama.text().strip():
            QMessageBox.information(self, "Informasi", "Nama Client belum diisi.")
            self.formclient.EditNama.setFocus()
            return False
        return True

    def simpan(self):
        if not self.validasi(False):
            return
        try:
            self.aksi.tambahClient(
                self.formclient.EditNama.text().strip(),
                self.formclient.EditEmail.text().strip() or None,
                self.formclient.EditNoHP.text().strip() or None,
                self.formclient.EditAlamat.toPlainText().strip() or None,
            )
            self.tampil()
            self.bersih()
            QMessageBox.information(self, "Informasi", "Data berhasil disimpan.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal simpan:\n{e}")

    def ubah(self):
        if not self.validasi(True):
            return
        try:
            self.aksi.gantiClient(
                int(self.formclient.EditId.text()),
                self.formclient.EditNama.text().strip(),
                self.formclient.EditEmail.text().strip() or None,
                self.formclient.EditNoHP.text().strip() or None,
                self.formclient.EditAlamat.toPlainText().strip() or None,
            )
            self.tampil()
            QMessageBox.information(self, "Informasi", "Data berhasil diubah.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal ubah:\n{e}")

    def hapus(self):
        if not self.formclient.EditId.text().strip():
            QMessageBox.information(self, "Informasi", "Pilih data dulu (klik tabel) untuk dihapus.")
            return
        pesan = QMessageBox.information(
            self, "Informasi", "Apakah yakin menghapus data ini?", QMessageBox.Yes | QMessageBox.No
        )
        if pesan != QMessageBox.Yes:
            return
        try:
            self.aksi.kurangClient(int(self.formclient.EditId.text()))
            self.tampil()
            self.bersih()
            QMessageBox.information(self, "Informasi", "Data berhasil dihapus.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal hapus:\n{e}")

    def tampil(self):
        self.formclient.tblClient.setRowCount(0)
        self._cache_rows = self.aksi.dataClient()
        for i, r in enumerate(self._cache_rows):
            self.formclient.tblClient.insertRow(i)
            self.formclient.tblClient.setItem(i, 0, QTableWidgetItem(str(r["id_client"])))
            self.formclient.tblClient.setItem(i, 1, QTableWidgetItem(str(r["nama_client"])))
            self.formclient.tblClient.setItem(i, 2, QTableWidgetItem(str(r.get("email") or "")))
            self.formclient.tblClient.setItem(i, 3, QTableWidgetItem(str(r.get("no_hp") or "")))
            self.formclient.tblClient.setItem(i, 4, QTableWidgetItem(str(r.get("alamat") or "")))
        self.formclient.tblClient.resizeColumnsToContents()

    def cari(self):
        cari = self.formclient.lineCari.text().strip()
        self.formclient.tblClient.setRowCount(0)
        self._cache_rows = self.aksi.filterClient(cari) if cari else self.aksi.dataClient()
        for i, r in enumerate(self._cache_rows):
            self.formclient.tblClient.insertRow(i)
            self.formclient.tblClient.setItem(i, 0, QTableWidgetItem(str(r["id_client"])))
            self.formclient.tblClient.setItem(i, 1, QTableWidgetItem(str(r["nama_client"])))
            self.formclient.tblClient.setItem(i, 2, QTableWidgetItem(str(r.get("email") or "")))
            self.formclient.tblClient.setItem(i, 3, QTableWidgetItem(str(r.get("no_hp") or "")))
            self.formclient.tblClient.setItem(i, 4, QTableWidgetItem(str(r.get("alamat") or "")))
        self.formclient.tblClient.resizeColumnsToContents()

    def pilih_baris(self, row, col):
        if row < 0 or row >= len(self._cache_rows):
            return
        r = self._cache_rows[row]
        self.formclient.EditId.setText(str(r["id_client"]))
        self.formclient.EditNama.setText(str(r["nama_client"]))
        self.formclient.EditEmail.setText(str(r.get("email") or ""))
        self.formclient.EditNoHP.setText(str(r.get("no_hp") or ""))
        self.formclient.EditAlamat.setPlainText(str(r.get("alamat") or ""))

    def cetak(self):
        try:
            self.aksi.cetakClient()
            QMessageBox.information(self, "Informasi", "Laporan berhasil dibuat (PDF).")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal cetak:\n{e}")
