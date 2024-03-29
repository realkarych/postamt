import types

from aiogram import Dispatcher

from app.exceptions.handler import RegisterHandlerError


def register(dp: Dispatcher, *handlers) -> None:
    """
    Register handlers. If `register()` wasn't implemented in module, it skips with error message.
    :param handlers: .py handler-modules with implemented register() method.
    :param dp: Dispatcher.
    """

    for handler in handlers:
        if isinstance(handler, types.ModuleType):
            try:
                dp.include_router(handler.register())
            except AttributeError as error:
                raise RegisterHandlerError(f"register() method wasn't implemented in {str(error.obj)}")
        else:
            raise RegisterHandlerError(f"`{handler}` from submitted args to `register()` is not a module")
