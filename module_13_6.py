from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = ('')
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb_1 = InlineKeyboardMarkup(row_width=2)
kb_1.add(InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
       InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas'))

kb_2 = ReplyKeyboardMarkup()
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb_2.add(button1)
kb_2.add(button2)
start_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать'),
                                            KeyboardButton(text='Информация')]],
                                 resize_keyboard=True)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_1)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.message_handler(text='/start')
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=start_menu)


@dp.callback_query_handler(text='calories')
async def inform(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    await state.get_data()
    data = await state.get_data()
    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))
    kal_ = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваша норма калорий {kal_}.')
    await state.finish()

@dp.message_handler(text='Информация')
async def all_massages(message):
    await message.answer('Тестовый Бот')

@dp.message_handler()
async def all_massages(message):
    await message.answer('Жми👉/start, чтобы рассчитать необходимое количество калорий в сутки!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
