
from datetime import datetime

from model.doc_model_base import DocModelBase


class ItemBaseInDB(DocModelBase):
    __table_name__ = "root_collection/root_document/items"


class Item(ItemBaseInDB):
    item_id: str
    name: str
    content: str
    question: str
    confidence: int
    correct_answers: list = []
    incorrect_answers: list = []
    createdate: datetime
    lastupdate: datetime = None


class ItemCreate(ItemBaseInDB):
    item_id: str
    name: str
    content: str
    question: str
    confidence: int
    correct_answers: list = []
    incorrect_answers: list = []
    createdate: datetime = datetime.utcnow()


class ItemUpdate(ItemBaseInDB):
    name: str
    content: str
    question: str
    confidence: int
    correct_answers: list = []
    incorrect_answers: list = []
    lastupdate: datetime = datetime.utcnow()
