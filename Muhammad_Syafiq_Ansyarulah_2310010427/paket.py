# This Python file uses the following encoding: utf-8
import os

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox

from crud import crud_app


def ui_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)


class form_paket(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        filenya = QFile(ui_path("paket.ui"))
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formpaket = muatfile.load(filenya, self)
        filenya.close()

        self.setWindowTitle(self.formpaket.windowTitle())
        self.resize(self.formpaket.size())

        self.aksi = crud_app()
        self._cache_rows = []

        self.formpaket.BtnSimpan.clicked.connect(self.simpan)
        self.formpaket.BtnUbah.clicked.connect(self.ubah)
        self.formpaket.BtnHapus.clicked.connect(self.hapus)
        self.formpaket.BtnBersih.clicked.connect(self.bersih)
        self.formpaket.lineCari.textChanged.connect(self.cari)
        self.formpaket.btnCetak.clicked.connect(self.cetak)
        self.formpaket.tblPaket.cellClicked.connect(self.pilih_baris)

        self.tampil()

    def bersih(self):
        self.formpaket.EditId.clear()
        self.formpaket.EditNama.clear()
        self.formpaket.SpinHarga.setValue(0.0)
        self.formpaket.EditDeskripsi.clear()
        self.formpaket.EditNama.setFocus()

    def validasi(self, untuk_update=False) -> bool:
        if untuk_update and not self.formpaket.EditId.text().strip():
            QMessageBox.information(self, "Informasi", "Pilih data dulu (klik tabel) untuk diubah/dihapus.")
            return False
        if not self.formpaket.EditNama.text().strip():
            QMessageBox.information(self, "Informasi", "Nama Paket belum diisi.")
            self.formpaket.EditNama.setFocus()
            return False
        return True

    def simpan(self):
        if not self.validasi(False):
            return
        try:
            self.aksi.tambahPaket(
                self.formpaket.EditNama.text().strip(),
                float(self.formpaket.SpinHarga.value()),
                self.formpaket.EditDeskripsi.toPlainText().strip() or None,
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
            self.aksi.gantiPaket(
                int(self.formpaket.EditId.text()),
                self.formpaket.EditNama.text().strip(),
                float(self.formpaket.SpinHarga.value()),
                self.formpaket.EditDeskripsi.toPlainText().strip() or None,
            )
            self.tampil()
            QMessageBox.information(self, "Informasi", "Data berhasil diubah.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal ubah:\n{e}")

    def hapus(self):
        if not self.formpaket.EditId.text().strip():
            QMessageBox.information(self, "Informasi", "Pilih data dulu (klik tabel) untuk dihapus.")
            return
        pesan = QMessageBox.information(
            self, "Informasi", "Apakah yakin menghapus data ini?", QMessageBox.Yes | QMessageBox.No
        )
        if pesan != QMessageBox.Yes:
            return
        try:
            self.aksi.kurangPaket(int(self.formpaket.EditId.text()))
            self.tampil()
            self.bersih()
            QMessageBox.information(self, "Informasi", "Data berhasil dihapus.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal hapus:\n{e}")

    def tampil(self):
        self.formpaket.tblPaket.setRowCount(0)
        self._cache_rows = self.aksi.dataPaket()
        for i, r in enumerate(self._cache_rows):
            self.formpaket.tblPaket.insertRow(i)
            self.formpaket.tblPaket.setItem(i, 0, QTableWidgetItem(str(r["id_paket"])))
            self.formpaket.tblPaket.setItem(i, 1, QTableWidgetItem(str(r["nama_paket"])))
            self.formpaket.tblPaket.setItem(i, 2, QTableWidgetItem(str(r.get("harga") if r.get("harga") is not None else "")))
            self.formpaket.tblPaket.setItem(i, 3, QTableWidgetItem(str(r.get("deskripsi") or "")))
        self.formpaket.tblPaket.resizeColumnsToContents()

    def cari(self):
        cari = self.formpaket.lineCari.text().strip()
        self.formpaket.tblPaket.setRowCount(0)
        self._cache_rows = self.aksi.filterPaket(cari) if cari else self.aksi.dataPaket()
        for i, r in enumerate(self._cache_rows):
            self.formpaket.tblPaket.insertRow(i)
            self.formpaket.tblPaket.setItem(i, 0, QTableWidgetItem(str(r["id_paket"])))
            self.formpaket.tblPaket.setItem(i, 1, QTableWidgetItem(str(r["nama_paket"])))
            self.formpaket.tblPaket.setItem(i, 2, QTableWidgetItem(str(r.get("harga") if r.get("harga") is not None else "")))
            self.formpaket.tblPaket.setItem(i, 3, QTableWidgetItem(str(r.get("deskripsi") or "")))
        self.formpaket.tblPaket.resizeColumnsToContents()

    def pilih_baris(self, row, col):
        if row < 0 or row >= len(self._cache_rows):
            return
        r = self._cache_rows[row]
        self.formpaket.EditId.setText(str(r["id_paket"]))
        self.formpaket.EditNama.setText(str(r["nama_paket"]))
        self.formpaket.SpinHarga.setValue(float(r.get("harga") or 0.0))
        self.formpaket.EditDeskripsi.setPlainText(str(r.get("deskripsi") or ""))

    def cetak(self):
        try:
            self.aksi.cetakPaket()
            QMessageBox.information(self, "Informasi", "Laporan berhasil dibuat (PDF).")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal cetak:\n{e}")
