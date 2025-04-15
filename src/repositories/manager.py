from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.book_offer import BookRepository
from src.repositories.points import PointRepository
from src.repositories.user import UserRepository


class RepositoryManager:
    def __init__(self, session: AsyncSession) -> None:
        self.book_offer_repo = BookRepository(session)
        self.point_repo = PointRepository(session)
        self.user_repo = UserRepository(session)
