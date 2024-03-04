from aiogram.fsm.state import State, StatesGroup


class BaseMenu(StatesGroup):

    register_email = State()
