from aiogram.fsm.state import State, StatesGroup

class StateAddAddress(StatesGroup):
	address = State()
