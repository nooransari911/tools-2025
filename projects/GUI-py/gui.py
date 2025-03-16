import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class ProfileApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create the layout
        layout = QVBoxLayout()

        # Create and set up widgets
        self.title = QLabel("ChatGPT - AI Assistant", self)
        self.description = QLabel("I am a large language model created by OpenAI.\nI can help with various tasks and answer questions.", self)
        self.more_info_btn = QPushButton("More Info", self)
        
        # Connect the button click to show more information
        self.more_info_btn.clicked.connect(self.show_more_info)

        # Add widgets to the layout
        layout.addWidget(self.title)
        layout.addWidget(self.description)
        layout.addWidget(self.more_info_btn)

        # Set layout for the window
        self.setLayout(layout)

        # Window title and size
        self.setWindowTitle('About ChatGPT')
        self.setGeometry(300, 300, 400, 200)

    def show_more_info(self):
        # Show additional info when the button is clicked
        self.description.setText(
            "I am a cutting-edge AI trained on diverse data sources.\n"
            "I can assist with programming, creative writing, general knowledge, and more!\n"
            "I learn from large datasets but don't have personal experiences."
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProfileApp()
    window.show()
    sys.exit(app.exec_())

