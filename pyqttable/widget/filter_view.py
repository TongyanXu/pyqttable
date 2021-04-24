# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['FilterHeader']

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from typing import List, NoReturn


class FilterHeader(QtWidgets.QHeaderView):
    filterActivated = QtCore.pyqtSignal()

    def __init__(self, parent: QtWidgets.QTableWidget, padding: int = 0):
        super().__init__(QtCore.Qt.Horizontal, parent)
        self._filters = []
        self._padding = padding
        self.setStretchLastSection(True)
        self.setSectionsClickable(True)
        self.sectionResized.connect(self.adjustPositions)
        self.sectionMoved.connect(self.adjustPositions)
        parent.horizontalScrollBar().valueChanged.connect(self.adjustPositions)

    @property
    def filters(self) -> List[QtWidgets.QWidget]:
        return self._filters

    @filters.setter
    def filters(self, filter_widgets: List[QtWidgets.QWidget]) -> NoReturn:
        while self._filters:
            editor = self._filters.pop()
            editor.deleteLater()
        self._filters = [i for i in filter_widgets]
        self.adjustPositions()

    def setFilterBoxes(self, count: int) -> NoReturn:
        filter_widgets = []
        for index in range(count):
            editor = QtWidgets.QLineEdit(self.parent())
            editor.setPlaceholderText(f'Filter{index}')
            editor.returnPressed.connect(self.filterActivated.emit)
            filter_widgets.append(editor)
        self.filters = filter_widgets

    def sizeHint(self) -> QtCore.QSize:
        size = super().sizeHint()
        if self._filters:
            height = self._filters[0].sizeHint().height()
            size.setHeight(size.height() + height + self._padding)
        return size

    def updateGeometries(self) -> NoReturn:
        if self._filters:
            height = self._filters[0].sizeHint().height()
            self.setViewportMargins(0, 0, 0, height + self._padding)
        else:
            self.setViewportMargins(0, 0, 0, 0)
        super().updateGeometries()
        self.adjustPositions()

    def adjustPositions(self) -> NoReturn:
        offset = self.parent().verticalHeader().width()
        for index, editor in enumerate(self._filters):
            height = editor.sizeHint().height()
            editor.move(
                self.sectionPosition(index) - self.offset() + offset + 1,
                height + (self._padding // 2) + 11)
            editor.resize(self.sectionSize(index), height)

    def filterText(self, index: int) -> str:
        if 0 <= index < len(self._filters):
            return self._filters[index].text()
        return ''

    def setFilterText(self, index: int, text: str) -> NoReturn:
        if 0 <= index < len(self._filters):
            self._filters[index].setText(text)

    def clearFilters(self) -> NoReturn:
        for editor in self._filters:
            editor.clear()


if __name__ == '__main__':
    class Window(QtWidgets.QWidget):
        def __init__(self):
            super(Window, self).__init__()
            self.view = QtWidgets.QTableView()
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(self.view)
            header = FilterHeader(self.view)
            self.view.setHorizontalHeader(header)
            model = QtGui.QStandardItemModel(self.view)
            model.setHorizontalHeaderLabels('One Two Three Four Five'.split())
            self.view.setModel(model)
            header.setFilterBoxes(4)
            header.filterActivated.connect(self.handleFilterActivated)

        def handleFilterActivated(self):
            header = self.view.horizontalHeader()
            for index in range(header.count()):
                print((index, header.filterText(index)))

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(600, 100, 600, 300)
    window.show()
    sys.exit(app.exec_())
