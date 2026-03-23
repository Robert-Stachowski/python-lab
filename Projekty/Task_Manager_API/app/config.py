import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("Brak lub błędy klucz dostępu")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30