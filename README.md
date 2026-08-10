# RepoBase

![RepoBase](https://via.placeholder.com/1200x630/0a0a0b/6366f1?text=RepoBase+-+The+OS+for+Your+Repositories)

**A premium developer workspace for organizing and managing repositories.** 
RepoBase transforms your workflow by combining the familiarity of version control dashboards with the speed and precision of a power-user command center. Built for speed, designed for elegance.

## 🚀 The "GitHub on Steroids" Experience

RepoBase is not just another CRUD app. It is a highly-interactive, low-latency Single Page Application (SPA) designed to feel like a modern personal operating system for your projects.

### ✨ Key Features
- **Premium Dark Mode**: Meticulously crafted layers, glassmorphism, and animated ambient mesh gradients.
- **Command Palette (`⌘K`)**: A Raycast-inspired instant search and command execution center. Navigate anywhere without touching your mouse.
- **Deterministic Visual Identities**: Every repository is automatically assigned a unique geometric color signature based on cryptographic hashing of its name.
- **Lightning Fast SPA Architecture**: Intelligent skeleton loaders, optimistic UI updates, and zero-latency modal interactions.
- **Intelligent Dashboards**: Real-time insights into your development universe.

## 🏗️ Architecture

RepoBase is built on a robust, modern stack that prioritizes both developer experience and production scalability.

- **Backend**: Django & Django Ninja (Asynchronous, High-Performance REST APIs)
- **Database**: SQLite / PostgreSQL (Production)
- **Frontend**: Vanilla JavaScript (ES6+), CSS3 Variables & Flexbox/Grid
- **Authentication**: Secure Session-based Auth with strictly enforced CSRF protection.

### API Overview

The RepoBase REST API is fully typed and interactive.

- `GET /api/repos` — List all accessible repositories.
- `GET /api/repos/{id}` — Fetch detailed metadata and increment view counts.
- `POST /api/repos` — Create a new repository securely.
- `PUT /api/repos/{id}` — Update repository settings and tags.
- `DELETE /api/repos/{id}` — Permanently delete a repository.

## 🛠️ Getting Started

### Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/thrilokmanjunath/RepoBase.git
   cd RepoBase
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python repobase_project/manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python repobase_project/manage.py runserver
   ```

Visit `http://localhost:8000` to access your new workspace.

### Testing

We maintain a rigorous test suite using `pytest`.
```bash
pytest repobase_project/
```

### Deployment

RepoBase is optimized for serverless deployments on platforms like **Vercel**.
It utilizes `whitenoise` for optimized static file delivery in production.
A specialized `index.py` handles WSGI application routing for the Vercel `@vercel/python` runtime.

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `⌘ + K`  | Open Command Palette |
| `N`      | Create New Repository |
| `/`      | Focus Search or Palette |
| `Esc`    | Close Modals / Unfocus Inputs |

## 🗺️ Roadmap

- [ ] GitHub OAuth Integration
- [ ] Real-time WebSockets for Activity Feeds
- [ ] Advanced Repository Analytics & Insights
- [ ] Team Collaboration Workspaces

---
*Built with precision for developers.*
