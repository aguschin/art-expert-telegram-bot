import random
from io import BytesIO

from coolname import generate
from httpx import AsyncClient
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.model_client import ModelClient
from bot.settings import BotSettings

settings = BotSettings()


model_client = ModelClient(
    model_api_url=settings.model_api_url,
    httpx_client=AsyncClient(),
)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! На связи ИИ. (Yes, I mean the ARTIFICIAL INTELLEGENCE). \n\n"
        f"Я взял все картины проданные на аукционе sothebys.com и "
        "обучил свою нейросеть, чтобы предсказать их стоимость.\n\n"
        "Отправь мне фотографию своего рисунка и я скажу, how much bucks он может стоить.",
    )


async def estimate_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    file_io = BytesIO()
    await photo_file.download_to_memory(out=file_io)
    res = await model_client.predict(file_io)

    pic_name = " ".join(generate(random.randint(2, 5))).capitalize()
    caption = f"""Original Title: {random.choice(["Unknown", pic_name])}
Author: {{author}}
Date: {random.choice(["2023", "Beginning of XXI century", "2020-es"])}
Estimated price: {{price}} $ [Sothebys auction]
Style: {random.choice(["Surrealism", "Realism", "Abstract Art", "Impressionism"])}
Genre: {random.choice(["animal painting", "portrait", "abstract", "illustration", "sketch and study", "figurative", "landscape"])}
Media: {random.choice(["oil", "pencil", "photo"])}
Similar painting: https://www.sothebys.com/en/buy/fine-art/paintings/abstract/_eve-ackroyd-woman-as-still-life-4eb9
    """
    # Price is estimated using Sothebys.com data
    # Other characteristics can be predicted using Wikiart data

    await update.message.reply_photo(
        update.message.photo[-1].file_id,
        caption=caption.format(
            price=res.price,
            author=update.effective_user.full_name,
        ),
    )


def create_app() -> Application:
    app = ApplicationBuilder().token(settings.telegram_token.get_secret_value()).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(MessageHandler(filters.PHOTO, estimate_price))

    return app
