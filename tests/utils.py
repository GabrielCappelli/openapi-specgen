from dataclasses import dataclass
from datetime import date, datetime
from typing import List

from marshmallow import Schema, fields


@dataclass
class DataclassObject():
    str_field: str
    int_field: int
    float_field: float
    boolean_field: bool
    list_field: List
    date_field: date
    datetime_field: datetime


@dataclass
class DataclassNestedObject():
    str_field: str
    nested_object: DataclassObject


class MarshmallowSchema(Schema):
    str_field = fields.String(required=True)
    int_field = fields.Integer()
    float_field = fields.Float()
    boolean_field = fields.Boolean()
    list_field = fields.List(fields.String())
    date_field = fields.Date()
    datetime_field = fields.DateTime()


class MarshmallowNestedSchema(Schema):
    str_field = fields.String(required=True)
    int_field = fields.Integer()
    float_field = fields.Float()
    boolean_field = fields.Boolean()
    list_field = fields.List(fields.String())
    nested_schema = fields.Nested('MarshmallowSchema')
    self_reference = fields.Nested('MarshmallowNestedSchema')
