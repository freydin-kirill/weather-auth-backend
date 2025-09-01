from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """Hash a user's password.

    :param password: plain password, str
    :returns: hashed string, str
    """

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.

    :param plain_password: original password, str
    :param hashed_password: hashed password, str
    :returns: verification result, bool
    """

    return pwd_context.verify(plain_password, hashed_password)
