from typing import Any, Callable, Type


def good_singleton(class_: Type) -> Callable[..., Any]:
    """
    Singleton decorator. If instance of class already exists, raises ValueError.
    It blocks creating new instances of classes that should instantiate only once.
    """
    instances: dict[Type, Any] = {}

    def getinstance(*args, **kwargs) -> Any:
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
            return instances[class_]
        raise ValueError(f"Instance of {class_} already exists")

    return getinstance
