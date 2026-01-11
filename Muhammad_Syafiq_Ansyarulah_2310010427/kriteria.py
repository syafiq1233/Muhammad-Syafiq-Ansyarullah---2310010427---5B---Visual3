# This Python file uses the following encoding: utf-8
import os

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox

from crud import crud_app


def ui_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)


class form_kriteria(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        filenya = QFile(ui_path("kriteria.ui"))
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formkriteria = muatfile.load(filenya, self)
        filenya.close()

        self.setWindowTitle(self.formkriteria.windowTitle())
        self.resize(self.formkriteria.size())

        self.aksi = crud_app()
        self._cache_rows = []

        self.formkriteria.BtnSimpan.clicked.connect(self.simpan)
        self.formkriteria.BtnUbah.clicked.connect(self.ubah)
        self.formkriteria.BtnHapus.clicked.connect(self.hapus)
        self.formkriteria.BtnBersih.clicked.connect(self.bersih)
        self.formkriteria.lineCari.textChanged.connect(self.cari)
        self.formkriteria.btnCetak.clicked.connect(self.cetak)
        self.formkriteria.tblKriteria.cellClicked.connect(self.pilih_baris)

        self.tampil()

    def bersih(self):
        self.formkriteria.EditId.clear()
        self.formkriteria.EditNama.clear()
        self.formkriteria.SpinBobot.setValue(0.0)
        self.formkriteria.ComboSifat.setCurrentIndex(0)
        self.formkriteria.EditNama.setFocus()

    def validasi(self, untuk_update=False) -> bool:
        if untuk_update and not self.formkriteria.EditId.text().strip():
            QMessageBox.information(self, "Informasi", "Pilih data dulu (klik tabel) untuk diubah/dihapus.")
            return False
        if not self.formkriteria.EditNama.text().strip():
            QMessageBox.information(self, "Informasi", "Nama Kriteria belum diisi.")
            self.formkriteria.EditNama.setFocus()
            return False
        return True

    def simpan(self):
        if not self.validasi(False):
            return
        try:
            self.aksi.tambahKriteria(
                self.formkriteria.EditNama.text().strip(),
                float(self.formkriteria.SpinBobot.value()),
                self.formkriteria.ComboSifat.currentText(),
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
            self.aksi.gantiKriteria(
                int(self.formkriteria.EditId.text()),
                self.formkriteria.EditNama.text().strip(),
                float(self.formkriteria.SpinBobot.value()),
                self.formkriteria.ComboSifat.currentText(),
            )
            self.tampil()
            QMessageBox.information(self, "Informasi", "Data berhasil diubah.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal ubah:\n{e}")

    def hapus(self):
        if not self.formkriteria.EditId.text().strip():
            QMessageBox.information(self, "Informasi", "Pilih data dulu (klik tabel) untuk dihapus.")
            return
        pesan = QMessageBox.information(
            self, "Informasi", "Apakah yakin menghapus data ini?", QMessageBox.Yes | QMessageBox.No
        )
        if pesan != QMessageBox.Yes:
            return
        try:
            self.aksi.kurangKriteria(int(self.formkriteria.EditId.text()))
            self.tampil()
            self.bersih()
            QMessageBox.information(self, "Informasi", "Data berhasil dihapus.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal hapus:\n{e}")

    def tampil(self):
        self.formkriteria.tblKriteria.setRowCount(0)
        self._cache_rows = self.aksi.dataKriteria()
        for i, r in enumerate(self._cache_rows):
            self.formkriteria.tblKriteria.insertRow(i)
            self.formkriteria.tblKriteria.setItem(i, 0, QTableWidgetItem(str(r["id_kriteria"])))
            self.formkriteria.tblKriteria.setItem(i, 1, QTableWidgetItem(str(r["nama_kriteria"])))
            self.formkriteria.tblKriteria.setItem(i, 2, QTableWidgetItem(str(r["bobot"])))
            self.formkriteria.tblKriteria.setItem(i, 3, QTableWidgetItem(str(r["sifat"])))
        self.formkriteria.tblKriteria.resizeColumnsToContents()

    def cari(self):
        cari = self.formkriteria.lineCari.text().strip()
        self.formkriteria.tblKriteria.setRowCount(0)
        self._cache_rows = self.aksi.filterKriteria(cari) if cari else self.aksi.dataKriteria()
        for i, r in enumerate(self._cache_rows):
            self.formkriteria.tblKriteria.insertRow(i)
            self.formkriteria.tblKriteria.setItem(i, 0, QTableWidgetItem(str(r["id_kriteria"])))
            self.formkriteria.tblKriteria.setItem(i, 1, QTableWidgetItem(str(r["nama_kriteria"])))
            self.formkriteria.tblKriteria.setItem(i, 2, QTableWidgetItem(str(r["bobot"])))
            self.formkriteria.tblKriteria.setItem(i, 3, QTableWidgetItem(str(r["sifat"])))
        self.formkriteria.tblKriteria.resizeColumnsToContents()

    def pilih_baris(self, row, col):
        if row < 0 or row >= len(self._cache_rows):
            return
        r = self._cache_rows[row]
        self.formkriteria.EditId.setText(str(r["id_kriteria"]))
        self.formkriteria.EditNama.setText(str(r["nama_kriteria"]))
        self.formkriteria.SpinBobot.setValue(float(r["bobot"]))
        idx = self.formkriteria.ComboSifat.findText(str(r["sifat"]))
        self.formkriteria.ComboSifat.setCurrentIndex(idx if idx >= 0 else 0)

    def cetak(self):
        try:
            self.aksi.cetakKriteria()
            QMessageBox.information(self, "Informasi", "Laporan berhasil dibuat (PDF).")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal cetak:\n{e}")
