
from datetime import datetime

from model.doc_model_base import DocModelBase


class ItemBaseInDB(DocModelBase):
    __table_name__ = "root/items/items"


class Item(ItemBaseInDB):
    item_id: str
    name: str
    content: str
    question: str
    confidence: int
    createdate: datetime
    lastupdate: datetime = None


class ItemCreate(ItemBaseInDB):
    item_id: str
    name: str
    content: str
    question: str
    confidence: int
    createdate: datetime = datetime.utcnow()


class ItemUpdate(ItemBaseInDB):
    name: str
    content: str
    question: str
    confidence: int
    lastupdate: datetime = datetime.utcnow()
