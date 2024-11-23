from fastapi import APIRouter

from database import get_db
from backend.api.database.models import Question

router = APIRouter(
    prefix="api/question"
)