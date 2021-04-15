# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['FilterManager']

import pandas as pd

from PyQt5 import QtWidgets, QtCore
from pyqttable.column import *
from pyqttable.editor import *
from typing import NoReturn, Optional


class FilterManager(QtCore.QObject):
    filterUpdated = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._filter_editor = {}  # column_key: (column, cell)

    def editor(self, column: Column) -> QtWidgets.QWidget:
        if column.filter.type == filter.FilterType.MultipleChoice:
            factory = MultiChoiceEditorFactory(column.selection or [])
        else:
            factory = LineEditorFactory()
        return self._create_editor(column, factory)

    def update_editor(self, column: Column, df: pd.DataFrame) -> Optional[QtWidgets.QWidget]:
        _, factory, editor = self._filter_editor[column.key]
        if hasattr(factory, 'reset_editor'):
            new_selection = sorted(df[column.key].unique().tolist())
            factory.reset_editor(editor, new_selection)

    def _create_editor(self, column: Column, factory: EditorFactory) -> QtWidgets.QWidget:
        editor = factory.create()
        factory.done_signal(editor).connect(self._on_filter_update)
        self._filter_editor[column.key] = (column, factory, editor)
        return editor

    def _on_filter_update(self, *args) -> NoReturn:
        _ = args
        self.filterUpdated.emit()

    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        for key, (column, factory, cell) in self._filter_editor.items():
            value = factory.get_data(cell)
            if value:
                df = column.filter.filter(
                    df=df, by=key,
                    filter_value=value,
                    to_string=column.type.to_string,
                    to_value=column.type.to_value,
                )
        return df


if __name__ == '__main__':
    pass
