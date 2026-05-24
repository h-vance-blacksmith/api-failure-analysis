from .models import Incident


store: dict[str, Incident] = {}
index: list[dict] = []


def load(id: str, data: dict):
    incident = Incident(**data)
    incident.id = id
    store[id] = incident
    index.append({"id": id, "summary": incident.summary})


def get_all() -> list[dict]:
    return index


def get_by_id(id: str) -> Incident | None:
    return store.get(id)
