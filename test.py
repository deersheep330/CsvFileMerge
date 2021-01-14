import sys
import os
from PySide6.QtWidgets import QWidget, QApplication, QPushButton, QFileDialog, QVBoxLayout, QLabel


class MainForm(QWidget):

    def __init__(self, name):

        super().__init__()

        self.files = []

        self.setWindowTitle(name)
        self.cwd = os.getcwd()
        self.resize(300, 400)

        # button for add files
        self.btn_add_files = QPushButton(self)
        self.btn_add_files.setText('添加檔案')

        # label for display filename
        self.label = QLabel(self)
        self.label.resize(200, 400)

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

    def slot_btn_add_files(self):
        files, filetype = QFileDialog.getOpenFileNames(self,
                                                       '添加一至多個檔案',
                                                       self.cwd,
                                                       'CSV (逗號分隔) (*.csv)')
        if len(files) == 0:
            self.files = []
        else:
            self.files = files
        self.label.setText('\n'.join(files))

    def slot_btn_write_file(self):
        write_filename, filetype = QFileDialog.getSaveFileName(self,
                                                               '儲存檔案',
                                                               self.cwd,
                                                               'CSV (逗號分隔) (*.csv)')

        if write_filename == "":
            print("\n取消选择")
            return

        print("\n你选择要保存的文件为:")
        print(write_filename)
        print("文件筛选器类型: ",filetype)


if __name__ == '__main__':
    app = QApplication([])
    mainForm = MainForm('CSV File Merge')
    mainForm.show()
    sys.exit(app.exec_())
