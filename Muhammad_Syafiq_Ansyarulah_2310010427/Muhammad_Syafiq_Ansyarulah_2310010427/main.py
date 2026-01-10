import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QAction

from client import form_client
from paket import form_paket
from kriteria import form_kriteria
from penilaian import form_penilaian


class AppMain:
    def __init__(self):
        self.forms = {}

        loader = QUiLoader()
        ui_file = QFile("main.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Gagal membuka main.ui")
        self.window = loader.load(ui_file)
        ui_file.close()

        if self.window is None:
            raise RuntimeError("Gagal load main.ui (hasil loader None)")

        self._connect_actions()

    def _connect_actions(self):
        def bind(action_name, fn):
            act = self.window.findChild(QAction, action_name)
            if act is None:
                # Debug cepat: print semua action yang kebaca
                print(f"[ERROR] QAction tidak ketemu: {action_name}")
                print("Daftar QAction yang ada:")
                for a in self.window.findChildren(QAction):
                    print(" -", a.objectName())
                return
            act.triggered.connect(fn)

        bind("actionDATA_CLIENT", self.buka_client)
        bind("actionDATA_PAKET", self.buka_paket)
        bind("actionDATA_KRITERIA", self.buka_kriteria)
        bind("actionDATA_PENILAIAN", self.buka_penilaian)

    def buka_client(self):
        if "client" not in self.forms:
            self.forms["client"] = form_client()
        self.forms["client"].show()
        self.forms["client"].raise_()
        self.forms["client"].activateWindow()

    def buka_paket(self):
        if "paket" not in self.forms:
            self.forms["paket"] = form_paket()
        self.forms["paket"].show()
        self.forms["paket"].raise_()
        self.forms["paket"].activateWindow()

    def buka_kriteria(self):
        if "kriteria" not in self.forms:
            self.forms["kriteria"] = form_kriteria()
        self.forms["kriteria"].show()
        self.forms["kriteria"].raise_()
        self.forms["kriteria"].activateWindow()

    def buka_penilaian(self):
        if "penilaian" not in self.forms:
            self.forms["penilaian"] = form_penilaian()
        self.forms["penilaian"].show()
        self.forms["penilaian"].raise_()
        self.forms["penilaian"].activateWindow()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    jendela = AppMain()
    jendela.window.show()
    sys.exit(app.exec())
