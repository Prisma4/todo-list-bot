from aiogram.fsm.state import StatesGroup, State


class BotStates(StatesGroup):
    START = State()
    TASKS = State()
    ADD_TASK_CATEGORY = State()
    ADD_TASK_TEXT = State()
    ADD_TASK_SCHEDULE = State()
    ADD_CATEGORY = State()
    CREATE_TASK = State()
