from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/")
def read_root():
    return {"Hello": "World"}
