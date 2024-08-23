from try_script import try_func
from tab_script import tab_func
from ab_script import ab_func
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6.QtCore import QStringListModel
from untitled import Ui_Form
import sys


class Window(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('AB TOOL')

        # 控件初始化
        self.pushButton.clicked.connect(lambda: self.load_func())
        self.pushButton_2.clicked.connect(lambda: self.calc_func(2))
        self.pushButton_3.clicked.connect(lambda: self.tab_func('+'))
        self.pushButton_4.clicked.connect(lambda: self.tab_func('-'))
        self.pushButton_5.clicked.connect(lambda: self.calc_func(1))
        self.pushButton_6.clicked.connect(lambda: self.save_func())
        self.pushButton_7.clicked.connect(lambda: self.undo_func())
        self.pushButton_8.clicked.connect(lambda: self.save_open_func())
        self.pushButton_9.clicked.connect(lambda: self.calc_func(2, True))
        self.pushButton_10.clicked.connect(lambda: self.calc_func(1, True))
        self.label.setText('OK.')

        # 绑定快捷键
        self.pushButton.setShortcut('ctrl+L')
        self.pushButton_6.setShortcut('ctrl+S')
        self.pushButton_5.setShortcut('ctrl+1')
        self.pushButton_2.setShortcut('ctrl+2')
        self.pushButton_7.setShortcut('ctrl+`')

        self.fn = None  # 保存文件名的默认值
        self.ab = None  # 保存字段，方便回退
        self.url = None  # 保存路径

    @try_func
    def load_func(self):
        url, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "文本文件 (*.txt);;所有文件 (*)")
        if url:
            with open(url, 'r') as f:
                ls = f.readlines()
            m = QStringListModel()  # 建立模型
            m.setStringList(ls)  # 写入内容至模型
            self.listView.setModel(m)  # lv绑定模型
            self.fn = url.split('/')[-1]  # 记忆文件名
            self.label.setText('load file. finsh.')

    @try_func
    def tab_func(self, x: str):
        """
        :param x: +是进格，-是退格
        :return:
        """
        m = self.listView.model()  # 读模型，QStringListModel
        ls = self.listView.selectionModel().selectedIndexes()  # [<PyQt6.QtCore.QModelIndex>]
        for i in ls:
            ab = m.data(i)  # 读
            self.ab = str(ab)
            ab2 = tab_func(ab, x)  # +是进格，-是退格
            m.setData(i, ab2)  # 写

    @try_func
    def calc_func(self, x, y=False):
        """
        :param x: 1是大招，2是普通技
        :param y: 强制 "" mod模板 ，默认false
        """
        m = self.listView.model()  # 读模型，QStringListModel
        ls = self.listView.selectionModel().selectedIndexes()  # [<PyQt6.QtCore.QModelIndex>]
        for i in ls:
            ab = m.data(i)  # 读
            ab2 = ab_func(ab, x, y)  # 计算后x位
            m.setData(i, ab2)  # 写
            self.ab = f'{ab}'  # 备份原字段

    @try_func
    def undo_func(self):
        m = self.listView.model()  # 读模型，QStringListModel
        ls = self.listView.selectionModel().selectedIndexes()  # [<PyQt6.QtCore.QModelIndex>]
        for i in ls:
            if self.ab:
                m.setData(i, self.ab)  # 写

    @try_func
    def save_func(self):
        url, _ = QFileDialog.getSaveFileName(self, "保存文件", self.fn, "文本文件 (*.txt);;所有文件 (*)")
        if url:
            with open(url, 'w') as f:
                m = self.listView.model()  # 读模型，QStringListModel
                row = m.rowCount()  # 共多少行
                ls = []
                for r in range(row):
                    i = m.index(r, 0)  # r行0列
                    tx = m.data(i)  # 内容
                    ls.append(tx)  # 写入列表
                f.writelines(ls)  # 写
            self.url = f'{url}'
            self.label.setText('save file. finsh.')

    @try_func
    def open_func(self):
        import os
        if self.url:
            os.startfile(self.url)

    @try_func
    def save_open_func(self):
        self.save_func()
        self.open_func()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec()
