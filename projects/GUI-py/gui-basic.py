from PyQt5.QtWidgets import QApplication, QLabel
import sys

app = QApplication(sys.argv)
label = QLabel("Hello, Wayland!")
label.show()
sys.exit(app.exec_())
