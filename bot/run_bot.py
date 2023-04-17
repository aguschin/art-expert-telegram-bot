from bot.tg_bot import create_app


def main():
    app = create_app()
    app.run_polling()


if __name__ == "__main__":
    main()
