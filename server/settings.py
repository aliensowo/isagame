from pydantic_settings import BaseSettings


class ServerSettings(BaseSettings):
    version: str = "0.0.1"
    host: str = "127.0.0.1"
    port: int = 8000
    workers_count: int = 1
    reload: bool = True


settings: ServerSettings = ServerSettings()
