# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['TableHeader']

from .filter_cell import *
from .sorter import *

from PyQt5 import QtWidgets, QtCore
from pyqttable.column import Column
from typing import List, NoReturn


class TableHeader(QtWidgets.QTableWidget):
    sortingTriggered = QtCore.pyqtSignal(object)
    filterTriggered = QtCore.pyqtSignal(object)

    def __init__(self, parent: QtWidgets.QWidget, columns: List[Column], show_filter: bool = False):
        super().__init__(parent)
        self.columns = columns
        self.show_filter = show_filter
        self._sorter = HeaderSorter()
        self._filter = FilterManager()
        self._setup_basic()
        self._setup_header()
        self._setup_filter()
        self._setup_geometry()

    def _setup_basic(self) -> NoReturn:
        self.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem(''))
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def _setup_header(self) -> NoReturn:
        self.setColumnCount(len(self.columns))
        for j, col in enumerate(self.columns):
            item = self._sorter.item(col)
            self.setHorizontalHeaderItem(j, item)
        header = self.horizontalHeader()
        header.sectionClicked.connect(self._on_sorting)

    def _setup_filter(self) -> NoReturn:
        if self.show_filter:
            self.setRowCount(1)
            for j, col in enumerate(self.columns):
                cell = self._filter.cell(col)
                self.setCellWidget(0, j, cell)
            self._filter.filterUpdated.connect(self._on_filter)

    def _setup_geometry(self) -> NoReturn:
        head_height = self.horizontalHeader().height()
        if self.show_filter:
            head_height += self.rowHeight(0)
        self.setFixedHeight(head_height)

    def _on_sorting(self, index: int) -> NoReturn:
        sort_func = self._sorter.sort(self, index)
        self.sortingTriggered.emit(sort_func)

    def _on_filter(self) -> NoReturn:
        self.filterTriggered.emit(self._filter.filter)


if __name__ == '__main__':
    pass
