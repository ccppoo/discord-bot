import os
import logging

__all__ = [
    "RELEASE",
    "TOKEN"
]

# TODO : add logging mechanism for logging level
# pycord has its own logging(warning, debug) >> discriminate it

env = lambda x : os.getenv(x)

RELEASE = True if env('RELEASE') else False

TOKEN = token if (token:= env("DISCORD_BOT_TOKEN")) else None