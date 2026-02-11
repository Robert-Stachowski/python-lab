# 🧠 AI Knowledge Assistant — RAG Backend Project

## Projekt portfoliowy: Inteligentny asystent z własną bazą wiedzy

---

## 📌 Opis projektu

**AI Knowledge Assistant** to backendowa aplikacja umożliwiająca użytkownikowi zadawanie pytań w języku naturalnym i otrzymywanie precyzyjnych odpowiedzi opartych na **własnej bazie wiedzy** (dokumenty, artykuły, notatki). System wykorzystuje architekturę **RAG (Retrieval-Augmented Generation)** — zamiast polegać wyłącznie na wiedzy modelu LLM, wyszukuje najpierw relevantne fragmenty z bazy wektorowej i przekazuje je jako kontekst do modelu.

**Efekt:** minimalizacja halucynacji, maksymalizacja jakości odpowiedzi, pełna kontrola nad źródłami wiedzy.

---

## 🎯 Cele projektu

1. Zbudować działający RAG pipeline od A do Z
2. Nauczyć się praktycznie: embeddings, vector databases, chunking, prompt engineering
3. Stworzyć projekt portfoliowy na poziomie mid-level developera
4. Pokazać umiejętność integracji AI w architekturze backendowej
5. Przygotować solidne README, diagramy i testy

---

## 🏗️ Architektura systemu (wysokopoziomowa)

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Klient    │────▶│   FastAPI     │────▶│  Query Engine   │
│  (API/CLI)  │◀────│   REST API    │◀────│  (RAG Pipeline) │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                   │
                                    ┌──────────────┼──────────────┐
                                    ▼              ▼              ▼
                             ┌────────────┐ ┌───────────┐ ┌────────────┐
                             │  Embedding │ │  Vector   │ │    LLM     │
                             │  Service   │ │    DB     │ │  Service   │
                             │ (OpenAI)   │ │(Qdrant)   │ │ (OpenAI)   │
                             └────────────┘ └───────────┘ └────────────┘
