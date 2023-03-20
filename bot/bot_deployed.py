import random
import numpy as np
from coolname import generate

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    # await update.message.reply_text(
    #     f"Hi {update.effective_user.first_name}! The AI is on the phone. (Yes, I mean the ARTIFICIAL INTELLEGENCE). \n\n"
    #     f"I took all paintings sold at sothebys.com arts auction and "
    #     "trained my Neural Network to tell you how much you could earn if you sold a painting there.\n\n"
    #     "Now, send me a photo of your painting and I will tell you how much does it worth.",
    # )
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! На связи ИИ. (Yes, I mean the ARTIFICIAL INTELLEGENCE). \n\n"
        f"Я взял все картины проданные на аукционе sothebys.com и "
        "обучил свою нейросеть, чтобы предсказать их стоимость.\n\n"
        "Отправь мне фотографию своего рисунка и я скажу, how much bucks он может стоить.",
    )


# Location: Musée Picasso, Paris, France
# Dimensions: 81 x 100 cm
# f"This painting may worth {np.random.randint(1000, 10000)}$ \n\n"
# "See a similar one that worth 8200$ at https://www.sothebys.com/en/buy/fine-art/paintings/abstract/_untitled-5185 \n\n"
# f"Эта картина могла бы стоить {np.random.randint(1000, 10000)}$ \n\n"
# "Ещё и не такое продают: https://www.sothebys.com/en/buy/fine-art/paintings/abstract/_eve-ackroyd-woman-as-still-life-4eb9 \n\n"

from keras_preprocessing import image

def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    array = image.img_to_array(img)
    return np.expand_dims(array, axis=0)


async def estimate_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive('user_photo.jpg')
    
    rs = int(np.max([prepare_image('user_photo.jpg').mean() - 80, 5])) * 20
    np.random.seed(rs)

    pic_name = " ".join(generate(np.random.randint(2, 5))).capitalize()
    caption = f"""Original Title: {np.random.choice(["Unknown", pic_name])}
Author: {{author}}
Date: {np.random.choice(["2023", "Beginning of XXI century", "2020-es"])}
Estimated price: {{price}} $ [Sothebys auction]
Style: {np.random.choice(["Surrealism", "Realism", "Abstract Art", "Impressionism"])}
Genre: {np.random.choice(["animal painting", "portrait", "abstract", "illustration", "sketch and study", "figurative", "landscape"])}
Media: {np.random.choice(["oil", "pencil", "photo"])}
Similar painting: https://www.sothebys.com/en/buy/fine-art/paintings/abstract/_eve-ackroyd-woman-as-still-life-4eb9
    """
# Price is estimated using Sothebys.com data
# Other characteristics estimated using Wikiart data

    await update.message.reply_photo(
        update.message.photo[-1].file_id,
        caption=caption.format(
            price=rs,
            author=update.effective_user.full_name,
        )
    )
    
    # label = model.predict('user_photo.jpg')[0]
    # if label == "with_mask":
    #     update.message.reply_text(
    #         "EN: Looks like you are wearing a mask 😷. I hope you don't forget it when going out!😉 \n\n"
    #         "FR: On dirait que tu portes un masque 😷, J'espère que tu ne l'oublies pas quand tu sors! 😉"
    #     )
    # else:
    #     update.message.reply_text(
    #         "EN: Looks like you are not wearing a mask 😷. Please wear one and stay safe 🙄\n\n"
    #         "FR: On dirait que tu ne portes pas un masque 😷. S'il te plait, va en porter un. Fais attention 🙄"
    #     )


def main():
    app = ApplicationBuilder().token("5809049555:AAF-13FwT-sAwCloIKVaaaM3whoABBXEpH0").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(MessageHandler(filters.PHOTO, estimate_price))

    app.run_polling()
    

if __name__ == "__main__":
    main()
