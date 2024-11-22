from aiogram import Bot, Dispatcher, executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



api=('7876971454:AAEqQcBg_49V5wQXPu6d4jWz729ZXund1D4')
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = ReplyKeyboardMarkup()
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button1)
kb.add(button2)

@dp.message_handler(text='/start')
async def start(message):
    await message.answer('Необходимо ввести возраст, рост и вес!',reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def inform(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state= UserState.age)
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
    await message.answer('Этот бот является тестовым и его функционал будет усовершенствован😎')

@dp.message_handler()
async def all_massages(message):
    await message.answer('Жми👉/start, чтобы рассчитать необходимое количество калорий в сутки!')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)