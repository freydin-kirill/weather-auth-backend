from src.common.core import BaseDAO
from src.user.models import User


class UserDAO(BaseDAO):
    """Data Access Object (DAO) for user-related operations.
    This class provides methods to interact with the database for user management.
    """
    model = User
