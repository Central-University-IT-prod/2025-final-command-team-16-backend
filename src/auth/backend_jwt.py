from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend
from fastapi_users import FastAPIUsers

from src.auth.user_manager import get_user_manager
from src.models import User

SECRET = "SECRET"

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)