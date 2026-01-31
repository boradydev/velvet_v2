from enum import Enum


class AppEnv(str, Enum):
    test = "test"
    local = "local"
    dev = "dev"
    prod = "prod"
