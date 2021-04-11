# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['TableBody']

import pandas as pd

from .cell import *
from .delegate import *

from PyQt5 import QtWidgets, QtCore
from pyqttable.column import Column
from typing import List, NoReturn


class TableBody(QtWidgets.QTableWidget):
    dataEdited = QtCore.pyqtSignal(int, object, object)

    def __init__(self, parent: QtWidgets.QWidget, columns: List[Column]):
        super().__init__(parent)
        self.columns = columns
        self._delegate_setter = DelegateSetter(self)
        self._data_change_lock = False
        self._setup_header()
        self._setup_delegate()
        self._setup_cell()

    def _setup_header(self) -> NoReturn:
        self.setColumnCount(len(self.columns))
        # for j, col in enumerate(self.columns):
        #     item = QtWidgets.QTableWidgetItem(col.key)
        #     self.setHorizontalHeaderItem(j, item)
        self.horizontalHeader().setVisible(False)

    def _setup_delegate(self) -> NoReturn:
        for j, col in enumerate(self.columns):
            item_delegate = self._delegate_setter.get_delegate(col)
            if item_delegate is not None:
                self.setItemDelegateForColumn(j, item_delegate)

    def _setup_cell(self):
        self.cellChanged.connect(self._on_cell_change)

    def display(self, data: pd.DataFrame) -> NoReturn:
        self._data_change_lock = True
        self.clearContents()
        self.setRowCount(len(data))
        records = data.to_dict('records')
        for i, row in enumerate(records):
            for j, col in enumerate(self.columns):
                cell_item = TableCell.from_row(row, col)
                self.setItem(i, j, cell_item)
        self._data_change_lock = False

    def _on_cell_change(self, row: int, col: int):
        if not self._data_change_lock:
            item = self.item(row, col)
            self.dataEdited.emit(row, item.column_cfg, item.value)


if __name__ == '__main__':
    pass
