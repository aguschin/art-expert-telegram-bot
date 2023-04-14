from pydantic import AnyUrl, BaseSettings, SecretStr


class BotSettings(BaseSettings):
    model_api_url: AnyUrl
    telegram_token: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
