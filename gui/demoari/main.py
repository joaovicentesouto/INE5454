# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem

from MongoWrapper import MongoWrapper
from CassandraWrapper import CassandraWrapper

window = 0

def runQuery():
    # Get parameters and execute the query
    results, stats = execQuery()

    # Build the table
    window.resultsTable.setRowCount(results.shape[0])
    window.resultsTable.setColumnCount(results.shape[1])

    header = []
    for column in results.columns:
        header.append(column)

    window.resultsTable.setHorizontalHeaderLabels(header)

    rowCount = 0
    for i, row in results.iterrows():
        columnCount = 0
        for item in row:
            window.resultsTable.setItem(rowCount, columnCount, QTableWidgetItem(str(item)))
            columnCount += 1
        rowCount += 1

        if window.amountBox.isChecked():
            window.amountStat.setText('Amount by store:\n      Apple Store = ' + str(stats['amounts']['apple']) + ' apps\n      Google Store = ' + str(stats['amounts']['google']) + ' apps\n      Shopify Store = ' + str(stats['amounts']['shopify']) + ' apps')
        else:
            window.amountStat.setText('Amount by store:')

        if window.priceBox.isChecked():
            window.priceStat.setText('Price Statistics:\n      Maximum = ' + str(stats['prices']['max']) + '\n      Minimum = ' + str(stats['prices']['min']) + '\n      Average = ' + str(stats['prices']['sum'] / stats['prices']['count']))
        else:
            window.priceStat.setText('Price Statistics:')

        if window.associatedBox.isChecked():
            content = 'Associated Categories:\n      '

            count = 0
            for c in ', '.join(stats['categories']):
                if count > 110:
                    if c == ' ' or c == ',':
                        content = content + c + '\n      '
                    else:
                        content = content + c + '-\n      '
                    count = 0
                else:
                    content = content + c
                    count += 1

            window.associatedStat.setText(content)
        else:
            window.associatedStat.setText('Associated Categories:')

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
        min_rating = float(ratingText)

    sort = True
    orderBy = None
    orderText = window.orderCombo.currentText()
    if orderText != 'none' and window.orderBox.isChecked():
        orderBy = orderText
        if  window.highLowRadio.isChecked():
            sort = False

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

    wrapper = MongoWrapper()

    if not reviews:
        return wrapper.query(names, categories, gt, min_rating, orderBy, sort, stats, False)

    ids, stats = wrapper.query(names, categories, gt, min_rating, orderBy, sort, stats, True)

    wrapper = CassandraWrapper()

    return wrapper.query(ids, orderBy, sort, sentiment), stats

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
