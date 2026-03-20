from pydantic import BaseModel
from typing import Generic, TypeVar, List

# T to "placeholder" na dowolny typ — raz TaskResponse, raz UserResponse itp.
# Dzięki temu jeden schemat obsługuje paginację dla wszystkich list w API.
T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generyczny schemat odpowiedzi z paginacją.

    Użycie: PaginatedResponse[TaskResponse], PaginatedResponse[UserResponse] itp.

    Przykładowa odpowiedź:
    {
        "total": 50000,  <- ile wszystkich pasujących rekordów jest w bazie
        "skip": 20,      <- ile rekordów zostało pominiętych
        "limit": 10,     <- ile rekordów zwrócono na tej stronie
        "items": [...]   <- lista rekordów (konkretny typ zależy od T)
    }
    """
    total: int   # COUNT(*) — liczba wszystkich rekordów (po filtrach, przed paginacją)
    skip: int    # OFFSET — ile rekordów pominięto od początku
    limit: int   # LIMIT — ile rekordów zwrócono
    items: List[T]  # lista wyników — typ T podmieniony na konkretny schemat