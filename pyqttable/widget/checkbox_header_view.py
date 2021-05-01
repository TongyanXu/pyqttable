# -*- coding: utf-8 -*-
"""ComboBox with CheckBox on each row to support multi-selection"""

__all__ = ['CheckBoxVHeaderView']

from PyQt5 import QtCore, QtGui, QtWidgets


class CheckBoxVHeaderView(QtWidgets.QHeaderView):
    itemChecked = QtCore.pyqtSignal(int, bool)

    def __init__(self, parent: QtWidgets.QTableView = None):
        super().__init__(QtCore.Qt.Vertical, parent)
        self.setSectionsClickable(True)
        self.checkStates = []
        self.checkBoxes = []
        self.sectionCountChanged.connect(self.onSectionCountChanged)

        self._x_offset = 10
        self._width = 25
        self._height = 25

    def sizeHint(self):
        size = super().sizeHint()
        size.setWidth(size.width() + self._width + 2 * self._x_offset - 11)
        size.setHeight(size.height() + 13)
        return size

    @staticmethod
    def switchCheckState(option: QtWidgets.QStyleOptionButton):
        style = QtWidgets.QStyle
        if option.state & style.State_Off:
            option.state = style.State_Enabled | style.State_Active | style.State_On
        else:
            option.state = style.State_Enabled | style.State_Active | style.State_Off

    def paintSection(self, painter: QtGui.QPainter, rect: QtCore.QRect, logicalIndex: int):
        painter.save()
        super().paintSection(painter, rect, logicalIndex)
        painter.restore()

        _y_offset = (rect.height() - self._height) // 2

        option = self.checkBoxes[logicalIndex]
        option.rect = QtCore.QRect(rect.x() + rect.width() - self._width - self._x_offset,
                                   rect.y() + _y_offset, self._width, self._height)
        painter.save()
        self.style().drawControl(QtWidgets.QStyle.CE_CheckBox, option, painter)
        painter.restore()

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        option = self.checkBoxes[index]
        if option.rect.contains(event.pos()):
            self.checkStates[index] = not self.checkStates[index]
            self.switchCheckState(self.checkBoxes[index])
            self.updateSection(index)
            self.itemChecked.emit(index, self.checkStates[index])
        super().mousePressEvent(event)

    def onSectionCountChanged(self, oldCount: int,  newCount: int):
        if newCount > oldCount:
            for i in range(newCount - oldCount):
                self.checkStates.append(False)
                option = QtWidgets.QStyleOptionButton()
                self.switchCheckState(option)
                self.checkBoxes.append(option)
        else:
            self.checkStates = self.checkStates[0: newCount]
            self.checkBoxes = self.checkBoxes[0: newCount]


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    table = QtWidgets.QTableWidget()
    header = CheckBoxVHeaderView(table)
    table.setVerticalHeader(header)
    table.setColumnCount(1)
    table.setRowCount(10)
    table.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem('cao'))
    table.show()
    sys.exit(app.exec_())
