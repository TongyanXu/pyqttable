# -*- coding: utf-8 -*-
"""
PyQtTable - v0.0.1

copyright by Tongyan Xu
"""

__all__ = ['PyQtTable']

import pandas as pd

from . import header, body, column, utils
from PyQt5 import QtWidgets, QtCore
from typing import List, Dict, Any, Optional, NoReturn


class PyQtTable(QtWidgets.QWidget):
    """
    PyQtTable widget -

    methods:
    get_data(full) -> pd.DataFrame
    set_data(data)

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
        """
        super().__init__(parent)
        # Column configuration setup
        self._column_group = column.ColumnGroup(column_config)

        # Empty data
        self._data: pd.DataFrame = pd.DataFrame()
        self._shown_data: pd.DataFrame = pd.DataFrame()

        # Make header, body, and layout
        self._thead = header.TableHeader(self, self._column_group, show_filter, sortable)
        self._tbody = body.TableBody(self, self._column_group)
        self._layout = QtWidgets.QVBoxLayout(self)

        # Setup UI components
        self._setup_layout()
        self._setup_components()

    @utils.widget_error_signal
    def get_data(self, full: bool = True) -> pd.DataFrame:
        """
        Get table data

        Parameters
        ----------
        full: if True, all data (including hidden rows) will be returned
            if False, only currently shown rows will be returned
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
        self._thead.update_filter(self._data)
        self._display_data()

    def _setup_layout(self) -> NoReturn:
        self._layout.addWidget(self._thead)
        self._layout.addWidget(self._tbody)

        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._thead.setContentsMargins(0, 0, 0, 0)
        self._tbody.setContentsMargins(0, 0, 0, 0)

    def _setup_components(self) -> NoReturn:
        # Filter actions
        self._thead.filterTriggered.connect(self._filter_action)

        # Sorting actions
        self._thead.sortingTriggered.connect(self._sorting_action)

        # Data editing actions
        self._tbody.dataEdited.connect(self._update_data)

        # ScrollBars moving actions
        self._thead.horizontalScrollBar().valueChanged.connect(
            self._tbody.horizontalScrollBar().setValue
        )
        self._tbody.horizontalScrollBar().valueChanged.connect(
            self._thead.horizontalScrollBar().setValue
        )

    def _display_data(self) -> NoReturn:
        self._tbody.display(self._shown_data)

    @utils.widget_error_signal
    def _sorting_action(self, sort_func: callable):
        self._shown_data = sort_func(self._shown_data)
        self._display_data()

    @utils.widget_error_signal
    def _filter_action(self, filter_func: callable):
        self._shown_data = filter_func(self._data)
        self._display_data()

    @utils.widget_error_signal
    def _update_data(self, row_index: int, col: column.Column, value: Any):
        ori_index = self._shown_data.index[row_index]
        self._data.loc[ori_index, col.key] = \
            self._shown_data.loc[ori_index, col.key] = value


if __name__ == '__main__':
    pass
