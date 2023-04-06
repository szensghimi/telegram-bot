import ccxt
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor



# ccxt 
exchange = ccxt.bitfinex2()
markets = exchange.load_markets()
coins_dict = [market.split('/')[0] for market in markets if 'USD' in market]

# is_number? func
def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

# telegramm bot api
bot = Bot(token="6073849398:AAGgNFOioyZVB62Fo-2AdFOl1M-f4PARbW4", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.callback_query_handler(text="delete")
async def test_call(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

#калькулятор выражений 
@dp.message_handler(commands=['calc'])
async def image(message: types.Message):
    a = message.text.lower()[6:]
    await message.reply(eval(a))


# start command
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=f"Привет! Я криптобот, который всегда готов тебе сообщить текущий курс криптовалюты.\n\n"
    f"Чтобы пользоваться мной просто напиши BTC, SOL, 10 ETH или другой тег.\n\n"
    f"Я также умею считать, достаточно воспользоваться командой /calc (например, /calc (10+2) * 3)")


# скрипт для того чтобы бот отвечал на сообщения содержащие тег криптовалюты
@dp.message_handler()
async def crypto(message: types.Message):
    user_message = message.text.lower().split()
    prev = ''
    for word in user_message:
        word = word.upper()
        if word in coins_dict and is_number(prev) and prev != '1':
            coin_price_usd = '{0:,}'.format(float(prev) * exchange.fetch_ticker(f'{word}/USD')['last']).replace(',', '`') # текущая цена умноженная на впереди стоящее число
            coin_percentage = exchange.fetch_ticker(f'{word}/USD')['percentage'] # изменение за день в процентах 
            # клавиатура для удаления сообщения
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Delete", callback_data="delete"))

            await message.reply(f'{prev} <b>{word}</b> costs: \n'
                                f'<b>———————————</b>\n'
                                f'<pre>{coin_price_usd} USD | {coin_percentage}%</pre>\n', reply_markup=keyboard)
        elif word in coins_dict:
            coin_price_usd = '{0:,}'.format(exchange.fetch_ticker(f'{word}/USD')['last']).replace(',', '`') # текущая цена 
            coin_percentage = exchange.fetch_ticker(f'{word}/USD')['percentage'] # изменение за день в процентах 
            # клавиатура для удаления сообщения
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Delete", callback_data="delete"))

            await message.reply(f'1 <b>{word}</b> costs: \n'
                                f'<b>———————————</b>\n'
                                f'<pre>{coin_price_usd} USD | {coin_percentage}%</pre>\n', reply_markup=keyboard)
        prev = word


async def on_startup(dp):
    print('BOT started....')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
