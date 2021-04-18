# -*- coding: utf-8 -*-
"""selection related editor factory"""

__all__ = ['BoolEditorFactory', 'SingleChoiceEditorFactory', 'MultiChoiceEditorFactory']

from .base import EditorFactory

from PyQt5 import QtWidgets, QtCore
from pyqttable.widget import ComboCheckBox
from typing import List, NoReturn


class SingleChoiceEditorFactory(EditorFactory):
    """Factory of QComboBox for single selection"""

    klass = QtWidgets.QComboBox

    def __init__(self, selection: List[str]):
        self.selection = selection

    def create(self, parent: QtWidgets.QWidget = None) -> klass:
        editor = self.klass(parent)
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

    @staticmethod
    def set_place_holder(editor: klass, text: str) -> NoReturn:
        editor.lineEdit().setPlaceholderText(text)


class BoolEditorFactory(SingleChoiceEditorFactory):
    """Factory for boolean editor"""

    def __init__(self):
        super().__init__(['True', 'False'])


class MultiChoiceEditorFactory(SingleChoiceEditorFactory):
    """Factory of ComboCheckBox for multiple selections"""

    klass = ComboCheckBox

    def set_data(self, editor: klass, data: str) -> NoReturn:
        data_list = editor.text_to_data(data)
        editor.setCurrentData(data_list)
        editor.showPopup()

    def get_data(self, editor: klass) -> str:
        data_list = editor.currentData()
        return editor.data_to_text(data_list)

    def done_signal(self, editor: klass) -> QtCore.pyqtSignal:
        return editor.editTextChanged

    def reset_editor(self, editor: klass, data: list) -> NoReturn:
        if not self.selection:
            model = editor.model()
            model.removeRows(0, model.rowCount())
            editor.addItems(data)


if __name__ == '__main__':
    pass
