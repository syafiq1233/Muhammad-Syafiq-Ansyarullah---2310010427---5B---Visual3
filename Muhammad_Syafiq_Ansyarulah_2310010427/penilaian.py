# This Python file uses the following encoding: utf-8
import os

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox

from crud import crud_app


def ui_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)


class form_penilaian(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        filenya = QFile(ui_path("penilaian.ui"))
        filenya.open(QFile.ReadOnly)
        muatfile = QUiLoader()
        self.formpenilaian = muatfile.load(filenya, self)
        filenya.close()

        self.setWindowTitle(self.formpenilaian.windowTitle())
        self.resize(self.formpenilaian.size())

        self.aksi = crud_app()
        self._cache_rows = []

        self.formpenilaian.BtnSimpan.clicked.connect(self.simpan)
        self.formpenilaian.BtnUbah.clicked.connect(self.ubah)
        self.formpenilaian.BtnHapus.clicked.connect(self.hapus)
        self.formpenilaian.BtnBersih.clicked.connect(self.bersih)
        self.formpenilaian.lineCari.textChanged.connect(self.cari)
        self.formpenilaian.btnCetak.clicked.connect(self.cetak)
        self.formpenilaian.tblPenilaian.cellClicked.connect(self.pilih_baris)

        self.muat_combo()
        self.tampil()

    def muat_combo(self):
        # client
        self.formpenilaian.ComboClient.clear()
        for r in self.aksi.dataClient():
            self.formpenilaian.ComboClient.addItem(str(r["nama_client"]), int(r["id_client"]))

        # paket
        self.formpenilaian.ComboPaket.clear()
        for r in self.aksi.dataPaket():
            self.formpenilaian.ComboPaket.addItem(str(r["nama_paket"]), int(r["id_paket"]))

        # kriteria
        self.formpenilaian.ComboKriteria.clear()
        for r in self.aksi.dataKriteria():
            self.formpenilaian.ComboKriteria.addItem(str(r["nama_kriteria"]), int(r["id_kriteria"]))

    def bersih(self):
        self.formpenilaian.EditId.clear()
        if self.formpenilaian.ComboClient.count() > 0:
            self.formpenilaian.ComboClient.setCurrentIndex(0)
        if self.formpenilaian.ComboPaket.count() > 0:
            self.formpenilaian.ComboPaket.setCurrentIndex(0)
        if self.formpenilaian.ComboKriteria.count() > 0:
            self.formpenilaian.ComboKriteria.setCurrentIndex(0)
        self.formpenilaian.SpinNilai.setValue(0.0)

    def validasi(self, untuk_update=False) -> bool:
        if untuk_update and not self.formpenilaian.EditId.text().strip():
            QMessageBox.information(self, "Informasi", "Pilih data dulu (klik tabel) untuk diubah/dihapus.")
            return False
        if self.formpenilaian.ComboClient.count() == 0:
            QMessageBox.information(self, "Informasi", "Data client masih kosong. Isi data client dulu.")
            return False
        if self.formpenilaian.ComboPaket.count() == 0:
            QMessageBox.information(self, "Informasi", "Data paket masih kosong. Isi data paket dulu.")
            return False
        if self.formpenilaian.ComboKriteria.count() == 0:
            QMessageBox.information(self, "Informasi", "Data kriteria masih kosong. Isi data kriteria dulu.")
            return False
        return True

    def simpan(self):
        if not self.validasi(False):
            return
        try:
            id_client = int(self.formpenilaian.ComboClient.currentData())
            id_paket = int(self.formpenilaian.ComboPaket.currentData())
            id_kriteria = int(self.formpenilaian.ComboKriteria.currentData())
            nilai = float(self.formpenilaian.SpinNilai.value())

            self.aksi.tambahPenilaian(id_client, id_paket, id_kriteria, nilai)
            self.tampil()
            self.bersih()
            QMessageBox.information(self, "Informasi", "Data berhasil disimpan.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal simpan:\n{e}")

    def ubah(self):
        if not self.validasi(True):
            return
        try:
            id_penilaian = int(self.formpenilaian.EditId.text())
            id_client = int(self.formpenilaian.ComboClient.currentData())
            id_paket = int(self.formpenilaian.ComboPaket.currentData())
            id_kriteria = int(self.formpenilaian.ComboKriteria.currentData())
            nilai = float(self.formpenilaian.SpinNilai.value())

            self.aksi.gantiPenilaian(id_penilaian, id_client, id_paket, id_kriteria, nilai)
            self.tampil()
            QMessageBox.information(self, "Informasi", "Data berhasil diubah.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal ubah:\n{e}")

    def hapus(self):
        if not self.formpenilaian.EditId.text().strip():
            QMessageBox.information(self, "Informasi", "Pilih data dulu (klik tabel) untuk dihapus.")
            return
        pesan = QMessageBox.information(
            self, "Informasi", "Apakah yakin menghapus data ini?", QMessageBox.Yes | QMessageBox.No
        )
        if pesan != QMessageBox.Yes:
            return
        try:
            self.aksi.kurangPenilaian(int(self.formpenilaian.EditId.text()))
            self.tampil()
            self.bersih()
            QMessageBox.information(self, "Informasi", "Data berhasil dihapus.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal hapus:\n{e}")

    def tampil(self):
        self.formpenilaian.tblPenilaian.setRowCount(0)
        self._cache_rows = self.aksi.dataPenilaian()
        for i, r in enumerate(self._cache_rows):
            self.formpenilaian.tblPenilaian.insertRow(i)
            self.formpenilaian.tblPenilaian.setItem(i, 0, QTableWidgetItem(str(r["id_penilaian"])))
            self.formpenilaian.tblPenilaian.setItem(i, 1, QTableWidgetItem(str(r.get("nama_client") or "")))
            self.formpenilaian.tblPenilaian.setItem(i, 2, QTableWidgetItem(str(r.get("nama_paket") or "")))
            self.formpenilaian.tblPenilaian.setItem(i, 3, QTableWidgetItem(str(r.get("nama_kriteria") or "")))
            self.formpenilaian.tblPenilaian.setItem(i, 4, QTableWidgetItem(str(r.get("nilai") if r.get("nilai") is not None else "")))
        self.formpenilaian.tblPenilaian.resizeColumnsToContents()

    def cari(self):
        cari = self.formpenilaian.lineCari.text().strip()
        self.formpenilaian.tblPenilaian.setRowCount(0)
        self._cache_rows = self.aksi.filterPenilaian(cari) if cari else self.aksi.dataPenilaian()
        for i, r in enumerate(self._cache_rows):
            self.formpenilaian.tblPenilaian.insertRow(i)
            self.formpenilaian.tblPenilaian.setItem(i, 0, QTableWidgetItem(str(r["id_penilaian"])))
            self.formpenilaian.tblPenilaian.setItem(i, 1, QTableWidgetItem(str(r.get("nama_client") or "")))
            self.formpenilaian.tblPenilaian.setItem(i, 2, QTableWidgetItem(str(r.get("nama_paket") or "")))
            self.formpenilaian.tblPenilaian.setItem(i, 3, QTableWidgetItem(str(r.get("nama_kriteria") or "")))
            self.formpenilaian.tblPenilaian.setItem(i, 4, QTableWidgetItem(str(r.get("nilai") if r.get("nilai") is not None else "")))
        self.formpenilaian.tblPenilaian.resizeColumnsToContents()

    def pilih_baris(self, row, col):
        if row < 0 or row >= len(self._cache_rows):
            return
        r = self._cache_rows[row]
        self.formpenilaian.EditId.setText(str(r["id_penilaian"]))

        idx = self.formpenilaian.ComboClient.findData(int(r["id_client"]) if r.get("id_client") else -1)
        if idx >= 0:
            self.formpenilaian.ComboClient.setCurrentIndex(idx)

        idx = self.formpenilaian.ComboPaket.findData(int(r["id_paket"]) if r.get("id_paket") else -1)
        if idx >= 0:
            self.formpenilaian.ComboPaket.setCurrentIndex(idx)

        idx = self.formpenilaian.ComboKriteria.findData(int(r["id_kriteria"]) if r.get("id_kriteria") else -1)
        if idx >= 0:
            self.formpenilaian.ComboKriteria.setCurrentIndex(idx)

        self.formpenilaian.SpinNilai.setValue(float(r.get("nilai") or 0.0))

    def cetak(self):
        try:
            self.aksi.cetakPenilaian()
            QMessageBox.information(self, "Informasi", "Laporan berhasil dibuat (PDF).")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal cetak:\n{e}")
