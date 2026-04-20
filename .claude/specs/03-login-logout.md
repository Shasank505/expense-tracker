# Spec: Login and Logout

## Overview
Implement session-based authentication with login and logout. Users log in with email and password (validated against the hashed password in the database), get a session cookie, and can log out. Placeholder routes get protected with a login_required decorator.

## Depends on
- Step 01: Database Setup (users table with password_hash)

## Routes

### New / Modified routes
- `GET/POST /login` — authenticate user — public (already exists, needs implementation)
- `GET /logout` — clear session, redirect to landing — logged-in only
- `POST /register` — create account — public (placeholder, already exists)

### Protected routes (add login_required)
- `/profile` — logged-in only
- `/expenses/add` — logged-in only
- `/expenses/<int:id>/edit` — logged-in only
- `/expenses/<int:id>/delete` — logged-in only

## Database changes
No new tables or columns. Authentication uses existing `users` table.

## Templates
- **Modify:** `templates/login.html` — add flash message display, form already correct
- **Modify:** `templates/base.html` — show user name in navbar when logged in, show login/register links when not

## Files to change
- `app.py` — add secret key, login_required decorator, implement login/logout routes, protect placeholder routes
- `templates/login.html` — add flash/feedback display
- `templates/base.html` — conditional navbar auth section

## Files to create
- `database/auth.py` — `login_required` decorator and `get_current_user()` helper

## New dependencies
No new pip packages.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords verified with `werkzeug.security.check_password_hash`
- Use Flask `session` for session management
- Set `app.secret_key` in app.py (use a hardcoded dev key for now)
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values

## Definition of done
- [ ] `/login` POST with correct email/password redirects to profile with no error
- [ ] `/login` POST with wrong password shows error on login page
- [ ] `/login` POST with unknown email shows error on login page
- [ ] `/logout` clears session and redirects to `/`
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] Visiting `/expenses/add` while logged out redirects to `/login`
- [ ] Logged-in user name appears in navbar
- [ ] After login, navbar shows logout link instead of login/register
