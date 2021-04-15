# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['TableCell']

import pandas as pd

from PyQt5 import QtWidgets
from pyqttable.column import Column
from typing import Any


class TableCell(QtWidgets.QTableWidgetItem):

    def __init__(self, value: Any, column: Column):
        self.column_cfg = column
        display_value = self.column_cfg.type.to_string(value)
        super().__init__(display_value)
        self.column_cfg.align.apply_to_item(self)
        self.column_cfg.style.apply_to_item(self)

    @classmethod
    def from_row(cls, row_data: pd.Series, column: Column):
        val = row_data.get(column.key, column.default)
        return cls(val, column)

    @property
    def value(self) -> Any:
        return self.column_cfg.type.to_value(self.text())


if __name__ == '__main__':
    pass
