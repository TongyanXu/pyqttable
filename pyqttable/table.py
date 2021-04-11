# -*- coding: utf-8 -*-
"""doc string"""

import pandas as pd

from PyQt5 import QtWidgets
from pyqttable.column import Column
from pyqttable.header import *
from pyqttable.body import *
from typing import (
    List, Dict, Any, Optional, NoReturn
)


class PyQtTable(QtWidgets.QWidget):

    def __init__(self,
                 parent: Optional[QtWidgets.QWidget],
                 column_config: List[Dict[str, Any]],
                 show_filter: bool = False,
                 ):
        super().__init__(parent)
        self.columns = [Column.from_cfg(cfg)
                        for cfg in column_config]
        self.show_filter = show_filter

        self._data: pd.DataFrame = pd.DataFrame()
        self._shown_data: pd.DataFrame = pd.DataFrame()

        self._thead = TableHeader(self, self.columns, show_filter)
        self._tbody = TableBody(self, self.columns)
        self._layout = QtWidgets.QVBoxLayout(self)

        self._setup_layout()
        self._setup_components()

    @property
    def data(self) -> pd.DataFrame:
        return self._data.copy()

    @property
    def shown_data(self) -> pd.DataFrame:
        return self._shown_data.copy()

    def _setup_layout(self) -> NoReturn:
        self._layout.addWidget(self._thead)
        self._layout.addWidget(self._tbody)

        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._thead.setContentsMargins(0, 0, 0, 0)
        self._tbody.setContentsMargins(0, 0, 0, 0)

    def _setup_components(self) -> NoReturn:

        # delegate = BoolDelegate(self, self.columns[3])
        # self._tbody.setItemDelegateForColumn(3, delegate)

        self._thead.sortingTriggered.connect(self._sorting_action)
        self._thead.filterTriggered.connect(self._filter_action)
        self._tbody.dataEdited.connect(self._update_data)

        # 表格表身联动
        self._thead.horizontalScrollBar().valueChanged.connect(
            self._tbody.horizontalScrollBar().setValue
        )
        self._tbody.horizontalScrollBar().valueChanged.connect(
            self._thead.horizontalScrollBar().setValue
        )

    def set_data(self, data: List[Dict[str, Any]]) -> NoReturn:
        self._data = self._shown_data = pd.DataFrame(data)
        self._display_data()

    def _display_data(self) -> NoReturn:
        self._tbody.display(self._shown_data)

    def _sorting_action(self, sort_func: callable) -> NoReturn:
        self._shown_data = sort_func(self._shown_data)
        self._display_data()

    def _filter_action(self, filter_func: callable) -> NoReturn:
        self._shown_data = filter_func(self._data)
        self._display_data()

    def _update_data(self, row_index: int, column: Column, value: Any) -> NoReturn:
        row = self._shown_data.iloc[row_index]
        ori_index = self._shown_data.index[row_index]
        self._data.loc[ori_index, column.key] = row.loc[column.key] = value
        print(self._data)


if __name__ == '__main__':
    pass
