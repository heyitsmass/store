from pathlib import Path
from config import config
from models import DatabaseModel
from jinja import templates

from fastapi import Request

import json
import os


class Database(dict[int, DatabaseModel]):
    def __init__(self):
        super().__init__()
        self.path = Path(config.database_file).resolve()
        if not os.path.exists(self.path):
            self._create()
        self._load_from_disk()

    def _create(self):
        with open(self.path, "w+") as f:
            json.dump([], f)

    def _load_db(self, db: dict, save: bool = False):

        instance = self.create_db(db)
        if save:
            instance.save()

    def _load_from_disk(self):
        with open(self.path, "r") as f:
            for db in json.load(f):
                self._load_db(db)

    def check_existence(self, id: int):
        if id not in self:
            raise ValueError("Database not found")

    def create_db(self, db: dict):
        id = db.get("id")
        if id is None:
            id = len(self)
            db["id"] = id
        self[id] = DatabaseModel(**db)
        return self

    def update(self, id: int, **db: DatabaseModel):
        self.check_existence(id)
        curr = self.get(id)
        for key, value in db.items():
            setattr(curr, key, value)
        return self

    def remove(self, id: int):
        if id not in self:
            raise ValueError("Database not found")
        del self[id]
        return self

    @property
    def _databases(self):
        return [db.model_dump() for db in self.values()]

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self._databases, f)

    def render(self, request: Request):
        return templates.TemplateResponse(
            "index.jinja",
            context={
                "request": request,
                "databases": self._databases,
            },
        )
