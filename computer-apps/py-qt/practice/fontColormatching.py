import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, QSortFilterProxyModel, QStringListModel
from PyQt5.QtGui import QIcon, QFont
import pandas as pd
from pandas import DataFrame

class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))


    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)
        self.centerOnScreen()
        self.combo = ExtendedComboBox(self)
        self.my_list = ['','Option 1', 'Option 2', 'Option 3','Option 4', 'Option 5']
        self.combo.addItems(self.my_list)
        Data = {'Option Number': ['Option 2','Option 3','Option 5'],'Color': ['red','blue','grey']}
        df = DataFrame(Data,columns= ['Option Number', 'Color'])

        self.combo.setFixedWidth(250)

        print(df)

        def combo_changed():
            for color in ('red', 'blue', 'grey'):
                try:
                    if color == df.loc[df['Option Number'].str.contains(self.combo.currentText()), 'Color'].iloc[0]:
                        self.combo.setStyleSheet("QComboBox:editable{{ color: {} }}".format(color))
                except IndexError:
                    self.combo.setStyleSheet("QComboBox:editable{{ color: {} }}".format('black'))

        self.combo.currentIndexChanged.connect(combo_changed)

    def centerOnScreen (self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())