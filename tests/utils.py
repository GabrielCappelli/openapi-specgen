from dataclasses import dataclass
from typing import List


@dataclass
class SimpleObject():
    str_field: str
    int_field: int
    float_field: float
    boolean_field: bool
    list_field: List
