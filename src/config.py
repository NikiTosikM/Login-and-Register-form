from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    USER_DATABASE: str
    USER_PASSWORD: str
    HOST: str
    PORT: str
    DATABASE_NAME: str
    SECRET_JWT: str
    JWT_ALGORITHM: str

    def connect_db(self):
        return  f"postgresql+asyncpg://{self.USER_DATABASE}:{self.USER_PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE_NAME}"
    
    model_config = SettingsConfigDict(env_file="../.env")


setting = Settings()