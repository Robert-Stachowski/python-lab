from pydantic import BaseModel
from typing import Generic, TypeVar, List

# T to "placeholder" na dowolny typ — raz TaskResponse, raz UserResponse itp.
# Dzięki temu jeden schemat obsługuje paginację dla wszystkich list w API.
T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    
    total: int   # COUNT(*) — liczba wszystkich rekordów (po filtrach, przed paginacją)
    skip: int    # OFFSET — ile rekordów pominięto od początku
    limit: int   # LIMIT — ile rekordów zwrócono
    items: List[T]  # lista wyników — typ T podmieniony na konkretny schemat