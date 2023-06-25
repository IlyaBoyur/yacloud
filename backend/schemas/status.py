from pydantic import BaseModel


class Status(BaseModel):
    db: float
    cache: float


class StatusError(BaseModel):
    detail: str | dict[str, str]
