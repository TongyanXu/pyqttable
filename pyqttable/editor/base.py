# -*- coding: utf-8 -*-
"""base editor factory"""

__all__ = ['EditorFactory']

import abc

from PyQt5 import QtWidgets, QtCore
from typing import NoReturn


class EditorFactory(metaclass=abc.ABCMeta):
    """
    EditorFactory metaclass to do following things:

    To create your own EditorFactory, following methods must be implemented:
    - create: create a new editor widget
    - set_data: set initial data to editor widget
    - get_data: get current data of editor widget
    - done_signal: get signal of editor widget's ending event
    - set_place_holder: set place holder text of editor widget

    For special usages, following methods can be implemented:
    - reset_editor: reset editor model for some reason
        * update filter model according to table data
    """

    # editor widget class
    klass = QtWidgets.QWidget

    @abc.abstractmethod
    def create(self, parent: QtWidgets.QWidget = None) -> klass:
        """
        Create a new editor widget

        Parameters
        ----------
        parent: parent widget of editor

        Returns
        -------
        editor widget
        """
        ...

    @abc.abstractmethod
    def set_data(self, editor: klass, data: str) -> NoReturn:
        """
        Set initial data to editor widget

        Parameters
        ----------
        editor: editor widget created by this factory
        data: data to be shown on editor widget
            * data should be string to cope with various usage
        """
        ...

    @abc.abstractmethod
    def get_data(self, editor: klass) -> str:
        """
        Get current data of editor widget

        Parameters
        ----------
        editor: editor widget created by this factory

        Returns
        -------
        data of editor widget
            * data should be string to cope with various usage
        """
        ...

    @abc.abstractmethod
    def done_signal(self, editor: klass) -> QtCore.pyqtSignal:
        """
        Get signal of editor widget's ending event
        Signal is typically an instance of pyqtSignal
            (with emit method to trigger)
        * Signal is not required to bring any value,
            (brought value will not be used by connected slots)

        Parameters
        ----------
        editor: editor widget created by this factory

        Returns
        -------
        editor ending signal:
        - editFinished for QLineEdit
        - currentIndexChanged for QComboBox
        - ...
        """
        ...

    @staticmethod
    @abc.abstractmethod
    def set_place_holder(editor: klass, text: str) -> NoReturn:
        """
        Set place holder text of editor widget
        * Default text displayed when editor is empty

        Parameters
        ----------
        editor: editor widget created by this factory
        text: place holder text
        """
        ...

    # def reset_editor(self, editor: klass, data: list) -> NoReturn:
    #     """
    #     Reset editor model for some reason
    #     * Optional method
    #
    #     Parameters
    #     ----------
    #     editor: editor widget created by this factory
    #     data: data to reset editor widget
    #     """
    #     ...


if __name__ == '__main__':
    pass
