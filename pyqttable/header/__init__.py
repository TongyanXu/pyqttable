# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['TableHeader']

import pandas as pd

from .filter_cell import *
from .sorter import *

from PyQt5 import QtWidgets, QtCore
from pyqttable.column import ColumnGroup
from typing import NoReturn


class TableHeader(QtWidgets.QTableWidget):
    sortingTriggered = QtCore.pyqtSignal(object)
    filterTriggered = QtCore.pyqtSignal(object)

    def __init__(self, parent: QtWidgets.QWidget, col_group: ColumnGroup,
                 show_filter: bool = False, sortable: bool = False):
        super().__init__(parent)
        self._column_group = col_group
        self._show_filter = show_filter
        self._sortable = sortable
        self._sorter = HeaderSorter()
        self._filter = FilterManager()
        self._setup_basic()
        self._setup_header()
        self._setup_filter()
        self._setup_geometry()

    @property
    def show_filter(self) -> bool:
        return self._show_filter

    @property
    def sortable(self) -> bool:
        return self._sortable

    def _setup_basic(self) -> NoReturn:
        self.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem(''))
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def _setup_header(self) -> NoReturn:
        self.setColumnCount(len(self._column_group))
        for j, col in enumerate(self._column_group):
            item = self._sorter.item(col)
            self.setHorizontalHeaderItem(j, item)
        header = self.horizontalHeader()
        if self.sortable:
            header.sectionClicked.connect(self._on_sorting)

    def _setup_filter(self) -> NoReturn:
        if self.show_filter:
            self.setRowCount(1)
            for j, col in enumerate(self._column_group):
                cell = self._filter.editor(col)
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

    def update_filter(self, df: pd.DataFrame) -> NoReturn:
        header = self.horizontalHeader()
        for j in range(header.count()):
            item = self.horizontalHeaderItem(j)
            self._filter.update_editor(item.column_cfg, df)


if __name__ == '__main__':
    pass
