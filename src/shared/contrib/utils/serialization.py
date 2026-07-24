from typing import Any, Literal, assert_never, overload

import orjson  # fastest lib for json serialization on 2026.07.17


@overload
def json_dumps(data: Any) -> bytes: ...  # noqa: ANN401


@overload
def json_dumps(data: Any, mode: Literal["str"]) -> str: ...  # noqa: ANN401


@overload
def json_dumps(data: Any, mode: Literal["bytes"]) -> bytes: ...  # noqa: ANN401


def json_dumps(data: Any, mode: Literal["str", "bytes"] = "bytes") -> str | bytes:
    """Serialize a Python object to JSON

    Args:
        data (Dataclasses | dict| list| tuple| str| int| float| bool| None| datetime| UUID):
        dict key must be str

    Returns:
        JSON representation of the given object as UTF-8 encoded bytes or str.
    """  # noqa: E501
    match mode:
        case "str":
            return orjson.dumps(data).decode(encoding="utf-8")
        case "bytes":
            return orjson.dumps(data)
        case _:
            assert_never(mode)


def json_loads(data: bytes | str) -> dict | str | list | int:
    return orjson.loads(data)
