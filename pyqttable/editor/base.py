# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['EditorFactory']

import abc

from PyQt5 import QtWidgets, QtCore
from typing import NoReturn


class EditorFactory(metaclass=abc.ABCMeta):
    klass = QtWidgets.QWidget

    @abc.abstractmethod
    def create(self, parent: QtWidgets.QWidget = None) -> klass:
        ...

    @abc.abstractmethod
    def set_data(self, editor: klass, data: str) -> NoReturn:
        ...

    @abc.abstractmethod
    def get_data(self, editor: klass) -> str:
        ...

    @abc.abstractmethod
    def done_signal(self, editor: klass) -> QtCore.pyqtSignal:
        ...

    @staticmethod
    @abc.abstractmethod
    def set_place_holder(editor: klass, text: str) -> NoReturn:
        ...


if __name__ == '__main__':
    pass
