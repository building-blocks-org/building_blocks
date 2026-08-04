"""Classification of port types as abstract or concrete.

Used during ``__init_subclass__`` validation to skip abstract
intermediate classes such as ``UseCasePort`` or ``CommandHandlerPort``.
"""


class AbstractPortClassifier:
    """Determines whether a port class is abstract.

    Example:
        ```python
        class MyConcreteClass:
            def do_work(self) -> str: ...


        classifier = AbstractPortClassifier(MyConcreteClass)
        classifier.is_abstract()  # False (no abstract methods)
        ```
    """

    def __init__(self, cls: type) -> None:
        self._cls = cls

    def is_abstract(self) -> bool:
        """Return ``True`` when the class has unimplemented abstract methods.

        Checks ``__abstractmethods__`` first (populated after class creation).
        Falls back to scanning ``__dict__`` for ``__isabstractmethod__``
        attributes — needed during ``__init_subclass__`` when
        ``ABCMeta`` has not yet set ``__abstractmethods__``.
        """
        abstract_methods: frozenset[object] = getattr(self._cls, "__abstractmethods__", frozenset())
        if abstract_methods:
            return True
        for attr_value in self._cls.__dict__.values():
            if getattr(attr_value, "__isabstractmethod__", False):
                return True
        return False
