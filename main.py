from aiogram import Bot, Dispatcher, executor, types
from cryptocost import *

token_api = '5150577399:AAFeaZI5iLT-hIAup8mcybkBiF4CkIw5mBs'

bot = Bot(token=token_api)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('ahahh')

@dp.message_handler() 
async def echo(message: types.Message): 
   a = message.text.lower().split(' ')
   price_usd = all_cryptos_usd()
   for i in range(len(a)):
       print(a[i], a[i-1])
       if a[i] in price_usd and is_number(a[i-1]):
           await message.reply(a[i-1] + ' ' +a[i].upper() + ' costs: \n' + str(get_price_usd([a[i]])*int(a[i-1])) + ' usd \n' + str(get_price_rub([a[i]])*int(a[i-1])) + ' rub')
       elif a[i] in price_usd:
           await message.reply('1 ' + a[i].upper()  + ' costs: \n' + str(get_price_usd([a[i]])) + ' usd  \n' + str(get_price_rub([a[i]])) + ' rub')


if __name__  == '__main__':
    executor.start_polling(dp, skip_updates=True)
