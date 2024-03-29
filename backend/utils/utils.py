import time
from typing import Awaitable
from urllib.parse import quote


def set_content_disposition(
    headers: dict,
    filename: str,
    content_disposition_type: str = "attachment",
) -> None:
    if not filename:
        return
    content_disposition_filename = quote(filename)
    if content_disposition_filename != filename:
        content_disposition = "{}; filename*=utf-8''{}".format(
            content_disposition_type, content_disposition_filename
        )
    else:
        content_disposition = '{}; filename="{}"'.format(
            content_disposition_type, filename
        )
    headers.setdefault("content-disposition", content_disposition)


async def elapse(async_func: Awaitable) -> float:
    start = time.perf_counter()
    await async_func
    elapsed = time.perf_counter() - start
    return elapsed
