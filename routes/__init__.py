from .auth import auth_bp
from .main import main_bp
from .user import user_bp

__all__ = [
    "main_bp",
    "user_bp",
    "auth_bp",
]
