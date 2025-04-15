from fastapi import APIRouter

from src.api.v1 import auth, book_offer, points, users

router = APIRouter(prefix="/v1")
router.include_router(auth.router)
router.include_router(book_offer.router)
router.include_router(points.router)
router.include_router(users.router)
