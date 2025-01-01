from pathlib import Path
from importlib.metadata import version
from typing import Type, Tuple
import click
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


APP_NAME: str = "kanjo"
APP_DIR: Path = Path(click.get_app_dir(app_name=APP_NAME))
DB_URL: Path = APP_DIR / f"{APP_NAME}.db"
CONFIG_FILE_PATH: Path = APP_DIR / "config.toml"


class Settings(BaseSettings):
    version: str = version(APP_NAME)
    theme: str = "dracula"

    model_config = SettingsConfigDict(
        toml_file=CONFIG_FILE_PATH,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        APP_DIR.mkdir(parents=True, exist_ok=True)
        return (
            init_settings,
            TomlConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


if __name__ == "__main__":
    settings = Settings()
    print(settings.model_dump())
