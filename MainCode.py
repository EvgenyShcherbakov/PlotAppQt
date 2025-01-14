import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, \
    QLineEdit, QPushButton, QLabel, QScrollArea, QMessageBox


class PlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Function Plotter')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.functionInput = QLineEdit(self)
        self.functionInput.setPlaceholderText("Enter function, e.g. x*x + 3")
        self.layout.addWidget(self.functionInput)

        self.rangeInput = QLineEdit(self)
        self.rangeInput.setPlaceholderText("Enter range, e.g. -2,4")
        self.layout.addWidget(self.rangeInput)

        self.plotButton = QPushButton("Plot Function", self)
        self.plotButton.clicked.connect(self.plotFunction)
        self.layout.addWidget(self.plotButton)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.layout.addWidget(self.scrollArea)

        self.figureLabel = QLabel(self)
        self.scrollArea.setWidget(self.figureLabel)

    def plotFunction(self):
        try:
            function_str = self.functionInput.text()
            range_str = self.rangeInput.text()
            x_range = list(map(float, range_str.split(',')))

            func = eval("lambda x: " + function_str)
            x = np.linspace(x_range[0], x_range[1], 400)
            y = func(x)

            plt.figure()
            plt.plot(x, y)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'Plot of {function_str}')
            file_path = 'plot.png'
            plt.savefig(file_path)
            plt.close()

            self.figureLabel.setPixmap(QPixmap(file_path))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def closeEvent(self, event):
        file_path = 'plot.png'
        if os.path.exists(file_path):
            os.remove(file_path)
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlotApp()
    window.show()
    sys.exit(app.exec_())
