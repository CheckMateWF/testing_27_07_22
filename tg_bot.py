import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler

from token_parse import API_TOKEN_TG

from api_weather import get_weather

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    temperature = get_weather(update.message.text)
    if temperature:
        textMessage = ('По данным Яндекс.Погода в ' + update.message.text +
                       '\n температура: ' + str(temperature))
    else:
        textMessage = ('Информации о погоде в этом городе нет.' +
                       'Проверьте правильность написания названия города' +
                       ' и повторите попытку снова. Например: Нижний Новгород')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=textMessage)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Напиши мне название города,\
     в котором хочешь узнать погоду. \n Пример: Москва")

if __name__ == '__main__':
    application = ApplicationBuilder().token(API_TOKEN_TG).build()

    start_handler = CommandHandler('start', start)
    weather_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), weather)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(weather_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
