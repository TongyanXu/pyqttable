# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['SelectionEditorFactory', 'BoolEditorFactory']

from .base import EditorFactory

from PyQt5 import QtWidgets, QtCore
from typing import List, NoReturn


class SelectionEditorFactory(EditorFactory):
    klass = QtWidgets.QComboBox

    def __init__(self, selection: List[str]):
        self.selection = selection

    def create(self, parent: QtWidgets.QWidget = None) -> klass:
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(self.selection)
        return editor

    def set_data(self, editor: klass, data: str) -> NoReturn:
        index = self.selection.index(data)
        editor.setCurrentIndex(index)
        editor.showPopup()

    def get_data(self, editor: klass) -> str:
        return editor.currentText()

    def done_signal(self, editor: klass) -> QtCore.pyqtSignal:
        return editor.currentIndexChanged


class BoolEditorFactory(SelectionEditorFactory):

    def __init__(self):
        super().__init__(['True', 'False'])


if __name__ == '__main__':
    pass
