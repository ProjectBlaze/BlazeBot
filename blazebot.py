import logging
import os
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler
from commands import *
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    # Start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    # Help
    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)
    # Post
    post_handler = CommandHandler('post', post)
    application.add_handler(post_handler)
    # Upload
    upload_handler = CommandHandler('upload', upload)
    application.add_handler(upload_handler)
    # Test
    test_handler = CommandHandler('test', test)
    application.add_handler(test_handler)


    application.run_polling()
