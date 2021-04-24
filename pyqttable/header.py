# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['HeaderManager']

import pandas as pd

from PyQt5 import QtCore, QtWidgets, QtGui
from pyqttable.column import *
from pyqttable.editor import *
from pyqttable.widget import *
from typing import Dict, NoReturn


class NormalHeaderView(QtWidgets.QHeaderView):
    sectionRightClicked = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStretchLastSection(True)
        self.setSectionsClickable(True)

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> NoReturn:
        if e.button() == QtCore.Qt.RightButton:
            index = self.logicalIndexAt(e.pos())
            self.sectionRightClicked.emit(index)
        super().mouseReleaseEvent(e)


class FilterHeaderView(FilterHeader):
    sectionRightClicked = QtCore.pyqtSignal(int)

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> NoReturn:
        if e.button() == QtCore.Qt.RightButton:
            index = self.logicalIndexAt(e.pos())
            self.sectionRightClicked.emit(index)
        super().mouseReleaseEvent(e)


class HeaderViewItem(QtWidgets.QTableWidgetItem):

    def __init__(self, column: Column):
        self.column_cfg = column
        super().__init__(self.column_cfg.name)

        self._sort_status = sorter.SortStatus.Nothing

    # ================================ Sort Part ================================

    @property
    def sort_status(self) -> sorter.SortStatus:
        return self._sort_status

    @property
    def sort_indicator(self) -> QtCore.Qt.SortOrder:
        return _sort_indicator[self._sort_status]

    def update_sort_status(self) -> NoReturn:
        self._sort_status = _next_status[self._sort_status]

    def reset_sort_status(self) -> NoReturn:
        self._sort_status = sorter.SortStatus.Nothing

    def sort(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.column_cfg.sorter.sort_data(
            df=df,
            by=self.column_cfg.key,
            status=self._sort_status,
        )


class HeaderManager(QtCore.QObject):
    filterTriggered = QtCore.pyqtSignal(object)
    sortTriggered = QtCore.pyqtSignal(object)

    def __init__(self, parent: QtWidgets.QTableWidget, col_group: ColumnGroup,
                 show_filter: bool = False, sortable: bool = False, draggable: bool = False):
        super().__init__(parent)
        self._parent = parent
        self._column_group = col_group
        self._show_filter = show_filter
        self._sortable = sortable
        self._draggable = draggable

        self._filter_editor = {}
        self._curr_sorting_on = None

        self._setup_ui()

    # ================================ Public Methods ================================

    @property
    def show_filter(self) -> bool:
        return self._show_filter

    @property
    def sortable(self) -> bool:
        return self._sortable

    @property
    def draggable(self) -> bool:
        return self._draggable

    @property
    def filter_value(self) -> Dict[str, str]:
        filter_dict = {}
        for key, (column, factory, cell) in self._filter_editor.items():
            value = factory.get_data(cell)
            if value != '':
                filter_dict[key] = value
        return filter_dict

    # ================================ Setup Part ================================

    def _setup_ui(self) -> NoReturn:
        # If show filter, replace horizontal header to FilterHeader
        if self.show_filter:
            header = FilterHeaderView(self._parent)
        else:
            header = NormalHeaderView(self._parent)
        self._parent.setHorizontalHeader(header)

        # Set horizontal header items one by one
        self._parent.setColumnCount(len(self._column_group))
        filter_widgets = []  # List of filter widgets for FilterHeader
        for j, col in enumerate(self._column_group):
            self._parent.setHorizontalHeaderItem(j, HeaderViewItem(col))
            # If show filter, make filter widgets
            if self.show_filter:
                filter_widgets.append(self._create_filter_editor(col))

        # If show filter, set list of filter widgets to FilterHeader
        if self.show_filter:
            header.filters = filter_widgets

        # If sortable, connect sorting signal to sorting slot
        if self.sortable:
            header.sectionRightClicked.connect(self._on_sorting)

        # If draggable, set header movable
        header.setSectionsMovable(self.draggable)

    # ================================ Filter Part ================================

    def _create_filter_editor(self, column: Column) -> QtWidgets.QWidget:
        # For MultipleChoice filters, use MultiChoiceEditorFactory to create editors
        if column.filter.type == filter_.FilterType.MultipleChoice:
            column_selection = column.selection or []
            str_selection = [column.type.to_string(each)
                             for each in column_selection]
            factory = MultiChoiceEditorFactory(str_selection)
        # For other filters, use LineEditorFactory to create editors
        else:
            factory = LineEditorFactory()

        # Create editor and do basic setup for filter editors
        editor = factory.create(self._parent)
        factory.done_signal(editor).connect(self._on_filter)
        factory.set_place_holder(editor, column.filter.PlaceHolderText)
        self._filter_editor[column.key] = (column, factory, editor)
        return editor

    def _reload_filter_editor(self, column: Column, df: pd.DataFrame) -> NoReturn:
        # Reload filter widgets if they can be updated by table data
        _, factory, editor = self._filter_editor[column.key]
        if hasattr(factory, 'reset_editor'):
            new_selection = sorted(df[column.key].apply(column.type.to_string).unique().tolist())
            factory.reset_editor(editor, new_selection)

    def _do_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        # Filter the DataFrame
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

    def _on_filter(self) -> NoReturn:
        """
        When editing of filter widgets is done, emit filterTriggered signal to parent QTableWidget,
            with filter function which takes an original DataFrame and returns a filtered DataFrame
        """
        self.filterTriggered.emit(self._do_filter)

    def update_filter(self, df: pd.DataFrame) -> NoReturn:
        header = self._parent.horizontalHeader()
        for j in range(header.count()):
            item = self._parent.horizontalHeaderItem(j)
            assert isinstance(item, HeaderViewItem), \
                'Header item not HeaderViewItem'
            self._reload_filter_editor(item.column_cfg, df)

    # ================================ Sort Part ================================

    def _update_sort_item(self, item: HeaderViewItem) -> NoReturn:
        # Update sorting status of HeaderViewItems
        if self._curr_sorting_on != item and \
                self._curr_sorting_on is not None:
            self._curr_sorting_on.reset_sort_status()
        self._curr_sorting_on = item
        item.update_sort_status()

    @staticmethod
    def _update_sort_info(header: QtWidgets.QHeaderView, index: int,
                          indicator: QtCore.Qt.SortOrder) -> NoReturn:
        # Update header's sorting indicator according to sorting status
        if indicator is not None:
            header.setSortIndicator(index, indicator)
            header.setSortIndicatorShown(True)
        else:
            header.setSortIndicatorShown(False)

    def sort(self, df: pd.DataFrame) -> pd.DataFrame:
        # Sort DataFrame by current sorting item
        if self._curr_sorting_on is not None:
            return self._curr_sorting_on.sort(df)
        else:
            return df

    def _on_sorting(self, index: int) -> NoReturn:
        """
        When sortable header section is clicked, emit sortTriggered signal to parent QTableWidget,
            with sorting function which takes an original DataFrame and returns a sorted DataFrame
        """
        # Update sorting item
        item = self._parent.horizontalHeaderItem(index)
        assert isinstance(item, HeaderViewItem), \
            'Header item not HeaderViewItem'
        self._update_sort_item(item)
        self._update_sort_info(self._parent.horizontalHeader(),
                               index, item.sort_indicator)
        self.sortTriggered.emit(self.sort)


_next_status = {
    sorter.SortStatus.Nothing: sorter.SortStatus.Ascending,
    sorter.SortStatus.Ascending: sorter.SortStatus.Descending,
    sorter.SortStatus.Descending: sorter.SortStatus.Nothing,
}

_sort_indicator = {
    sorter.SortStatus.Nothing: None,
    sorter.SortStatus.Ascending: QtCore.Qt.AscendingOrder,
    sorter.SortStatus.Descending: QtCore.Qt.DescendingOrder,
}


if __name__ == '__main__':
    pass
