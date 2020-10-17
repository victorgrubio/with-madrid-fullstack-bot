# coding: utf-8
from bernard.storage.context import (
    create_context_store,
)
from os import(
    getenv
)

cs = create_context_store(ttl=0)
API_BASE = getenv("API_BASE", "https://framex-dev.wadrid.net/api/")
VIDEO_NAME = getenv(
    "VIDEO_NAME", "Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c"
)
DISPLAY_SIZE = (int(480 * 1.5), int(270 * 1.5))