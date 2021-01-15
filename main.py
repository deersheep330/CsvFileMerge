import sys
import os
from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QFileDialog, QVBoxLayout, QLabel

from merge.csv_merger import CsvMerger


class MainForm(QWidget):

    def __init__(self, name):

        super().__init__()

        self.csv_merger = CsvMerger(self.__append_text)

        self.files = []
        self.write_filename = ''

        self.setWindowTitle(name)
        self.cwd = os.getcwd()
        self.resize(300, 400)

        # button for add files
        self.btn_add_files = QPushButton(self)
        self.btn_add_files.setText('選取檔案')

        # label for display filename
        self.label = QLabel(self)
        self.label.resize(100, 200)

        # button for write file
        self.btn_write_file = QPushButton(self)
        self.btn_write_file.setText("合併檔案")

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.btn_add_files)
        layout.addWidget(self.label)
        layout.addWidget(self.btn_write_file)
        self.setLayout(layout)

        # set signal
        self.btn_add_files.clicked.connect(self.slot_btn_add_files)
        self.btn_write_file.clicked.connect(self.slot_btn_write_file)

    def __append_text(self, text):
        pre_text = self.label.text()
        self.label.setText(pre_text + '\n' + text)

    def slot_btn_add_files(self):
        files, filetype = QFileDialog.getOpenFileNames(self,
                                                       '選取一至多個檔案',
                                                       self.cwd,
                                                       'CSV (逗號分隔) (*.csv)')
        if len(files) == 0:
            self.files = []
            self.label.setText('請先選取檔案，再按合併')
        else:
            self.files = files
            self.label.setText('檔案清單\n' + '\n'.join(files))

    def slot_btn_write_file(self):
        write_filename, filetype = QFileDialog.getSaveFileName(self,
                                                               '儲存檔案',
                                                               self.cwd,
                                                               'CSV (逗號分隔) (*.csv)')
        self.write_filename = write_filename
        if len(self.files) == 0:
            self.label.setText('請先選取檔案，再按合併')
        elif len(write_filename) == 0:
            self.label.setText(self.label.text() + '\n' + '請先指定要寫入的檔案名')
        else:
            self.csv_merger.merge(self.files, self.write_filename)


if __name__ == '__main__':
    app = QApplication([])
    mainForm = MainForm('CSV File Merge')
    mainForm.show()
    sys.exit(app.exec_())
