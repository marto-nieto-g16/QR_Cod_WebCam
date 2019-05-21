
import sys
import qrcode

from PyQt4 import QtGui, QtCore 
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Image(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size):
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QtGui.QImage(
            size, size, QtGui.QImage.Format_RGB16)
        self._image.fill(QtCore.Qt.white)

    def pixmap(self):
        return QtGui.QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QtGui.QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            QtCore.Qt.black)

class Window(QtGui.QWidget):
    ruta = ""
    fichero_actual = ""

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.label = QtGui.QLabel(self)
        self.edit = QtGui.QLineEdit(self)
        self.button = QtGui.QPushButton("Guardar QR", self)  
        self.button.resize(100, 30) 

        self.edit.returnPressed.connect(self.handleTextEntered)
        self.button.clicked.connect(self.saveImage)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

    def handleTextEntered(self):
        text = unicode(self.edit.text())
        self.label.setPixmap(
            qrcode.make(text, image_factory=Image).pixmap())

    def saveImage(self):
        if unicode(self.edit.text()) != '':
            if self.fichero_actual:
                ruta_guardar = self.fichero_actual
            else:
                ruta_guardar = self.ruta

            nombre_fichero = QFileDialog.getSaveFileName(self, "Guardar Imagen QR", ruta_guardar, "PNG Image (*.png)" )
            if nombre_fichero:
                self.fichero_actual = nombre_fichero
                self.setWindowTitle(QFileInfo(nombre_fichero).fileName())
                self.ruta = QFileInfo(nombre_fichero).path()

                qr = qrcode.QRCode(version = 1, error_correction = qrcode.constants.ERROR_CORRECT_H, box_size = 10, border = 4,)
                qr.add_data(unicode(self.edit.text()))
                qr.make(fit=True)
                img = qr.make_image()
                img.save(str(QFileInfo(nombre_fichero).fileName())+".png")
        else:
            QtGui.QMessageBox.critical(self, "Error",  '''No Existe QR Para Guardar''', QtGui.QMessageBox.Ok)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 200, 200)
    window.show()
    sys.exit(app.exec_())