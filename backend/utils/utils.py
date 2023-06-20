from urllib.parse import quote


def set_content_disposition(
    headers: dict,
    filename: str,
    content_disposition_type: str = "attachment",
):
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
