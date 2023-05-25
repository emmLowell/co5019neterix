import os
from typing import Dict, TypeVar, Type
from dataclasses import dataclass
from .JSONSerializer import JSONSerializer


@dataclass
class RedisConfig:
    url: str = "redis://localhost:6379"


@dataclass
class GeneralConfig:
    production: bool = False
    website_link: str = "http://localhost:8080"


T = TypeVar("T", RedisConfig, GeneralConfig)


class ConfigManager:
    configs: Dict[str, T]

    def __init__(self):
        self.configs = {}
        if not os.path.exists("configs"):
            os.mkdir("configs")

    def _class_to_name(self, config: Type[T]) -> str:
        return f"configs/{config.__name__.removesuffix('Config')}.json"

    def read_config(self, config: Type[T]) -> T:
        name = self._class_to_name(config)
        if name in self.configs:
            return self.configs[name]
        if not os.path.exists(name):
            self.save_config(config())
        return JSONSerializer.deserialize(config, name)

    def save_config(self, config: T):
        name = self._class_to_name(type(config))
        self.configs[name] = config
        JSONSerializer.serialize(config, name)
