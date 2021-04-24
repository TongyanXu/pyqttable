# -*- coding: utf-8 -*-
"""
PyQtTable - v0.0.2
A simple configurable table widget based on PyQt5 and pandas

copyright by Tongyan Xu
"""

__all__ = ['PyQtTable']

import pandas as pd

from . import column, delegate, header, utils
from PyQt5 import QtWidgets, QtCore
from typing import List, Dict, Any, Optional, NoReturn


class PyQtTable(QtWidgets.QTableWidget):
    """
    PyQtTable widget - subclass of QTableWidget

    methods:
    get_data(full) -> pd.DataFrame
    set_data(data)
    get_filter_data() -> Dict[str, str]

    signals:
    errorOccurred(Exception, traceback)
    """

    # when an error occurs, this signal will be emitted
    # connect you error handling functions if necessary
    errorOccurred = QtCore.pyqtSignal(object, object)

    def __init__(self,
                 parent: Optional[QtWidgets.QWidget] = None,
                 column_config: List[Dict[str, Any]] = None,
                 show_filter: bool = False,
                 sortable: bool = False,
                 draggable: bool = False,
                 ):
        """
        create a PyQtTable widget using column configurations

        Parameters
        ----------
        parent: parent widget (optional parameter)
        column_config: column configurations
            * should be a list of configurations for each column
                > [ config for column 1, config for column 2, ... ]
            * format of single configuration:
                dict(
                    key='staff_id',  # key of column (used to access data from DataFrame)
                    name='StaffID',  # column name to display
                    type=str,  # column value type (required for real value - string conversion)
                    editable=True,  # controlling the cell value is read-only or not
                    default=None,  # default value when key is missing in data (not recommended)
                    h_align='l',  # horizontal alignment
                    v_align='c',  # vertical alignment
                    selection=None,  # valid values
                    sort_lt=None,  # DIY __lt__ methods for sorting (only effective when sortable is True)
                    filter_type='contain',  # filter type (only effective when show_filter is True)
                    color=None,  # font color (string like '#000000' or tuple like (0, 0, 0, Optional[0]))
                    bg_color=None,  # background color (same format as color)
                )
        show_filter: show filter in header or not
        sortable: sorting is allowed or not
        draggable: column is draggable or not
        """
        super().__init__(parent)
        # Column configuration setup
        self._column_group = column.ColumnGroup(column_config)

        # Empty data
        self._data: pd.DataFrame = pd.DataFrame()
        self._shown_data: pd.DataFrame = pd.DataFrame()

        # Make header/delegate components
        self._header_manager = header.HeaderManager(self, self._column_group,
                                                    show_filter, sortable, draggable)
        self._delegate_setter = delegate.DelegateSetter(self)

        # Data change lock to distinguish manually change on UI and set_data
        self._lock = utils.NameLock()

        # Setup UI components
        self._setup_components()

    # ================================ Public Methods ================================

    @utils.widget_error_signal
    def get_data(self, full: bool = True) -> pd.DataFrame:
        """
        Get table data

        Parameters
        ----------
        full: if True, all data (including hidden rows) will be returned
            if False, only currently shown rows will be returned

        Returns
        -------
        Full or filtered data
        """
        return self._data.copy() if full else self._shown_data.copy()

    @utils.widget_error_signal
    def set_data(self, data: pd.DataFrame):
        """
        Set table data

        Parameters
        ----------
        data: DataFrame
            * attention: index of DataFrame will be reset
            * please do not save any information in index
        """
        df = data.reset_index(drop=True)
        self._data = self._shown_data = df
        self._header_manager.update_filter(self._data)
        self._display_data()

    def get_filter_data(self) -> Dict[str, str]:
        """
        Get table filter data

        Returns
        -------
        Dictionary of key - filter string
        """
        return self._header_manager.filter_value \
            if self._header_manager.show_filter else {}

    # ================================ Private Methods ================================

    def _setup_components(self) -> NoReturn:
        # Filter actions
        self._header_manager.filterTriggered.connect(self._filter_action)

        # Sorting actions
        self._header_manager.sortTriggered.connect(self._sort_action)

        # Data editing actions
        self.cellChanged.connect(self._update_data)

        # Customized delegate
        for j, col in enumerate(self._column_group):
            item_delegate = self._delegate_setter.get_delegate(col)
            if item_delegate is not None:
                self.setItemDelegateForColumn(j, item_delegate)

    def _display_data(self) -> NoReturn:
        with self._lock.get_lock('display_data'):
            self.clearContents()
            self.setRowCount(len(self._shown_data))
            records = self._shown_data.to_dict('records')
            for i, row in enumerate(records):
                for j, col in enumerate(self._column_group):
                    cell_item = TableCell.from_row(row, col)
                    self.setItem(i, j, cell_item)
            self._data_change_lock = False

    @utils.widget_error_signal
    def _sort_action(self, sort_func: callable):
        self._shown_data = sort_func(self._shown_data)
        self._display_data()

    @utils.widget_error_signal
    def _filter_action(self, filter_func: callable):
        filtered_data = filter_func(self._data)
        self._shown_data = self._header_manager.sort(filtered_data)
        self._display_data()

    @utils.widget_error_signal
    def _update_data(self, row: int, col: int):
        if not self._lock.get_lock('display_data'):
            item = self.item(row, col)
            assert isinstance(item, TableCell)
            column_cfg = item.column_cfg
            ori_index = self._shown_data.index[row]
            self._data.loc[ori_index, column_cfg.key] = \
                self._shown_data.loc[ori_index, column_cfg.key] = item.value


class TableCell(QtWidgets.QTableWidgetItem):

    def __init__(self, value: Any, column_cfg: column.Column):
        self.column_cfg = column_cfg
        display_value = self.column_cfg.type.to_string(value)
        super().__init__(display_value)
        if not self.column_cfg.editable:
            self.setFlags(self.flags() & ~ QtCore.Qt.ItemIsEditable)
        self.column_cfg.align.apply_to_item(self)
        self.column_cfg.style.apply_to_item(self)

    @classmethod
    def from_row(cls, row_data: pd.Series, column_cfg: column.Column):
        val = row_data.get(column_cfg.key, column_cfg.default)
        return cls(val, column_cfg)

    @property
    def value(self) -> Any:
        return self.column_cfg.type.to_value(self.text())


if __name__ == '__main__':
    pass
