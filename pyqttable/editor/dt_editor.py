# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['DateTimeEditorFactory', 'DateEditorFactory', 'TimeEditorFactory']

import datetime as dt

from .base import EditorFactory

from PyQt5 import QtWidgets, QtCore
from typing import NoReturn


class DateTimeEditorFactory(EditorFactory):
    klass = QtWidgets.QDateTimeEdit

    def __init__(self, value_format: str, display_format: str):
        self.value_format = value_format
        self.display_format = display_format

    def create(self, parent: QtWidgets.QWidget = None) -> klass:
        editor = self.klass(parent)
        editor.setDisplayFormat(self.display_format)
        return editor

    def set_data(self, editor: klass, data: str) -> NoReturn:
        datetime = dt.datetime.strptime(data, self.value_format)
        editor.setDateTime(datetime)
        editor.setCalendarPopup(True)

    def get_data(self, editor: klass) -> str:
        datetime = editor.dateTime().toPyDateTime()
        return datetime.strftime(self.value_format)

    def done_signal(self, editor: klass) -> QtCore.pyqtSignal:
        return editor.editingFinished


class DateEditorFactory(DateTimeEditorFactory):
    klass = QtWidgets.QDateEdit

    def set_data(self, editor: klass, data: str) -> NoReturn:
        datetime = dt.datetime.strptime(data, self.value_format)
        editor.setDate(datetime.date())
        editor.setCalendarPopup(True)

    def get_data(self, editor: klass) -> str:
        date = editor.date().toPyDate()
        return date.strftime(self.value_format)


class TimeEditorFactory(DateTimeEditorFactory):
    klass = QtWidgets.QTimeEdit

    def set_data(self, editor: klass, data: str) -> NoReturn:
        datetime = dt.datetime.strptime(data, self.value_format)
        editor.setTime(datetime.time())

    def get_data(self, editor: klass) -> str:
        time = editor.time().toPyTime()
        return time.strftime(self.value_format)


if __name__ == '__main__':
    pass
