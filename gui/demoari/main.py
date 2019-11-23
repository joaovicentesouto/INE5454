# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QApplication, QMainWindow

from MongoWrapper import MongoWrapper
from CassandraWrapper import CassandraWrapper

window = 0

def runQuery():
#    updateTable(createTable(*execQuery()))
    print(execQuery(), flush = True)

def execQuery():

    names = []
    nameText = window.nameField.text()
    if nameText != '' and window.nameBox.isChecked():
        names = nameText.split(',')

    categories = []
    categoriesText = window.categoriesField.text()
    if categoriesText != '' and window.categoriesBox.isChecked():
        categories = categoriesText.split(',')

    gt = 0
    if window.ratingBox.isChecked():
        gt = 1
        if window.ltRadio.isChecked():
            gt = -1

    min_rating = 0
    ratingText = window.ratingField.text()
    if ratingText != '' and window.ratingBox.isChecked():
        min_rating = int(ratingText)

    sort = 'asc'
    orderBy = None
    orderText = window.orderCombo.currentText()
    if orderText != 'none' and window.orderBox.isChecked():
        orderBy = orderText
        if  window.highLowRadio.isChecked():
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
    if reviews and window.sentimentBox.isChecked():
        sentiment = 1
        if window.negativeRadio.isChecked():
            sentiment = -1

    if not reviews:
        wrapper = MongoWrapper()
        return wrapper.query(names, categories, gt, min_rating, orderBy, sort, stats, [])

    print('\nNames: ', names, '\nCategories: ', categories, '\nGt: ', gt, '\nMin Rating: ', min_rating, '\nOrderby: ', orderBy, '\nSort Rule: ', sort, '\nStats: ', stats, '\nReviews: ', reviews, '\nSentiment', sentiment, flush=True)

#    wrapper = MongoWrapper()
#    ids, stats = wrapper.query(names, categories, gt, ratingText, orderText, sort, stats, ['id'])

#    wrapper = CassandraWrapper()
#    return wrapper.query(ids, gt, ratingText, orderText, sort, sentiment)

#    return ids, stats
    return [],[]

def createTable(text, vector):
    return ''

def updateTable(content):
    print(content)

if __name__ == "__main__":
    app = QApplication([])

    ui_file = QFile("/home/bonotto/Dropbox/Faculdade/2019-02/Gestao_de_BD/gui/demoari/mainwindow.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)

    window.runButton.clicked.connect(runQuery)

    window.orderCombo.addItem('none')
    window.orderCombo.addItem('name')
    window.orderCombo.addItem('categories')
    window.orderCombo.addItem('rating')
    window.orderCombo.addItem('sentiment')

    window.positiveRadio.setChecked(True)
    window.gtRadio.setChecked(True)
    window.lowHighRadio.setChecked(True)

    window.show()

    sys.exit(app.exec_())