```

### Warstwy aplikacji

```
📁 src/
├── api/              ← Endpointy FastAPI (kontrollery)
├── services/         ← Logika biznesowa (RAG, embedding, LLM)
├── repositories/     ← Warstwa dostępu do danych (vector DB, metadata)
├── models/           ← Pydantic schemas (request/response)
├── core/             ← Konfiguracja, settings, exceptions
├── ingestion/        ← Pipeline ładowania i przetwarzania dokumentów
└── tests/            ← Testy jednostkowe i integracyjne
```

---

## 🔧 Stack technologiczny

| Warstwa | Technologia | Dlaczego |
|---|---|---|
| **Framework API** | FastAPI | Async, szybki, świetna dokumentacja, type hints |
| **Baza wektorowa** | Qdrant | Open-source, łatwy setup (Docker), REST + Python SDK |
| **Embeddings** | OpenAI `text-embedding-3-small` | Najlepsza jakość/cena, prosty API |
| **LLM** | OpenAI `gpt-4o-mini` | Tani, szybki, wystarczający do RAG |
| **Chunking** | LangChain Text Splitters | Gotowe, konfigurowalne splittery |
| **ORM/Metadata** | SQLAlchemy + SQLite/PostgreSQL | Metadata dokumentów, historia zapytań |
| **Testy** | pytest + httpx | Standard w Python, async support |
| **Konteneryzacja** | Docker + docker-compose | Qdrant + app w jednym poleceniu |
| **Config** | python-dotenv + pydantic-settings | Bezpieczne zarządzanie API keys |
| **CI** | GitHub Actions | Automatyczne testy przy push |

---

## 📚 Czego musisz się nauczyć (i w jakiej kolejności)

### Faza 0 — Fundament teoretyczny (3-5 dni)

> Zanim napiszesz linijkę kodu, zrozum CO budujesz.

| Temat | Co dokładnie | Zasoby |
|---|---|---|
| Czym jest embedding | Tekst → wektor liczbowy, semantic similarity | [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings) |
| Czym jest baza wektorowa | Przechowywanie wektorów + wyszukiwanie nearest neighbors | Dokumentacja Qdrant |
| Czym jest RAG | Retrieve → Augment → Generate — cały przepływ | [RAG paper](https://arxiv.org/abs/2005.11401), blogi |
| Chunking | Dlaczego i jak dzielić dokumenty na fragmenty | LangChain docs, eksperymenty |
| Prompt engineering | Jak konstruować prompt z kontekstem | OpenAI Cookbook |
| Cosine similarity | Jak mierzy się podobieństwo wektorów (intuicja, nie math) | Wizualizacje na YouTube |

**Cel:** Umieć narysować na kartce cały flow RAG od dokumentu do odpowiedzi.

### Faza 1 — Proof of Concept w jednym pliku (3-4 dni)

> Jeden skrypt Pythona, który robi cały RAG od A do Z.

```python
# poc_rag.py — Twój pierwszy RAG w 50 linijkach
# 1. Wczytaj tekst
# 2. Podziel na chunki
# 3. Wygeneruj embeddingi (OpenAI API)
# 4. Zapisz do Qdrant
# 5. Przyjmij pytanie usera
# 6. Wygeneruj embedding pytania
# 7. Wyszukaj top-k chunków z Qdrant
# 8. Zbuduj prompt: "Na podstawie kontekstu odpowiedz: {pytanie}"
# 9. Wyślij do OpenAI Chat API
# 10. Zwróć odpowiedź
```

**Cel:** Zobaczyć, że to DZIAŁA. Poczuć magię. Zmotywować się.

### Faza 2 — Architektura i refaktor (5-7 dni)

> Przepisz PoC na porządną, warstwową aplikację.

**Zadania:**
- Stwórz strukturę katalogów (patrz wyżej)
- Wydziel `EmbeddingService`, `VectorRepository`, `LLMService`, `RAGService`
- Stwórz Pydantic modele request/response
- Dodaj `Settings` z pydantic-settings (`.env`)
- Dependency injection przez FastAPI `Depends()`
- Error handling (custom exceptions + handlers)

### Faza 3 — Ingestion Pipeline (4-5 dni)

> System ładowania dokumentów do bazy wiedzy.

**Funkcjonalności:**
- Upload dokumentów przez API (`.txt`, `.md`, `.pdf`)
- Automatyczny chunking (recursive text splitter)
- Generowanie embeddingów batch
- Zapis do Qdrant z metadanymi (nazwa pliku, data, chunk_index)
- Zapis metadanych dokumentu do SQL (SQLAlchemy)
- Endpoint: `POST /documents/upload`
- Endpoint: `GET /documents` — lista załadowanych dokumentów
- Endpoint: `DELETE /documents/{id}` — usunięcie dokumentu + chunków

### Faza 4 — Query Engine (3-4 dni)

> Silnik odpowiadania na pytania.

**Funkcjonalności:**
- Endpoint: `POST /query` — zadaj pytanie, dostań odpowiedź
- Wyszukiwanie semantyczne top-k chunków
- Budowanie prompta z kontekstem + system message
- Streaming odpowiedzi (SSE) — opcjonalnie
- Zwracanie źródeł (z którego dokumentu/chunka pochodzi odpowiedź)
- Historia zapytań w SQL

**Response schema:**
```json
{
  "answer": "Django to framework webowy...",
  "sources": [
    {
      "document": "python_basics.md",
      "chunk": "Django jest full-stack frameworkiem...",
      "relevance_score": 0.92
    }
  ],
  "query_id": "uuid-123"
}
```

### Faza 5 — Testy (4-5 dni)

> Testy to Twoja wizytówka. Rekruter zobaczy je PIERWSZE.

| Typ testu | Co testujesz | Narzędzia |
|---|---|---|
| Unit | Chunking, prompt building, parsowanie | pytest, unittest.mock |
| Integration | Embedding → Qdrant → retrieval | pytest + testcontainers / Qdrant in-memory |
| API (e2e) | Pełny flow: upload → query → response | httpx.AsyncClient + TestClient |
| Fixtures | Przykładowe dokumenty, mocki API | conftest.py, factories |

**Cele testów:**
- Pokrycie kluczowych ścieżek (happy path + edge cases)
- Mockowanie external API (OpenAI) w unit testach
- Prawdziwy Qdrant w testach integracyjnych (Docker)
- Minimum 70-80% coverage na services/

### Faza 6 — DevOps & Polish (3-4 dni)

**Docker:**
```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [qdrant]
  qdrant:
    image: qdrant/qdrant:latest
    ports: ["6333:6333"]
