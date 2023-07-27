import asyncio
import aiogram
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot('6029976465:AAEKx27Dgyx00knJBb2Q8lXitwqn9c8wHVI')
dp = Dispatcher(storage=MemoryStorage(), bot=bot)


class StateTest(StatesGroup):
    old = State()


@dp.message_handler(commands=['start'])
async def suggest_a(msg: aiogram.types.Message):
    await StateTest.old.set()
    await msg.reply('Сколько тебе лет?', reply_markup=aiogram.types.InlineKeyboardMarkup().add(aiogram.types.InlineKeyboardButton(callback_data='cancel_call', text='Отмена')))


@dp.message_handler(state=StateTest.old)
async def state_test_handler(msg: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    await msg.reply('Хорошо, понял')
    await state.finish()


@dp.callback_query_handler(lambda call: call.data == 'cancel_call', state=StateTest.old)
async def cancel_process(callback: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    await state.finish()
    await callback.answer('Отменяю.', show_alert=True)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
