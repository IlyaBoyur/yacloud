from pydantic import BaseModel


class Status(BaseModel):
    db: float


class StatusError(BaseModel):
    detail: str | dict[str, str]
