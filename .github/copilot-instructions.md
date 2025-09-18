<!--
Project: VoteSec
Purpose: Provide concise, actionable instructions for AI coding agents (Copilot / coding agents)
--> 

# Copilot / AI agent instructions for VoteSec

Short summary
- This is a small Django project (Django 5.x) named `VoteSec`. Primary app is `users` and the project settings live in `votesec/settings.py`.
- Database: SQLite (file `db.sqlite3` by default). Authentication uses a custom user model: `AUTH_USER_MODEL = 'users.User'` in `votesec/settings.py`.

What you should know (big picture)
- The repo is a single Django project (no external services). Entrypoint: `manage.py`.
- URL routing is minimal: `votesec/urls.py` currently only exposes the Django admin at `/admin/`.
- The `users` app exists but contains only scaffolding (`models.py`, `views.py`, `tests.py` are mostly empty). Changes to authentication, user fields, or admin customization should be done under `users/` and wired via `votesec/settings.py`.

Developer workflows & commands
- Use a Python virtual environment (repo contains a `venv/` directory but treat it as local/dev — prefer creating your own `venv` for PRs). Typical commands (PowerShell):

```powershell
# create venv (if needed)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies (project currently has no requirements file)
pip install django==5.2.6

# make migrations / apply migrations
python manage.py makemigrations
python manage.py migrate

# run dev server
python manage.py runserver

# run tests
python manage.py test
```

Project-specific conventions & patterns
- Custom user model: The project sets `AUTH_USER_MODEL = 'users.User'`. If you add fields or change user behavior, edit `users/models.py` and include a corresponding migration. Avoid adding a second user model.
- Minimal URL surface: Add app `urls.py` files and include them from `votesec/urls.py` when expanding the site.
- Settings live in `votesec/settings.py`. Defaults are development friendly (`DEBUG = True`, SQLite). Be conservative when changing `SECRET_KEY` or `DEBUG` — CI or deployments (if added) may expect the current layout.

Using the repository `venv` vs creating a new one
- The repository contains a `venv/` directory (likely created for local development). Prefer creating a fresh local virtual environment for contributions to avoid accidental environment drift or platform-specific binaries:

```powershell
# prefer new venv for PRs
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# if you must use the included venv (not recommended):
.\venv\Scripts\Activate.ps1
```

Code style & linting (recommended)
- The project currently has no style/lint config. Recommended minimal stack for Python/Django:
	- `black` for formatting
	- `isort` for import sorting
	- `flake8` for linting
	- `pre-commit` to run hooks locally

Example quick setup (PowerShell):

```powershell
pip install black isort flake8 pre-commit
pre-commit install
```

Suggested `pre-commit` hooks (add to `.pre-commit-config.yaml` when introducing):
- `black`, `isort`, and a lightweight `flake8` config. Commit this file when adding the toolchain.

Minimal suggested `users.User` schema (example)
- The repo currently sets `AUTH_USER_MODEL = 'users.User'` but `users/models.py` is empty. A low-risk way to start is to subclass `AbstractUser` (keeps username behavior and avoids migration complexity from switching auth backends). Example to place in `users/models.py`:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
		# Keep default username-based auth for stability. Add fields here.
		email = models.EmailField('email address', unique=True)
		is_election_admin = models.BooleanField(default=False)

		def __str__(self):
				return self.username
```

- Notes:
	- After adding this model, run `python manage.py makemigrations users` and `python manage.py migrate` and commit the migration.
	- Avoid changing `AUTH_USER_MODEL` after initial migrations — doing so is disruptive.
	- If you want email-based login (no `username`), create a more involved `AbstractBaseUser` implementation and update `AUTHENTICATION_BACKENDS` and `settings` accordingly.

Integration points & external dependencies
- Currently there are no external services configured (no cache, no external DB, no third-party APIs). If adding integrations, register configuration in `votesec/settings.py` and ensure local development falls back to safe defaults (e.g., environment variables with dev fallbacks).

Files to inspect for common tasks (examples)
- Add user fields / auth: `users/models.py` and `users/admin.py` (to expose in admin). `votesec/settings.py` for `AUTH_USER_MODEL` and INSTALLED_APPS.
- Routing / new endpoints: `votesec/urls.py` and create `users/urls.py` for the app.
- Templates: `TEMPLATES` is configured with `APP_DIRS=True` — place templates under `users/templates/...`.

Edge cases & hints for PRs
- Project is intentionally minimal. When adding dependencies, include a `requirements.txt` or `pyproject.toml` and update README with setup instructions.
- If you add migrations, commit them. The project uses SQLite by default so migrations are portable.
- Keep `DEBUG=False` and secrets out of the repo for production changes.

When you edit files
- Run `python manage.py test` locally before pushing changes.
- If you modify the user model (`users.User`), create migrations and be aware that changing `AUTH_USER_MODEL` after initial migrations can be disruptive.

If anything is unclear or you need more context, ask the maintainers for the intended authentication fields, deployment targets, or CI expectations.
