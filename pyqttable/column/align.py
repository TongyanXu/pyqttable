# -*- coding: utf-8 -*-
"""column content alignment"""

__all__ = ['Alignment']

from PyQt5 import QtCore, QtWidgets
from .default import ValueFetcher

_horizontal_flag = {
    'l':        QtCore.Qt.AlignLeft,
    'r':        QtCore.Qt.AlignRight,
    'c':        QtCore.Qt.AlignHCenter,
    'left':     QtCore.Qt.AlignLeft,
    'right':    QtCore.Qt.AlignRight,
    'center':   QtCore.Qt.AlignHCenter,
}
_vertical_flag = {
    't':        QtCore.Qt.AlignTop,
    'b':        QtCore.Qt.AlignBottom,
    'c':        QtCore.Qt.AlignVCenter,
    'top':      QtCore.Qt.AlignTop,
    'bottom':   QtCore.Qt.AlignBottom,
    'center':   QtCore.Qt.AlignVCenter,
}


class Alignment:
    """Column content alignment (both horizontal and vertical)"""

    def __init__(self, h_align: str = 'l', v_align: str = 'c'):
        self.h_align, self.v_align = h_align, v_align
        self._h_flag = _horizontal_flag.get(self.h_align, 'l')
        self._v_flag = _vertical_flag.get(self.v_align, 't')
        self._flag = self._h_flag | self._v_flag

    @classmethod
    def make(cls, fetcher: ValueFetcher):
        """Make Alignment from ValueFetcher"""
        return cls(
            h_align=fetcher.get('h_align'),
            v_align=fetcher.get('v_align'),
        )

    def apply_to_item(self, item: QtWidgets.QTableWidgetItem):
        """Apply alignment to QTableWidgetItem"""
        item.setTextAlignment(self._flag)

    def apply_to_widget(self, widget: QtWidgets.QWidget):
        """Apply alignment to QWidget"""
        style = widget.style()
        style.visualAlignment(QtCore.Qt.LeftToRight, self._flag)
        widget.setStyle(style)


if __name__ == '__main__':
    pass
