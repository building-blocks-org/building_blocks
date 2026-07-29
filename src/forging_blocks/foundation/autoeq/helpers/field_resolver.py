"""Field resolution logic shared by the auto_eq decorator."""

import dataclasses
from collections.abc import Sequence


class FieldResolver:
    """Resolves which field names contribute to ``__eq__`` for a class."""

    @staticmethod
    def resolve(
        class_: type[object],
        fields: Sequence[str] | None = None,
    ) -> list[str]:
        if fields is not None:
            return list(fields)

        if dataclasses.is_dataclass(class_):
            return [f.name for f in dataclasses.fields(class_)]

        slots = FieldResolver._collect_slots(class_)
        if slots:
            return sorted(slots)

        annotations = FieldResolver._collect_annotations(class_)
        if annotations:
            return sorted(annotations)

        msg = (
            f"Cannot determine eq fields for non-dataclass {class_.__name__}. "
            f"Pass fields= explicitly, e.g. @auto_eq(fields=['x', 'y'])."
        )
        raise TypeError(msg)

    @staticmethod
    def _collect_slots(class_: type[object]) -> set[str]:
        all_slots: set[str] = set()
        for cls in class_.__mro__:
            slots = getattr(cls, "__slots__", ())
            if isinstance(slots, str):
                slots = (slots,)
            for slot in slots:
                if not slot.startswith("__"):
                    all_slots.add(slot)
        return all_slots

    @classmethod
    def _collect_annotations(cls, class_: type[object]) -> set[str]:
        """Collect all ``__annotations__`` keys from *class_* and its MRO.

        Excludes dunder names (``__module__``, ``__qualname__``, etc.).
        """
        all_annotations: set[str] = set()
        for c in class_.__mro__:
            ann: dict[str, object] | None = getattr(c, "__annotations__", None)
            if ann is not None:
                for key in ann:
                    if not key.startswith("__"):
                        all_annotations.add(key)
        return all_annotations
