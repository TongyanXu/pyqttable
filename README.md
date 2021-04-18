# pyqttable

A simple configurable table widget based on PyQt5 and pandas

## How to use
```
from pyqttable import PyQtTable

table_widget = PyQtTable(
    parent=None, 
    column_config=my_config,
    show_filter=True,
    sortable=True,
)
```

## Column Config
A list of configurations for each column

| Config Key | Description | Value Type | Default Value |
| --- | --- | --- | --- |
| key | key of column (used to access data from DataFrame) | str | # required |
| name | column name to display | str | # same as key |
| type | column value type (required for conversion between real value and string) | # see Column.Type | str |
| editable | controlling the cell value is read-only or not | bool | True |
| default | default value when key is missing in data (not recommended) | - | None |
| h_align | horizontal alignment | # see Column.Align | 'l' |
| v_align | vertical alignment | # see Column.Align | 'c' |
| selection | list of valid values | list | None |
| sort_lt |  DIY \_\_lt\_\_ methods for sorting (only effective when sortable is True) | # see Column.Sort | None |
| filter_type | filter type (only effective when show_filter is True) | # see Column.Filter | 'contain' |
| color | font color (in string or tuple indicating RGB) | # see Column.Color | None |
| bg_color | background color (same format as color) | # see Column.Color | None |

### Example
```
{
    'key': 'gender',                        # same as DataFrame column
    'name': 'Gender',                       # shown as table header
    'type': str,                            # string variable
    'editable': False,                      # read-only
    'selection': ['male', 'female'],        # could be either 'male' or 'female'
    'h_align': 'r',                         # align right
    'sort_lt': lambda x, y: x == 'female',  # 'female' < 'male'
    'filter_type': 'multiple_choice',       # multiple-choice filter
    'bg_color': (135, 206, 250)},           # blue opaque background
}
```

### Column.Type
Column type should be following class (not instance)

| Column type |
| --- |
| int |
| float |
| str |
| bool |
| datetime.datetime |
| datetime.date |
| datetime.time |

Column type can also be instance of ColumnType
Inherit from ColumnType to make DIY column type
Inherit from EditorFactory to make DIY editor for DIY column type (if required)
```
from pyqttable.column import type_
from pyqttable.editor import EditorFactory

class MyEditorFactory(EditorFactory):
    ...

class MyColumnType(type_.ColumnType):
    EditorFactory = MyEditorFactory()
    ...
```
 
### Column.Align

| Key | Valid value | Flag |
| --- | --- | --- |
| h_align | 'l' / 'left' | AlignLeft |
| h_align | 'r' / 'right' | AlignRight |
| h_align | 'c' / 'center' | AlignHCenter |
| v_align | 't' / 'top' | AlignTop |
| v_align | 'b' / 'bottom' | AlignBottom |
| v_align | 'c' / 'center' | AlignVCenter |

### Column.Color

| Value type | Value format |
| --- | --- |
| str | '#RRGGBB' |
| Tuple[int] | (R, G, B, Optional[T]) |

### Column.Filter
Column filter type should by following string

| Filter type |
| --- |
| 'exact' |
| 'contain' |  
| 'expression' |
| 'regex' |
| 'multiple_choice' |

Column filter type can also be instance of Filter
Inherit from Filter to make DIY filter type
```
from pyqttable.column import filter_

class MyFilterType(filter_.Filter):
    ...
```

### Column.Sort
Variable sort_lt should be a function with same signature as \_\_lt\_\_
When sort_lt is defined, sorting action will based on sort_lt instead of default \_\_lt\_\_

## How to set data
```
import pandas as pd
my_data = pd.DataFrame(...)
table_widget.set_data(my_data)
```

## How to get data
```
my_data = table_widget.get(data)
shown_data = table_widget.get(data, full=False)
```
