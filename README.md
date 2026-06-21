# Bookwurm Adaptive Language Reader

A language learning app built around Stephen Krashen's input hypothesis: that acquisition happens fastest when reading material contains roughly 1% unknown vocabulary; just enough challenge to stretch comprehension without losing meaning.

i+1 delivers sentence- and paragraph-level reading chunks, scores them against the learner's known vocabulary, and sequences them using spaced repetition so every session stays at the ideal difficulty level. As the user's vocabulary grows, the scoring updates automatically, surfacing harder content only when the learner is ready for it.

Think Anki meets LingQ, driven by an algorithm instead of manual curation.

---

## Scope

The core loop:

1. User reads a text chunk
2. Unknown words can be looked up (tracked as a difficulty signal)
3. User rates comprehension (1–5)
4. SRS algorithm schedules the next review
5. Vocabulary model updates, re-scoring future cards automatically

Each card carries NLP metadata: sub-word tokens, lemmas, frequency rank, and a history of past exposures. The i+1 scorer uses this to rank candidate cards by predicted comprehension and serves the most appropriate one next.

---

## Planned Architecture

```
Reader UI (HTML / Gradio)
        │
        │ REST
        ▼
FastAPI (app/main.py)
   ├── routers/        ← cards, reviews, vocab
   ├── services/       ← SRS algorithm, i+1 scorer
   ├── models.py       ← SQLAlchemy table definitions
   └── schemas.py      ← Pydantic request/response shapes
        │
        ├── SQLite (dev) → PostgreSQL (prod)
        └── S3           ← model artifacts, corpora (later)

Deployment
   ├── Docker           ← containerised from day one
   ├── Railway          ← MVP hosting
   └── AWS ECS Fargate  ← production target (later)

CI/CD
   └── GitHub Actions   ← test → build → push → deploy
```

---

```

<!-- TREE_START -->

```text
app
├── core
│   ├── __init__.py
│   └── dependencies.py
├── db
│   ├── __init__.py
│   ├── database.py
│   └── models.py
├── modules
│   ├── cards
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── repository.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── decks
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── repository.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── reviews
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── repository.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── __init__.py
│   └── router_template.py
├── __init__.py
└── main.py
```
<!-- TREE_END -->

```
---

## Work Packages

### WP1: Data model and SRS core
- PostgreSQL/SQLite schema: users, cards, vocab items, review history
- SQLAlchemy models and Alembic migrations
- SM-2 SRS algorithm implemented from scratch in `services/srs.py`
- Unit tests for scheduling logic
- Seed script with initial sentence data

### WP2: FastAPI layer
- `GET /cards/next` - returns next i+1 card for a user
- `POST /reviews` - submits comprehension score, triggers SRS update
- `GET /vocab/{user_id}` - returns known vocabulary with metadata
- Pydantic schemas, JWT authentication, dependency injection

### WP3: NLP pipeline and i+1 scorer
- spaCy tokenisation, lemmatisation, POS tagging on corpus
- Word frequency ranking integrated into card metadata
- `services/scorer.py` - ranks candidate cards by predicted comprehension
- Heuristic baseline (% unknown words), upgradeable to ML model

### WP4: Containerisation and MVP deploy
- Dockerfile for FastAPI app
- Docker Compose for local dev (API + DB)
- Deploy to Railway via Docker
- Environment-variable-driven config (no hardcoded credentials)

### WP5: CI/CD and observability
- GitHub Actions: run tests → build image → push to registry → deploy
- Swap SQLite → PostgreSQL (Railway-managed)
- CloudWatch logging and basic latency alarm
- Architecture diagram and API docs (auto-generated via FastAPI)

### WP6: AWS migration (stretch goal)
- Push image to AWS ECR
- Deploy to ECS Fargate
- RDS for PostgreSQL in production
- Full monitoring stack

---

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI + Uvicorn |
| ORM | SQLAlchemy + Alembic |
| Database | SQLite → PostgreSQL |
| NLP | spaCy |
| Containers | Docker |
| CI/CD | GitHub Actions |
| Hosting | Railway → AWS ECS Fargate |
| Observability | CloudWatch |

---

## Status

Work in progress: WP1 in development.
