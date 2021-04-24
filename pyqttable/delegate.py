# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['DelegateSetter']

from PyQt5 import QtWidgets, QtCore
from pyqttable.column import Column
from pyqttable.editor import *
from typing import Optional, NoReturn


class DelegateSetter:

    def __init__(self, parent: QtWidgets.QTableWidget):
        self._parent = parent

    @staticmethod
    def get_editor_factory(column: Column) -> Optional[EditorFactory]:
        if column.selection:
            str_selection = [column.type.to_string(each)
                             for each in column.selection]
            return SingleChoiceEditorFactory(str_selection)
        if column.type.EditorFactory is not None:
            return column.type.EditorFactory
        return None

    def get_delegate(self, column: Column) -> Optional[QtWidgets.QStyledItemDelegate]:
        editor_factory = self.get_editor_factory(column)
        if editor_factory:
            return EditorDelegate(self._parent, editor_factory)
        return None


class EditorDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent: QtWidgets.QWidget, editor_factory: EditorFactory):
        super().__init__(parent)
        self._editor_factory = editor_factory

    def editor_factory(self):
        return self._editor_factory

    def createEditor(self, parent: QtWidgets.QWidget, option: QtWidgets.QStyleOptionViewItem,
                     index: QtCore.QModelIndex) -> QtWidgets.QWidget:
        return self.editor_factory().create(parent)

    def setEditorData(self, editor: QtWidgets.QWidget, index: QtCore.QModelIndex) -> NoReturn:
        data = index.model().data(index)
        self.editor_factory().set_data(editor, data)

    def setModelData(self, editor: QtWidgets.QWidget, model: QtCore.QAbstractItemModel,
                     index: QtCore.QModelIndex) -> NoReturn:
        data = self.editor_factory().get_data(editor)
        model.setData(index, data)


if __name__ == '__main__':
    pass
