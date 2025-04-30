from pydantic import BaseModel


class DatabaseModel(BaseModel):
    id: int
    name: str | None = None
    address: str | None = None
    status: str | None = None
