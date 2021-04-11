# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['error_handler', 'widget_error_handler']

import functools as ft
import traceback as tb
from PyQt5 import QtWidgets


def error_handler(func):
    @ft.wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            _ = e
            tb.print_exc()
        else:
            return res
    return wrapped_func


def widget_error_handler(error_msg):
    def method_decorator(method):
        @ft.wraps(method)
        def wrapped_method(widget, *args, **kwargs):
            try:
                res = method(widget, *args, **kwargs)
            except Exception as e:
                _ = e
                tb.print_exc()
                dlg = QtWidgets.QErrorMessage(widget)
                dlg.showMessage(error_msg)
            else:
                return res
        return wrapped_method
    return method_decorator


if __name__ == '__main__':
    pass
