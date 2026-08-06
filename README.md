# RepoBase - Modern Repository Management

![Build Status](https://img.shields.io/github/actions/workflow/status/your-org/repobase/ci.yml?branch=main)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

RepoBase is a premium, high-performance platform for managing repositories, tags, and bookmarks. This project has been modernized to enterprise standards using a hybrid monolithic and API-driven architecture.

## Features

- **Blazing Fast API**: Powered by Django Ninja with pydantic schemas.
- **Premium UI**: Modern glassmorphism, responsive grid layouts, and dynamic JS interactions.
- **Security**: Built-in CSRF, XSS, and secure header protection.
- **Testing**: Comprehensive Pytest suite covering auth, models, and APIs.
- **DevOps**: Docker and GitHub Actions CI/CD ready.

## Installation

1. Clone the repository
```bash
git clone https://github.com/your-org/repobase.git
cd repobase
```

2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
cd repobase_project
python manage.py migrate
```

5. Start the development server
```bash
python manage.py runserver
```

## Architecture

* **Backend**: Django 5.2.8
* **API**: Django Ninja 1.6
* **Database**: SQLite (Configured for easy swap to PostgreSQL)
* **Frontend**: Django Templates + Vanilla CSS + ES6 JavaScript
* **Auth**: Django session-based authentication

## Deployment

### Vercel
A `vercel.json` is provided for serverless deployment using the `@vercel/python` builder. Ensure your `SECRET_KEY` is configured in Vercel environment variables.

### Docker
A `Dockerfile` is included for containerized environments (Render, AWS, DigitalOcean).

```bash
docker build -t repobase .
docker run -p 8000:8000 repobase
```
