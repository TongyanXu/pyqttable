# -*- coding: utf-8 -*-
"""column style"""

__all__ = ['Style']

from .default import ValueFetcher
from PyQt5 import QtWidgets, QtGui
from typing import Union, Tuple


class Style:
    """
    Column style including:
    - font color
    - background color
    """

    def __init__(self, color: Union[str, Tuple[int], None] = None,
                 bg_color: Union[str, Tuple[int], None] = None):
        self.color = color
        self.bg_color = bg_color
        self._color = self._get_color(color)
        self._bg_color = self._get_color(bg_color)

    @staticmethod
    def _get_color(color):
        try:
            if isinstance(color, str):
                return QtGui.QColor(color)
            elif isinstance(color, tuple):
                return QtGui.QColor(*color)
        except Exception as e:
            _ = e
        return None

    @classmethod
    def make(cls, fetcher: ValueFetcher):
        """Make Style from ValueFetcher"""
        return cls(
            color=fetcher.get('color'),
            bg_color=fetcher.get('bg_color'),
        )

    def apply_to_item(self, item: QtWidgets.QTableWidgetItem):
        """Apply style to QTableWidgetItem"""
        if self.color:
            item.setForeground(self._color)
        if self.bg_color:
            item.setBackground(self._bg_color)

    def apply_to_widget(self, widget: QtWidgets.QWidget):
        """Apply style to QWidget"""
        palette = QtGui.QPalette()
        updated = False
        if self.color:
            palette.setColor(QtGui.QPalette.Foreground, self._color)
            updated = True
        if self.bg_color:
            palette.setColor(QtGui.QPalette.Background, self._bg_color)
            updated = True
        if updated:
            widget.setPalette(palette)


if __name__ == '__main__':
    pass
