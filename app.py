from flask import Flask, render_template, request, redirect, url_for
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext
from telegram.error import TelegramError

app = Flask(__name__)

BOT_TOKEN = '6726605899:AAF5frBHD2xCXg9QM6k85Af7EieBzXSbpEI'
bot = Bot(token=BOT_TOKEN)

blocked_users = []


@app.route('/')
def index():
    return render_template('index.html', blocked_users=blocked_users, bot_token=BOT_TOKEN)


@app.route('/block_user', methods=['POST'])
def block_user():
    user_id = request.form.get('user_id')
    if user_id:
        try:
            bot.send_message(chat_id=user_id, text="You have been blocked.")
            blocked_users.append(user_id)
            return redirect(url_for('index'))
        except TelegramError as e:
            return f"Error blocking user: {str(e)}"
    else:
        return "User ID is required."


@app.route('/unblock_user', methods=['POST'])
def unblock_user():
    user_id = request.form.get('user_id')
    if user_id:
        blocked_users.remove(user_id)
        return redirect(url_for('index'))
    else:
        return "User ID is required."


@app.route('/update_bot_settings', methods=['POST'])
def update_bot_settings():
    new_token = request.form.get('new_token')
    if new_token:
        global BOT_TOKEN
        BOT_TOKEN = new_token
        bot.token = new_token
        return redirect(url_for('index'))
    else:
        return "New API Key is required."

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! This is your AST Consulting bot.')

if __name__ == '__main__':
    app.run(debug=True)
