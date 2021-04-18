# -*- coding: utf-8 -*-
"""column filter"""

__all__ = ['Filter', 'FilterType']

import abc
import enum
import pandas as pd
import re

from .default import ValueFetcher
from .type import basic_column_type
from pyqttable import const
from typing import List, Optional, Any


class FilterType(enum.Enum):
    """Column filter type"""
    Exact = 'exact'
    Contain = 'contain'
    Regex = 'regex'
    Expression = 'expression'
    MultipleChoice = 'multiple_choice'


class Filter(metaclass=abc.ABCMeta):
    """
    Column filter, including:
    - filter type
    - filter widget info
    - filter function
    """

    # Placeholder text for filter widget
    PlaceHolderText = ''

    def __init__(self, filter_type):
        self.type = filter_type

    @classmethod
    def make(cls, fetcher: ValueFetcher):
        """Make Filter from ValueFetcher"""
        filter_type = fetcher.get('filter_type')

        # If filter_type is already Filter, just return
        if isinstance(filter_type, cls):
            return filter_type

        # Convert filter_type to enum
        try:
            filter_type = FilterType(filter_type)
        except Exception as e:
            _ = e
        else:
            # Make Filter instance according to FilterType
            if filter_type == FilterType.Exact:
                return ExactFilter(filter_type)
            elif filter_type == FilterType.Contain:
                return ContainFilter(filter_type)
            elif filter_type == FilterType.Regex:
                return RegexFilter(filter_type)
            elif filter_type == FilterType.Expression:
                return ExpressionFilter(filter_type)
            elif filter_type == FilterType.MultipleChoice:
                return MultipleChoice(filter_type)

        # If FilterType is invalid, raise error
        raise TypeError(f'invalid filter type \'{filter_type}\'')

    def filter(self, df: pd.DataFrame, by: str, filter_value: Any,
               to_string: Optional[callable] = None,
               to_value: Optional[callable] = None) -> pd.DataFrame:
        """
        Filter DataFrame

        Parameters
        ----------
        df: input DataFrame to be filtered
        by: column key to do filtering
        filter_value: current value passed by filter widget
        to_string: function to convert data from original format to string
        to_value: function to convert data from string to original format

        Returns
        -------
        Filtered DataFrame
        """
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
        """Common filter for all kinds of Filters"""
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
        """
        Method to filter each value

        Parameters
        ----------
        content: cell data to be filtered
        filter_value: current value passed by filter widget
        to_string: function to convert data from original format to string
        to_value: function to convert data from string to original format

        Returns
        -------
        Remain in result or not
        """
        ...


class ExactFilter(Filter):
    """Perfect match filter"""

    PlaceHolderText = 'Exact'

    def filter_each(self, content: Any, filter_value: Any,
                    to_string: Optional[callable],
                    to_value: Optional[callable]) -> bool:
        if isinstance(filter_value, str):
            return to_string(content) == filter_value
        else:
            return content == filter_value


class ContainFilter(Filter):
    """Contain filter"""

    PlaceHolderText = 'Contain'

    def filter_each(self, content: Any, filter_value: Any,
                    to_string: Optional[callable],
                    to_value: Optional[callable]) -> bool:
        if isinstance(filter_value, str):
            return to_string(content).find(filter_value) > -1
        else:
            return False


class RegexFilter(Filter):
    """Filtered by regex expression"""

    PlaceHolderText = 'Regex'

    def filter_each(self, content: Any, filter_value: Any,
                    to_string: Optional[callable],
                    to_value: Optional[callable]) -> bool:
        if isinstance(filter_value, str):
            return True if re.findall(filter_value, to_string(content)) else False
        else:
            return False


class ExpressionFilter(Filter):
    """Filtered by python expression"""

    PlaceHolderText = 'Express'

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
    """Filter with multiple choices"""

    PlaceHolderText = 'Multi'
    Delimiter = const.DefaultDelimiter

    def filter_each(self, content: str, filter_value: str,
                    to_string: Optional[callable],
                    to_value: Optional[callable]) -> bool:
        if isinstance(filter_value, str):
            filter_list = filter_value.split(self.Delimiter)
            return to_string(content) in filter_list
        else:
            return False


if __name__ == '__main__':
    pass
