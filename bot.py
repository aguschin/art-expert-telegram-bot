import os

import numpy as np
from coolname import generate
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# create a telegram bot and paste it here, or use `flyctl secrets set TELEGRAM_TOKEN=token` to set it secretly
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TOKEN")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        f"Hi, {update.effective_user.first_name}! AI is on the line. (Yes, I mean the ARTIFICIAL INTELLEGENCE). \n\n"
        "I will tell you what kind of art you send to me and how much bucks it may worth.",
    )


async def estimate_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive('user_photo.jpg')

    pic_name = " ".join(generate(np.random.randint(2, 5))).capitalize()
    caption = f"""Original Title: {np.random.choice(["Unknown", pic_name])}
Author: {update.effective_user.full_name}
Date: {np.random.choice(["2023", "Beginning of XXI century", "2020-es"])}
Estimated price: {np.random(0, 100000)} $ [Sothebys auction]
Style: {np.random.choice(["Surrealism", "Realism", "Abstract Art", "Impressionism"])}
Genre: {np.random.choice(["animal painting", "portrait", "abstract", "illustration", "sketch and study", "figurative", "landscape"])}
Media: {np.random.choice(["oil", "pencil", "photo"])}
Similar painting: https://www.sothebys.com/en/buy/fine-art/paintings/abstract/_eve-ackroyd-woman-as-still-life-4eb9
    """

    await update.message.reply_photo(
        update.message.photo[-1].file_id,
        caption=caption
    )


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(MessageHandler(filters.PHOTO, estimate_price))

    app.run_polling()


if __name__ == "__main__":
    main()