```

**GitHub Actions CI:**
```yaml
# .github/workflows/ci.yml
- Lint (ruff/flake8)
- Type check (mypy) — opcjonalnie
- Testy (pytest)
- Coverage report
```

**README:**
- Opis projektu + screenshot/demo
- Diagram architektury (Mermaid lub draw.io)
- Quick start (docker-compose up)
- Przykłady użycia API (curl/httpx)
- Opis decyzji technologicznych
- Co bym zmienił / roadmap

---

## 📐 Diagramy do stworzenia

1. **Diagram architektury** — warstwy systemu (ten z góry, ale ładniejszy)
2. **Diagram przepływu RAG** — od pytania usera do odpowiedzi (sequence diagram)
3. **Diagram ingestion** — od uploadu dokumentu do zapisu w Qdrant
4. **Diagram ERD** — tabele SQL (documents, queries, chunks metadata)

Narzędzia: Mermaid (w README), draw.io, Excalidraw

---

## 🗓️ Harmonogram (szacunkowo 4-6 tygodni)

| Tydzień | Faza | Rezultat |
|---|---|---|
| 1 | Faza 0 + Faza 1 | Teoria + działający PoC w jednym pliku |
| 2 | Faza 2 | Warstwowa architektura, FastAPI, DI |
| 3 | Faza 3 | Ingestion pipeline, upload dokumentów |
| 4 | Faza 4 | Query engine, pełny RAG flow przez API |
| 5 | Faza 5 | Testy (unit, integration, e2e) |
| 6 | Faza 6 | Docker, CI, README, diagramy, polish |

---

## 🔑 Kluczowe pliki konfiguracyjne

### `.env.example`
```env
OPENAI_API_KEY=sk-your-key-here
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=knowledge_base
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o-mini
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RESULTS=5
DATABASE_URL=sqlite:///./metadata.db
```

### `pyproject.toml` (dependencies)
```toml
[project]
name = "ai-knowledge-assistant"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    "fastapi>=0.110",
    "uvicorn[standard]",
    "openai>=1.0",
    "qdrant-client>=1.7",
    "langchain-text-splitters>=0.0.1",
    "sqlalchemy>=2.0",
    "pydantic-settings>=2.0",
    "python-dotenv",
    "python-multipart",    # file uploads
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio",
    "httpx",
    "ruff",
    "coverage",
]
```

---

## 🚀 Endpointy API (plan)

| Metoda | Endpoint | Opis |
|---|---|---|
| `POST` | `/api/v1/documents/upload` | Upload dokumentu do bazy wiedzy |
| `GET` | `/api/v1/documents` | Lista załadowanych dokumentów |
| `GET` | `/api/v1/documents/{id}` | Szczegóły dokumentu + chunki |
| `DELETE` | `/api/v1/documents/{id}` | Usunięcie dokumentu |
| `POST` | `/api/v1/query` | Zadaj pytanie → otrzymaj odpowiedź RAG |
| `GET` | `/api/v1/query/history` | Historia zapytań |
| `GET` | `/api/v1/health` | Health check |
| `GET` | `/api/v1/stats` | Statystyki (ile dokumentów, chunków, zapytań) |

---

## 💡 Opcjonalne rozszerzenia (po MVP)

Jeśli starczy czasu i motywacji — każde z tych rozszerzeń podnosi wartość projektu:

| Rozszerzenie | Opis | Trudność |
|---|---|---|
| **Conversation memory** | Wieloturowe rozmowy z kontekstem | ⭐⭐ |
| **Re-ranking** | Ponowne rankowanie wyników (cross-encoder) | ⭐⭐⭐ |
| **Hybrid search** | Wyszukiwanie semantyczne + keyword (BM25) | ⭐⭐⭐ |
| **Web UI** | Prosty frontend (React/HTMX) | ⭐⭐ |
| **Multi-collection** | Różne bazy wiedzy per user/temat | ⭐⭐ |
| **PDF parsing** | Parsowanie złożonych PDF-ów (tabele, obrazy) | ⭐⭐⭐ |
| **Evaluation pipeline** | Automatyczna ocena jakości odpowiedzi | ⭐⭐⭐⭐ |
| **Auth** | JWT + role-based access | ⭐⭐ |
| **Rate limiting** | Limity zapytań per user | ⭐ |
| **Caching** | Redis cache na powtarzające się zapytania | ⭐⭐ |

---

## 🎯 Czym ten projekt wyróżnia się w portfolio

1. **Nie jest CRUD-em** — to system z prawdziwą logiką biznesową
2. **Integruje AI** — embeddingi, LLM, baza wektorowa
3. **Ma porządną architekturę** — service-repository, DI, warstwy
4. **Ma testy** — unit, integration, e2e
5. **Jest skonteneryzowany** — Docker + docker-compose
6. **Ma CI/CD** — GitHub Actions
7. **Ma dokumentację** — README z diagramami, przykłady API
8. **Rozwiązuje realny problem** — wyszukiwanie wiedzy w dokumentach

---

## 📖 Zasoby do nauki

### Embeddings & Vector DB
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [What are Vector Databases?](https://www.pinecone.io/learn/vector-database/) — Pinecone (teoria)

### RAG
- [RAG from scratch — LangChain YouTube](https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23CLFamC)
- [OpenAI Cookbook — RAG](https://cookbook.openai.com/)
- [Building RAG from scratch (bez frameworków)](https://github.com/anthropics/anthropic-cookbook)

### FastAPI + architektura
- [FastAPI docs](https://fastapi.tiangolo.com/)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)

### Testy
- [pytest docs](https://docs.pytest.org/)
- [Testing FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)

---

## ✅ Definition of Done

Projekt jest gotowy do portfolio gdy:

- [ ] `docker-compose up` uruchamia całą aplikację
- [ ] Można uploadować dokumenty przez API
- [ ] Można zadawać pytania i otrzymywać odpowiedzi ze źródłami
- [ ] Testy przechodzą (min. 70% coverage)
- [ ] CI pipeline jest zielony
- [ ] README zawiera: opis, diagram, quickstart, przykłady
- [ ] Kod jest czysty, sformatowany (ruff), z docstringami
- [ ] `.env.example` jest dołączony (bez prawdziwych kluczy!)
- [ ] Repozytorium ma sensowną historię commitów

---

> **Pamiętaj:** Ten projekt nie musi być perfekcyjny od razu. Zbuduj MVP (Fazy 0-4), a potem iteruj. Lepiej mieć działający RAG z testami niż idealną architekturę bez działającego kodu.
