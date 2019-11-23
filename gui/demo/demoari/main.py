# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QApplication, QMainWindow

from MongoWrapper import MongoWrapper
from CassandraWrapper import CassandraWrapper

window = 0

def runQuery():
    updateTable(createTable(*execQuery()))

def execQuery():

    nameText = window.nameField.text()
    ratingText = window.ratingField.text()
    orderText = window.orderCombo.currentText()
    categoriesText = window.categoriesField.text()

    gt = 0
    if window.ratingBox.isChecked():
        gt = 1
        if window.highLowRadio.isChecked():
            gt = -1

    sort = 'asc'
    if window.highLowRadio.isChecked():
        sort = 'desc'

    stats = []
    if window.amountBox.isChecked():
        stats.append('amounts')

    if window.associatedBox.isChecked():
        stats.append('categories')

    if window.priceBox.isChecked():
        stats.append('prices')

    reviews = False
    if window.reviewsBox.isChecked():
        reviews = True

    sentiment = 0
    if window.sentimentBox.isChecked():
        sentiment = 1
        if window.negative.isChecked():
            sentiment = -1

    if not reviews:
        wrapper = MongoWrapper()
        return wrapper.query(nameText, categoriesText, gt, ratingText, orderText, sort, stats, [])

    wrapper = MongoWrapper()
    ids, stats = wrapper.query(nameText, categoriesText, gt, ratingText, orderText, sort, stats, ['id'])

#    wrapper = CassandraWrapper()
#    return wrapper.query(ids, gt, ratingText, orderText, sort, sentiment)

    return ids, stats

def createTable(text, vector):
    print(text)
    print(vector)
    return ''

def updateTable(content):
    print(content)

if __name__ == "__main__":
    app = QApplication([])

    ui_file = QFile("/home/bonotto/Downloads/INE5454/gui/demo/demoari/mainwindow.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)

    window.runButton.clicked.connect(runQuery)

    window.orderCombo.addItem('Name')
    window.orderCombo.addItem('Categories')
    window.orderCombo.addItem('Rating')
    window.orderCombo.addItem('Sentiment')

    window.show()

    sys.exit(app.exec_())
