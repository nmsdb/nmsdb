from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MAINTENANCE_MODE: bool = False

    # CORs - https://fastapi.tiangolo.com/tutorial/cors/
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]
    CORS_HEADERS: list[str] = ["*"]

    # More verbose logging
    DEBUG_MODE: bool = False

    DATABASE_URI: str = "mysql+asyncmy://root:Pa55w0rd!@localhost:3306/nmsdb"

    REDIS_URI: str = "redis://localhost:6379"
    REDIS_PASSWORD: str = "Pa55w0rd!"
    CACHE_EXPIRE: int = 60


settings = Settings()
