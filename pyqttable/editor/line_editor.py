# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['LineEditorFactory']

from .base import EditorFactory

from PyQt5 import QtWidgets, QtCore
from typing import NoReturn


class LineEditorFactory(EditorFactory):
    klass = QtWidgets.QLineEdit

    def create(self, parent: QtWidgets.QWidget = None) -> klass:
        return self.klass(parent)

    def set_data(self, editor: klass, data: str) -> NoReturn:
        editor.setText(data)
        editor.selectAll()

    def get_data(self, editor: klass) -> str:
        return editor.text()

    def done_signal(self, editor: klass) -> QtCore.pyqtSignal:
        return editor.editingFinished


if __name__ == '__main__':
    pass