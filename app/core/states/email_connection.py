from aiogram.fsm.state import State, StatesGroup


class EmailAcc(StatesGroup):

    server = State()
    email = State()
    password = State()
