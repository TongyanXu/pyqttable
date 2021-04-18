# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['ColumnType', 'DateColumnType', 'TimeColumnType', 'DateTimeColumnType', 'basic_column_type']

import abc
import datetime as dt

from .default import ValueFetcher

from pyqttable.editor import *

basic_column_type = [int, float, str, bool]


class ColumnType(metaclass=abc.ABCMeta):
    EditorFactory = LineEditorFactory()

    @classmethod
    def make(cls, fetcher: ValueFetcher):
        klass = fetcher.get('type')
        if isinstance(klass, cls):
            return klass
        elif klass in basic_column_type:
            return BasicColumnType.from_type(klass)
        elif klass in [dt.datetime, dt.date, dt.time]:
            return DateTimeColumnType.from_type(klass)
        else:
            raise TypeError(f'invalid type \'{klass}\'')

    def to_string(self, value):
        try:
            return self.to_str(value)
        except Exception as e:
            _ = e
            raise ValueError(
                f'[{self.__class__.__name__}] '
                f'cannot convert \'{value}\' to string'
            )

    def to_value(self, string):
        try:
            return self.to_val(string)
        except Exception as e:
            _ = e
            raise ValueError(
                f'[{self.__class__.__name__}] '
                f'cannot convert \'{string}\' to value'
            )

    @abc.abstractmethod
    def to_str(self, value):
        ...

    @abc.abstractmethod
    def to_val(self, string):
        ...


class BasicColumnType(ColumnType):

    def __init__(self, cls):
        self.cls = cls

    @classmethod
    def from_type(cls, klass):
        if klass in [int, float, str]:
            return cls(klass)
        elif klass in [bool]:
            return BoolColumnType(klass)
        else:
            raise TypeError(f'invalid type \'{klass}\'')

    def to_str(self, value):
        return str(value)

    def to_val(self, string):
        return self.cls(string)


class BoolColumnType(BasicColumnType):
    EditorFactory = BoolEditorFactory()

    def to_str(self, value):
        return 'True' if value else 'False'

    def to_val(self, string):
        return string == 'True'


class DateTimeColumnType(ColumnType):
    DtFormat = '%Y-%m-%d %H:%M:%S'
    EditorDtFormat = 'yyyy-MM-dd hh:mm:ss'
    EditorFactory = DateTimeEditorFactory(DtFormat, EditorDtFormat)

    def __init__(self, cls):
        self.cls = cls

    @classmethod
    def from_type(cls, klass):
        if klass == dt.datetime:
            return DateTimeColumnType(klass)
        elif klass == dt.date:
            return DateColumnType(klass)
        elif klass == dt.time:
            return TimeColumnType(klass)
        else:
            raise TypeError(f'invalid type \'{klass}\'')

    def to_str(self, value):
        assert isinstance(value, self.cls), \
            f'invalid {self.cls} given: \'{value}\''
        return value.strftime(self.DtFormat)

    def to_val(self, string):
        return dt.datetime.strptime(self.DtFormat, string)


class DateColumnType(DateTimeColumnType):
    DtFormat = '%Y-%m-%d'
    EditorDtFormat = 'yyyy-MM-dd'
    EditorFactory = DateEditorFactory(DtFormat, EditorDtFormat)

    def to_val(self, string):
        return super().to_val(string).date()


class TimeColumnType(DateTimeColumnType):
    DtFormat = '%H:%M:%S'
    EditorDtFormat = 'hh:mm:ss'
    EditorFactory = TimeEditorFactory(DtFormat, EditorDtFormat)

    def to_val(self, string):
        return super().to_val(string).time()


if __name__ == '__main__':
    pass
