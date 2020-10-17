# coding: utf-8
from bernard.storage.context import (
    create_context_store,
)
from os import(
    getenv
)

cs = create_context_store(ttl=0)
