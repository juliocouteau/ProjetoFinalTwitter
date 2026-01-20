# Copilot / AI agent instructions — Projeto-Twitter (meu_twitter)

Purpose: quick orientation for AI coding agents to be immediately productive in this Django app.

- Big picture
  - This is a single Django project with one main app `twitter` (app package: [twitter](twitter)).
  - URL routing: root URLs are in [core/urls.py](core/urls.py) which includes the app routes in [twitter/twitter/urls.py](twitter/twitter/urls.py).
  - Templates live under [twitter/templates/twitter](twitter/templates/twitter) and follow conventional Django template names (e.g. `home.html`, `profile.html`).
  - Custom user model: AUTH_USER_MODEL = `twitter.User` (see [core/settings.py](core/settings.py) and [twitter/models.py](twitter/models.py)).
  - Media uploads: MEDIA_ROOT and MEDIA_URL configured in [core/settings.py](core/settings.py); ImageFields store files under `media/` (profile_pics/ and covers/).

- Key patterns and examples to follow
  - Models: `User` extends `AbstractUser` and exposes `following` as ManyToMany (asymmetric) — use `user.following` and `user.followers` (see [twitter/models.py](twitter/models.py)).
  - Views use decorators like `@login_required` and return template contexts directly; prefer editing the existing views rather than introducing new heavy abstractions (see [twitter/views.py](twitter/views.py)).
  - Forms: registration and profile-edit forms are in [twitter/forms.py](twitter/forms.py). Reuse `CustomUserCreationForm` and `UserUpdateForm` when changing user signup/edit flows.
  - Templates reference `request.user.profile_pic.url` and other `ImageField` URLs — when editing templates, ensure `MEDIA_URL` is handled (see [core/urls.py](core/urls.py) debug static serving).

- Developer workflows (commands)
  - Run locally (dev):
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```
  - Create admin user: `python manage.py createsuperuser`.
  - When changing models (especially `User`): always run `makemigrations` then `migrate`.

- Project-specific quirks & gotchas
  - Custom user model is active; changing fields requires migrations and care — avoid creating a second user model.
  - The app routing file is located at [twitter/twitter/urls.py](twitter/twitter/urls.py) and its import lines look non-standard (it imports `from .twitter import views`). Confirm imports before editing routes — if you add views, prefer `from . import views` or adjust package layout.
  - Media files are served only in DEBUG: static(media) helper is added in [core/urls.py](core/urls.py). In production, media must be served by the web server.
  - Templates use Tailwind-style utility classes; CSS is expected to be provided in templates/static but not tracked here. Keep classes intact when editing markup.

- Integration points & external deps
  - No external APIs are present in the codebase; primary dependencies are Django and Python standard libs (check `venv` for installed versions).
  - Image handling uses `ImageField` — Pillow should be available in environment when uploading images.

- How to make safe changes
  - For model changes: run `python manage.py makemigrations` and `python manage.py migrate` locally; add tests if altering relationships.
  - For view/URL changes: update [twitter/twitter/urls.py](twitter/twitter/urls.py) and corresponding templates under [twitter/templates/twitter](twitter/templates/twitter).
  - When adding fields on `User`, update `UserUpdateForm` in [twitter/forms.py](twitter/forms.py) and templates that show those fields.

- When you get stuck
  - Check `core/settings.py` for DEBUG, AUTH_USER_MODEL and MEDIA settings.
  - Look at template usage in [twitter/templates/twitter/home.html](twitter/templates/twitter/home.html) for examples of context keys (`posts`, `form`, `view_user`).

If any part of this file is unclear or you want me to expand examples (e.g. exact migration steps or a checklist for changing `User`), tell me which section to expand.
