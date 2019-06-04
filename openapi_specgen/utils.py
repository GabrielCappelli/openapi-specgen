from typing import List

OPENAPI_TYPE_MAP = {
    str: "string",
    float: "number",
    int: "integer",
    bool: "boolean",
    list: "array",
    List: "array",
    List[str]: "array",
    List[float]: "array",
    List[int]: "array",
    List[bool]: "array"
}

OPENAPI_ARRAY_ITEM_MAP = {
    List[str]: "string",
    List[float]: "number",
    List[int]: "integer",
    List[bool]: "boolean",
    List: None
}


def get_openapi_type(data_type: type) -> str:
    return OPENAPI_TYPE_MAP.get(data_type, "object")


def get_openapi_list_generic_type(data_type: type) -> str:
    return OPENAPI_ARRAY_ITEM_MAP.get(data_type)
