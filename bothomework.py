import logging
from config import API_TOKEN, WEBHOOK_HOST, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

API_TOKEN = API_TOKEN
WEBHOOK_HOST = WEBHOOK_HOST
WEBHOOK_PATH = WEBHOOK_PATH
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = WEBAPP_HOST
WEBAPP_PORT = WEBAPP_PORT

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def command_regexp_help(message: types.Message):
    await message.answer(f'<b>Привет</b>, {message.from_user.full_name}, <b>я обычный телеграм бот!</b> ')

@dp.message_handler(commands=['about'])
async def cmd_about(message: types.Message):
        await message.answer('Я пока ничего не умею.')

async def on_startup(dp):
   await bot.set_webhook(WEBHOOK_URL)
   # insert code here to run it after start

async def on_shutdown(dp):
   logging.warning('Shutting down..')
   # insert code here to run it before shutdown

   # Remove webhook (not acceptable in some cases)
   await bot.delete_webhook()

   # Close DB connection (if used)
   await dp.storage.close()
   await dp.storage.wait_closed()

   logging.warning('Bye!')

if __name__ == '__main__':
   start_webhook(
       dispatcher=dp,
       webhook_path=WEBHOOK_PATH,
       on_startup=on_startup,
       on_shutdown=on_shutdown,
       skip_updates=True,
       host=WEBAPP_HOST,
       port=WEBAPP_PORT,
   )
