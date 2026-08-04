"""The `auto_hash` decorator generates `__hash__` for class instances.

Does **not** generate ``__eq__`` or apply ``auto_freeze``. Combine with
`auto_eq` for explicit equality,
and `auto_freeze` for immutability.

## Usage

=== "Bare decorator"
    ```python
    from forging_blocks.foundation.autohash import auto_hash

    @auto_hash
    class Point2D:
        __slots__ = ("x", "y")

        def __init__(self, x: float, y: float) -> None:
            self.x = x
            self.y = y

    p1 = Point2D(1.0, 2.0)
    p2 = Point2D(1.0, 2.0)
    assert hash(p1) == hash(p2)
    ```

=== "With parameters"
    ```python
    from forging_blocks.foundation.autohash import auto_hash

    @auto_hash(fields=["id"])
    class Record:
        __slots__ = ("id", "data")

        def __init__(self, id: str, data: str) -> None:
            self.id = id
            self.data = data

    r1 = Record("abc", "payload-a")
    r2 = Record("abc", "payload-b")
    assert hash(r1) == hash(r2)

## Generated members

|Member|Description|
|---|---|
|`__hash__`|Hash computed from the selected fields (mutable values converted to hashable equivalents)|
|`__auto_hash_fields__`|Tuple of field names used in hashing|
