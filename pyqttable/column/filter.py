# -*- coding: utf-8 -*-
"""doc string"""

__all__ = ['Filter', 'FilterType']

import abc
import enum
import pandas as pd

from .default import ValueFetcher
from .type import basic_column_type

from typing import List, Optional, Any


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

    def filter(self, df: pd.DataFrame, by: str, filter_value: Any,
               to_string: Optional[callable] = None,
               to_value: Optional[callable] = None) -> pd.DataFrame:
        kwargs = dict(filter_value=filter_value, to_string=to_string, to_value=to_value)
        return df[df[by].apply(self._filter_apply, **kwargs)].copy()

    def _filter_apply(self, content: Any, filter_value: Any,
                      to_string: Optional[callable],
                      to_value: Optional[callable]) -> bool:
        if self.common_filter(content, filter_value):
            return True
        try:
            return self.filter_each(content, filter_value, to_string, to_value)
        except Exception as e:
            _ = e
            return False

    @staticmethod
    def common_filter(content: Any, filter_value: Any) -> bool:
        if isinstance(filter_value, str):
            if filter_value == '#blank':
                return False if content else True
            elif filter_value == '#non-blank':
                return True if content else False
        return False

    @abc.abstractmethod
    def filter_each(self, content: Any, filter_value: Any,
                    to_string: Optional[callable],
                    to_value: Optional[callable]) -> bool:
        ...


class ExactFilter(Filter):

    def filter_each(self, content: Any, filter_value: Any,
                    to_string: Optional[callable],
                    to_value: Optional[callable]) -> bool:
        if isinstance(filter_value, str):
            return to_string(content) == filter_value
        else:
            return content == filter_value


class ContainFilter(Filter):

    def filter_each(self, content: Any, filter_value: Any,
                    to_string: Optional[callable],
                    to_value: Optional[callable]) -> bool:
        if isinstance(filter_value, str):
            return to_string(content).find(filter_value) > -1
        else:
            return False


class FuzzyFilter(Filter):

    def filter_each(self, content: Any, filter_value: Any,
                    to_string: Optional[callable],
                    to_value: Optional[callable]) -> bool:
        raise NotImplementedError


class ExpressionFilter(Filter):

    def filter_each(self, content: Any, filter_value: Any,
                    to_string: Optional[callable],
                    to_value: Optional[callable]) -> bool:
        if isinstance(filter_value, str):
            if not isinstance(content, tuple(basic_column_type)):
                content = to_string(content)
            expression = f'{content!r} {filter_value}'
            try:
                res = eval(expression)
            except Exception as e:
                _ = e
                return False
            else:
                return False if res is False else True
        else:
            return False


class MultipleChoice(Filter):

    def filter_each(self, content: str, filter_value: List[str],
                    to_string: Optional[callable],
                    to_value: Optional[callable]) -> bool:
        raise NotImplementedError


if __name__ == '__main__':
    pass
