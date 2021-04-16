# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['ComboCheckBox']

from PyQt5 import QtWidgets, QtCore, QtGui
from typing import List, NoReturn


class ComboCheckBox(QtWidgets.QComboBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # # Make the lineEdit the same color as QPushButton
        # palette = QtGui.QPalette()
        # palette.setBrush(QtGui.QPalette.Base, palette.button())
        # self.lineEdit().setPalette(palette)

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.update_text)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event: QtCore.QEvent.Resize) -> NoReturn:
        # Recompute text to elide as needed
        self.update_text()
        super().resizeEvent(event)

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:

        if obj == self.lineEdit():
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if obj == self.view().viewport():
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == QtCore.Qt.Checked:
                    item.setCheckState(QtCore.Qt.Unchecked)
                else:
                    item.setCheckState(QtCore.Qt.Checked)
                return True
        return False

    def showPopup(self) -> NoReturn:
        super().showPopup()
        # When the popup is displayed, a click on the lineEdit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self) -> NoReturn:
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.update_text()

    def timerEvent(self, event: QtCore.QEvent.Timer) -> NoReturn:
        # After timeout, kill timer, and re-enable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    @classmethod
    def data_to_text(cls, data: List[str]) -> str:
        return ', '.join(data)

    def update_text(self) -> NoReturn:
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == QtCore.Qt.Checked:
                texts.append(self.model().item(i).text())
        text = self.data_to_text(texts)

        # Compute elided text (with "...")
        metrics = QtGui.QFontMetrics(self.lineEdit().font())
        elided_text = metrics.elidedText(text, QtCore.Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elided_text)

    def addItem(self, text: str, data=None) -> NoReturn:
        item = QtGui.QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, p_str=None) -> NoReturn:
        for i, text in enumerate(texts):
            self.addItem(text, None)

    def setCurrentData(self, data: List[str]) -> NoReturn:
        for i in range(self.model().rowCount()):
            if self.model().item(i).data() in data:
                self.model().item(i).setCheckState(QtCore.Qt.Checked)

    def currentData(self, role=None) -> List[str]:
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == QtCore.Qt.Checked:
                res.append(self.model().item(i).data())
        return res


if __name__ == '__main__':
    pass
