import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

# تنظیمات توکن‌ها
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
POE_API_URL = 'https://api.poe.com/v1/your_endpoint'
POE_API_KEY = os.getenv('POE_API_KEY')

# راه‌اندازی لاگ‌گیری
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('سلام! من ربات شما هستم.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('چطور می‌توانم کمکتان کنم؟')

def poe_response(message: str) -> str:
    headers = {
        'Authorization': f'Bearer {POE_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'query': message
    }
    response = requests.post(POE_API_URL, headers=headers, json=data)
    return response.json().get('response', 'خطایی رخ داده است.')

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = poe_response(user_message)
    update.message.reply_text(response)

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
