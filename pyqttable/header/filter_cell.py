# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['FilterManager']

import pandas as pd

from PyQt5 import QtWidgets, QtCore
from pyqttable.column import *
from pyqttable.editor import *
from typing import NoReturn


class FilterManager(QtCore.QObject):
    filterUpdated = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._filter_cell = []  # column_key: (column, cell)

    def cell(self, column: Column) -> QtWidgets.QWidget:
        # if column.filter.type == filter_type.FilterType.Exact:
        #     factory = column.type.editor_factory
        # else:
        factory = LineEditorFactory()
        cell = factory.create()
        factory.done_signal(cell).connect(self._on_filter_update)
        self._filter_cell.append((column, factory, cell))
        return cell

    def _on_filter_update(self, *args) -> NoReturn:
        _ = args
        self.filterUpdated.emit()

    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        for column, factory, cell in self._filter_cell:
            value = factory.get_data(cell)
            if value:
                df = column.filter.filter(df, column.key, value, column.type.to_string)
        return df


if __name__ == '__main__':
    pass
