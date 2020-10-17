# coding: utf-8
from bernard.storage.context import (
    create_context_store,
)
from os import(
    getenv
)

cs = create_context_store(ttl=0)

BASE_VIDEO_API_URL = getenv("BASE_VIDEO_API_URL", "https://framex-dev.wadrid.net/api/")
VIDEO_NAME = getenv(
    "VIDEO_NAME", "Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c"
)