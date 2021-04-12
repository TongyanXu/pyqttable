# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['HeaderSorter']

import pandas as pd

from PyQt5 import QtWidgets, QtCore
from pyqttable.column import *
from typing import NoReturn

_next_status = {
    sorter.SortStatus.Nothing: sorter.SortStatus.Ascending,
    sorter.SortStatus.Ascending: sorter.SortStatus.Descending,
    sorter.SortStatus.Descending: sorter.SortStatus.Nothing,
}

_sort_indicator = {
    sorter.SortStatus.Nothing: None,
    sorter.SortStatus.Ascending: QtCore.Qt.AscendingOrder,
    sorter.SortStatus.Descending: QtCore.Qt.DescendingOrder,
}


class SortableHeaderItem(QtWidgets.QTableWidgetItem):

    def __init__(self, column: Column):
        self.column_cfg = column
        super().__init__(self.column_cfg.name)
        self.status = sorter.SortStatus.Nothing

    @property
    def indicator(self) -> QtCore.Qt.SortOrder:
        return _sort_indicator[self.status]

    def update_status(self) -> NoReturn:
        self.status = _next_status[self.status]

    def reset_status(self) -> NoReturn:
        self.status = sorter.SortStatus.Nothing

    def sort(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.column_cfg.sorter.sort_data(
            df=df,
            by=self.column_cfg.key,
            status=self.status,
        )


class HeaderSorter:

    def __init__(self):
        self.sorting_item = None

    @classmethod
    def item(cls, column: Column) -> SortableHeaderItem:
        return SortableHeaderItem(column)

    def _update_sorting_item(self, item: SortableHeaderItem) -> NoReturn:
        if self.sorting_item != item and \
                self.sorting_item is not None:
            self.sorting_item.reset_status()
        self.sorting_item = item
        item.update_status()

    @staticmethod
    def _update_sorting_info(header: QtWidgets.QHeaderView, index: int,
                             indicator: QtCore.Qt.SortOrder) -> NoReturn:
        if indicator is not None:
            header.setSortIndicator(index, indicator)
            header.setSortIndicatorShown(True)
        else:
            header.setSortIndicatorShown(False)

    def sort(self, table: QtWidgets.QTableWidget, index: int) -> callable:
        header = table.horizontalHeader()
        item = table.horizontalHeaderItem(index)
        assert isinstance(item, SortableHeaderItem), \
            'header item not SortableHeaderItem'
        self._update_sorting_item(item)
        self._update_sorting_info(header, index, item.indicator)
        return item.sort


if __name__ == '__main__':
    pass
