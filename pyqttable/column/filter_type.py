# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['Filter', 'FilterType']

import abc
import enum
import pandas as pd

from pyqttable.column.default import ValueFetcher
from typing import Union, List, Optional


class FilterType(enum.Enum):
    Exact = 'exact'
    Contain = 'contain'
    Fuzzy = 'fuzzy'
    Expression = 'expression'
    MultipleChoice = 'multiple_choice'


class Filter(metaclass=abc.ABCMeta):

    def __init__(self, filter_type):
        self.type = filter_type

    @classmethod
    def make(cls, fetcher: ValueFetcher):
        filter_type = fetcher.get('filter_type')
        try:
            filter_type = FilterType(filter_type)
        except Exception as e:
            _ = e
        else:
            if filter_type == FilterType.Exact:
                return ExactFilter(filter_type)
            elif filter_type == FilterType.Contain:
                return ContainFilter(filter_type)
            elif filter_type == FilterType.Fuzzy:
                return FuzzyFilter(filter_type)
            elif filter_type == FilterType.Expression:
                return ExpressionFilter(filter_type)
            elif filter_type == FilterType.MultipleChoice:
                return MultipleChoice(filter_type)
        raise TypeError(f'invalid filter type \'{filter_type}\'')

    def filter(self, df: pd.DataFrame, by: str, filter_value: Union[str, List[str]],
               convert_func: Optional[callable]):
        if convert_func:
            converted = df[by].apply(convert_func)
            by = f'{by}_filter_proxy'
            df = df.copy()
            df[by] = converted

        res = df[df[by].apply(self._filter_apply, filter_value=filter_value)].copy()

        if convert_func:
            res.drop(by, axis=1, inplace=True)

        return res

    def _filter_apply(self, content: str, filter_value: Union[str, List[str]]) -> bool:
        if self.common_filter(content, filter_value):
            return True
        try:
            return self.filter_each(content, filter_value)
        except Exception as e:
            _ = e
            return False

    @staticmethod
    def common_filter(content: str, filter_value: Union[str, List[str]]) -> bool:
        if isinstance(filter_value, str):
            if filter_value == '#blank':
                return False if content else True
            elif filter_value == '#non-blank':
                return True if content else False
        return False

    @abc.abstractmethod
    def filter_each(self, content: str, filter_value: Union[str, List[str]]) -> bool:
        ...


class ExactFilter(Filter):

    def filter_each(self, content: str, filter_value: str) -> bool:
        return content == filter_value


class ContainFilter(Filter):

    def filter_each(self, content: str, filter_value: str) -> bool:
        return content.find(filter_value) > -1


class FuzzyFilter(Filter):

    def filter_each(self, content: str, filter_value: str) -> bool:
        raise NotImplementedError


class ExpressionFilter(Filter):

    def filter_each(self, content: str, filter_value: str) -> bool:
        expression = f'{content!r}{filter_value}'
        res = eval(expression)
        return False if res is False else True


class MultipleChoice(Filter):

    def filter_each(self, content: str, filter_value: List[str]) -> bool:
        return content in filter_value


if __name__ == '__main__':
    pass
