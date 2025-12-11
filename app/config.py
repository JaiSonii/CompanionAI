from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    CONTEXT_WINDOW: int = 5
    CHAT_MODEL: str = "gemini-2.5-flash"
    SUMMARIZATION_MODEL: str = "gemini-2.5-flash"

    class Config:
        env_file = ".env"

settings = Settings() #type:ignore