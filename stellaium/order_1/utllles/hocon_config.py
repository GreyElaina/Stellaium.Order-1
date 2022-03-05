from typing import Any, Dict
from pydantic import BaseSettings, BaseConfig, BaseModel
import pyhocon
from pathlib import Path
import stringcase

class HoconModelConfig(BaseConfig):
    env_file_encoding = 'utf-8'
    env_file = "./config.conf"

    @classmethod
    def hocon_config_settings_source(cls, settings: BaseSettings) -> Dict[str, Any]:
        encoding = settings.__config__.env_file_encoding
        return dict(pyhocon.ConfigFactory.parse_string(Path(cls.env_file).read_text(encoding)))

    @classmethod
    def customise_sources(
        cls,
        init_settings,
        env_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            cls.hocon_config_settings_source,
            env_settings,
            file_secret_settings,
        )

    alias_generator = stringcase.spinalcase

class HoconConfig(BaseSettings):
    class Config(HoconModelConfig):
        pass
