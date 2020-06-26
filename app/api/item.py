
from fastapi import APIRouter

from service import item_service

router = APIRouter()


@router.get("/")
async def read_root():
    return {"Hello": "Universe"}

@router.post("/ask")
def predict(context: "Some story of wild.", question: "What happened?"):
    return item_service.answer_question(context, question)
