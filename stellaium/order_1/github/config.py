from stellaium.order_1.utllles.hocon_config import HoconConfig

class GithubConfig(HoconConfig):
    access_token: str

    class Config(HoconConfig.Config):
        pass