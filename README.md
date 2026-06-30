# FastAPI Banking API

A simple banking backend built with FastAPI, PostgreSQL and SQLAlchemy Async.

## Features

- JWT Authentication
- User Registration & Login
- Bank Account Creation
- Deposits
- Withdrawals
- Transaction History
- Repository-Service Architecture
- Alembic Database Migrations

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy Async
- Alembic
- JWT Authentication
- uv

## Setup

Install dependencies

```bash
uv sync
```

Copy environment variables

```bash
cp .env.example .env
```

Run migrations

```bash
uv run alembic upgrade head
```

Start the server

```bash
uv run uvicorn app.main:app --reload
```

Open

```
http://localhost:8000/docs
```

## Project Structure

```
app/
├── api/
├── core/
├── db/
├── enums/
├── models/
├── repositories/
├── schemas/
└── services/
```

## Status

Current features

- Authentication
- Account Management
- Deposits
- Withdrawals
- Transaction History

Work in progress

- Transfers
- Account Statements
- Admin APIs
- Unit Tests