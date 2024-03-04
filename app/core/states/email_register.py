from aiogram.fsm.state import State, StatesGroup


class EmailRegister(StatesGroup):

    server = State()
    email = State()
    password = State()
