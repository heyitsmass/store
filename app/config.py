from pydantic_settings import BaseSettings


class Config(BaseSettings):

    static_dir: str = "static"
    templates_dir: str = "app/jinja"
    database_file: str = "db.json"


config = Config()
