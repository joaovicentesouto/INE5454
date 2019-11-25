# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem

from MongoWrapper import MongoWrapper
from CassandraWrapper import CassandraWrapper

window = 0

def buildTable(results, stats):

    maxSize = 1000
    if results.shape[0] < 1000:
        maxSize = results.shape[0]

    window.resultsTable.setRowCount(maxSize)
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
        if rowCount > 999:
            break

    if window.statsBox.isChecked():
        window.amountStat.setText('Amount by store:\n      Apple Store = ' + str(stats['amounts']['apple']) + ' apps\n      Google Store = ' + str(stats['amounts']['google']) + ' apps\n      Shopify Store = ' + str(stats['amounts']['shopify']) + ' apps')
        window.priceStat.setText('Price Statistics:\n      Maximum = US$ ' + str(stats['prices']['max']) + '\n      Minimum = US$ ' + str(stats['prices']['min']) + '\n      Average = US$ ' + str(stats['prices']['sum'] / stats['prices']['count']))

        content = 'Associated Categories:\n      '
        count = 0
        rowCount = 0
        for c in ', '.join(stats['categories']):
            if count > 90 and rowCount > 4:
                content = content + '...'
                break
            if count > 95:
                if c == ' ' or c == ',':
                    content = content + c + '\n      '
                else:
                    content = content + c + '-\n      '
                    rowCount += 1
                count = 0
            else:
                content = content + c
                count += 1

        window.associatedStat.setText(content)
    else:
        window.amountStat.setText('Amount by store:')
        window.priceStat.setText('Price Statistics:')
        window.associatedStat.setText('Associated Categories:')

def runAppsQuery():

    names = []
    nameText = window.nameField.text()
    if nameText != '' and window.nameBox.isChecked():
        names = nameText.split(',')

    categories = []
    categoriesText = window.categoriesField.text()
    if categoriesText != '' and window.categoriesBox.isChecked():
        categories = categoriesText.split(',')

    gt = 0
    if window.appsRatingBox.isChecked():
        gt = 1
        if window.appsLtRadio.isChecked():
            gt = -1

    min_rating = 0
    ratingText = window.appsRatingField.text()
    if ratingText != '' and window.appsRatingBox.isChecked():
        min_rating = float(ratingText)

    sort = True
    orderBy = None
    orderText = window.appsOrderCombo.currentText()
    if orderText != 'none' and window.appsOrderBox.isChecked():
        orderBy = orderText
        if  window.appsHighLowRadio.isChecked():
            sort = False

    stats = []
    if window.statsBox.isChecked():
        stats.append('amounts')
        stats.append('categories')
        stats.append('prices')

    wrapper = MongoWrapper()

    buildTable(*wrapper.query(names, categories, gt, min_rating, orderBy, sort, stats, False))

def runReviewsQuery():

    names = []
    nameText = window.nameField.text()
    if nameText != '' and window.nameBox.isChecked():
        names = nameText.split(',')

    categories = []
    categoriesText = window.categoriesField.text()
    if categoriesText != '' and window.categoriesBox.isChecked():
        categories = categoriesText.split(',')

    gt = 0
    if window.appsRatingBox.isChecked():
        gt = 1
        if window.appsLtRadio.isChecked():
            gt = -1

    min_rating = 0
    ratingText = window.appsRatingField.text()
    if ratingText != '' and window.appsRatingBox.isChecked():
        min_rating = float(ratingText)

    stats = []
    if window.statsBox.isChecked():
        stats.append('amounts')
        stats.append('categories')
        stats.append('prices')

    wrapper = MongoWrapper()

    ids, stats = wrapper.query(names, categories, gt, min_rating, None, True, stats, True)

    sentiment = False
    sentimentType = 'Neutral'
    if window.sentimentBox.isChecked():
        sentiment = True
        if window.positiveRadio.isChecked():
            sentimentType = 'Positive'
        if window.negativeRadio.isChecked():
            sentimentType = 'Negative'

    sort = True
    orderBy = None
    orderText = window.reviewsOrderCombo.currentText()
    if orderText != 'none' and window.reviewsOrderBox.isChecked():
        orderBy = orderText
        if  window.reviewsHighLowRadio.isChecked():
            sort = False

    polarity = 0
    polarityValue = 0
    if window.polarityBox.isChecked():
        polarity = 1
        polarityValue = window.polarityField.text()
        if window.reviewsLtRadio.isChecked():
            polarity = -1

    wrapper = CassandraWrapper()

    buildTable(wrapper.query(ids['id'].values.tolist(), orderBy, sort, sentiment, sentimentType, polarity, polarityValue), stats)

if __name__ == "__main__":
    app = QApplication([])

    ui_file = QFile("/home/bonotto/Dropbox/Faculdade/2019-02/Gestao_de_BD/gui/demoari/mainwindow.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)

    window.appsRunButton.clicked.connect(runAppsQuery)
    window.reviewsRunButton.clicked.connect(runReviewsQuery)

    window.appsOrderCombo.addItem('none')
    window.appsOrderCombo.addItem('name')
    window.appsOrderCombo.addItem('categories')
    window.appsOrderCombo.addItem('rating')

    window.reviewsOrderCombo.addItem('none')
    window.reviewsOrderCombo.addItem('sentiment_polarity')

    window.appsGtRadio.setChecked(True)
    window.appsLowHighRadio.setChecked(True)
    window.reviewsLowHighRadio.setChecked(True)
    window.positiveRadio.setChecked(True)
    window.reviewsGtRadio.setChecked(True)

    window.show()

    sys.exit(app.exec_())
