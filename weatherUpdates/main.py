import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
# from telegram.ext import CallbackContext


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "6726605899:AAF5frBHD2xCXg9QM6k85Af7EieBzXSbpEI"
WEATHER_API_KEY = "b918144a1acc4215846f55e7d553f246"

ADMIN_USER_IDS = [1555861426]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to AST Bot! Type /subscribe to receive weather updates.')

def subscribe(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    context.user_data['subscribed'] = True
    update.message.reply_text('You are now subscribed to weather updates. '
                              'To get weather updates, type /weather.')

def weather(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if 'subscribed' in context.user_data and context.user_data['subscribed']:
        city = 'New Delhi'
        weather_data = get_weather(city)
        update.message.reply_text(f'Weather Update for {city}:\n{weather_data}')
    else:
        update.message.reply_text('You are not subscribed. Type /subscribe to receive weather updates.')

def get_weather(city: str) -> str:
    api_endpoint = 'https://api.weatherbit.io/v2.0/current'
    params = {'city': city, 'key': WEATHER_API_KEY}
    response = requests.get(api_endpoint, params=params)
    weather_data = response.json()
    print(weather_data)
    temperature = weather_data['data'][0]['app_temp']
    return f'Temperature: {temperature}°C\n'

def admin_panel(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if user_id in ADMIN_USER_IDS:
        update.message.reply_text('Admin Panel:\n'
                                  '/set_weather_api <api_key> - Set the weather API key\n'
                                  '/remove_user <user_id> - Remove (block and delete) a user account')
    else:
        update.message.reply_text('You are not authorized to access the admin panel.')

def set_weather_api(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if user_id in ADMIN_USER_IDS:
        if len(context.args) == 1:
            global WEATHER_API_KEY
            WEATHER_API_KEY = context.args[0]
            update.message.reply_text('Weather API key updated successfully.')
        else:
            update.message.reply_text('Usage: /set_weather_api <api_key>')
    else:
        update.message.reply_text('You are not authorized to use this command.')


def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("subscribe", subscribe))
    dispatcher.add_handler(CommandHandler("weather", weather))
    dispatcher.add_handler(CommandHandler("admin", admin_panel))
    dispatcher.add_handler(CommandHandler("set_weather_api", set_weather_api, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
