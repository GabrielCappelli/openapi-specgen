from dataclasses import dataclass
from typing import List


@dataclass
class DataclassObject():
    str_field: str
    int_field: int
    float_field: float
    boolean_field: bool
    list_field: List


@dataclass
class DataclassNestedObject():
    str_field: str
    nested_object: DataclassObject
