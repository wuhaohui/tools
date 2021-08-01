import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, QByteArray, QBuffer, QIODevice
import re
import os
import configparser
from aip import AipOcr
import keyboard


class ClipBoard(QWidget):

    def __init__(self):
        app = QApplication(sys.argv)
        super().__init__()
        # self.show()
        self.setHotKey()  # 设置热键
        sys.exit(app.exec_())

    def setHotKey(self):
        print('initHotKey')

        # self.bbs = QShortcut(QKeySequence(Qt.Key_F6), self)
        # self.key_f7 = QShortcut(QKeySequence(Qt.Key_F7), self)
        # self.bbs.activated.connect(self.transformTxtForMysql)
        # self.key_f7.activated.connect(self.transImage)
        keyboard.add_hotkey('f6', lambda: self.transformTxtForMysql())
        keyboard.add_hotkey('f7', lambda: self.transImage())
        # keyboard.wait()

    # 转换成 '123','12'
    def transformTxtForMysql(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        pattern = re.compile(r'(\S+)')
        data = pattern.findall(text)
        newText = ""
        for row in data:
            newText += '"' + row + '",'
        clipboard.setText(newText.strip(','))
        print('替换成功')

    # 图片转文字
    def transImage(self):
        APP_ID = '11041712'
        API_KEY = 'oT6GbdF8QslWmEh7Amzp33Rp'
        SECRET_KEY = 'GSMpovMRvOG7AI8Kki6f1l4hS2i7annU'

        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        clipboard = QApplication.clipboard()
        # print(clipboard.image())
        ba = QByteArray()
        buffer = QBuffer(ba)
        buffer.open(QIODevice.WriteOnly)
        clipboard.image().save(buffer, "jpeg")
        buffer.close()
        result = client.basicGeneral(ba)
        if result['words_result_num'] > 0:
            # 图片识别成功
            matchTxt = result['words_result'][0]['words']
            clipboard.setText(matchTxt)
            print('图片识别结果：' + matchTxt)
        else:
            print('识别失败')
