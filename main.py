import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

import enums
import menu
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QButtonGroup
import errors
import savmail
from PIL import Image


class MenuW(QMainWindow, menu.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.radioButton, 1)
        self.button_group.addButton(self.radioButton_2, 2)
        self.button_group.addButton(self.radioButton_3, 3)
        self.button_group.addButton(self.radioButton_4, 4)
        self.button_group.addButton(self.radioButton_5, 5)
        self.button_group.addButton(self.radioButton_6, 7)
        self.button_group.addButton(self.radioButton_7, 8)
        self.button_group.addButton(self.radioButton_8, 0)
        self.button_group.buttonClicked.connect(self.on_radio)
        # self.figure = plt.figure()
        # self.figure.subplots_adjust(top=1.0, bottom=0.0, left=0.0, right=1.0)
        # self.canvas = FigureCanvas(self.figure)
        self.pixmap = QPixmap("output0.png")
        self.label_3.setPixmap(self.pixmap)
        self.label_3.resize(500, 400)
        # qp = self.pixmap.scaled(self.label_3.size(), Qt.KeepAspectRatio, Qt.FastTransformation)
        # self.label_3.setPixmap(qp)
        self.save = None
        self.opensavebutton.clicked.connect(self.save_dialog)
        self.horizontalScrollBar.valueChanged.connect(self.show_current)
        self.pushButton.clicked.connect(self.export_image)
        self.pushButton_2.clicked.connect(self.export_images)
        self.orig_lang = 2

    def on_radio(self, button):
        if self.save:
            self.save.lang = self.button_group.id(button) if self.button_group.id(button) != 0 else self.orig_lang
            self.show_current()

    def resizeEvent(self, a0) -> None:
        qp = self.pixmap.scaled(self.label_3.size(), Qt.KeepAspectRatio, Qt.FastTransformation)
        # self.pixmap = qp
        self.label_3.setPixmap(qp)
        super().resizeEvent(a0)

    def save_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",  # Dialog title
            "",  # Start directory (empty for default)
            "Save files (*.sav);;All Files (*)"  # File filters
        )

        if file_path:
            try:
                self.save = savmail.SAV(file_path)
            except errors.IdkWhatVersionException:
                self.opensavebutton.setText("Not a gen 4 save!")
            else:
                self.opensavebutton.setText("Loaded!")
                self.load_save()
                self.orig_lang = self.save.lang

    def byte_to_pixmap(self, ind):
        pixmap = QPixmap()
        if mai := self.save.read_mail(ind):
            pixmap.loadFromData(mai.getvalue())
        return pixmap

    def export_image(self):
        if self.save:
            ind = self.horizontalScrollBar.value()
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Mail",  # Dialog title
                "",  # Start directory (empty for default)
                "Image File (*.png);;All Files (*)"  # File filters
            )
            if file_path:
                if mai := self.save.read_mail(ind):
                    img = Image.open(mai)
                    img.save(file_path)
                    img.close()

    def export_images(self):
        if self.save:
            file_path = QFileDialog.getExistingDirectory(
                self,
                "Save Folder",  # Dialog title
                "",  # Start directory (empty for default)
            )
            if file_path:
                for ind in range(20):
                    if mai := self.save.read_mail(ind):
                        img = Image.open(mai)
                        img.save(file_path + f'/mail{ind}.png')
                        img.close()

    def load_save(self):
        self.label_2.setText(f'Version: {self.save.version}')
        self.label.setText(f'Save language: {enums.languages[self.save.lang]}')
        self.pixmap = self.byte_to_pixmap(self.horizontalScrollBar.value())
        qp = self.pixmap.scaled(self.label_3.size(), Qt.KeepAspectRatio, Qt.FastTransformation)
        # self.pixmap = qp
        self.label_3.setPixmap(qp)
        self.button_group.button(0).setChecked(True)
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)

    def show_current(self):
        if self.save:
            self.pixmap = self.byte_to_pixmap(self.horizontalScrollBar.value())
            qp = self.pixmap.scaled(self.label_3.size(), Qt.KeepAspectRatio, Qt.FastTransformation)
            # self.pixmap = qp
            self.label_3.setPixmap(qp)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MenuW()
    ex.show()
    sys.exit(app.exec_())


# savefile = SAV('Pokemon HeartGold Version.sav')
# for i in range(20):
#     savefile.read_mail(i)
