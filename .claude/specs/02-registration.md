# Spec: Registration

## Overview

Implement user registration functionality for the Spendly expense tracker. This feature allows new users to create an account by providing their name, email, and password. The registration page already exists as a placeholder route; this step implements the full backend logic, form validation, password hashing, and user creation in the database.

## Depends on

- Step 01 (Database Setup) — the `users` table must exist with the correct schema

## Routes

- `GET /register` — display registration form — public (already implemented)
- `POST /register` — handle registration submission — public (new)

## Database changes

No database changes — the `users` table from Step 01 is sufficient.

## Templates

- **Modify:** `templates/register.html` — add form with proper input fields, CSRF token, and error display

## Files to change

- `app.py` — add POST handler for `/register` with form processing
- `templates/register.html` — add registration form with name, email, password fields

## Files to create

- `database/db.py` — add `create_user(name, email, password_hash)` function

## New dependencies

No new dependencies.

## Rules for implementation

- No SQLAlchemy or ORMs — use raw SQLite with parameterized queries
- Passwords must be hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate all inputs on the server side:
  - Name: required, non-empty
  - Email: required, valid format, unique
  - Password: required, minimum length (e.g., 6 characters)
- Display user-friendly error messages for validation failures
- On successful registration, redirect to `/login`

## Definition of done

- [ ] Registration form displays with name, email, and password fields
- [ ] Form submission validates all inputs server-side
- [ ] Duplicate email is rejected with appropriate error message
- [ ] Password is hashed before storing in database
- [ ] New user is inserted into `users` table via `create_user()` function
- [ ] Successful registration redirects to `/login` page
- [ ] Error messages display above the form
- [ ] Form includes CSRF protection
- [ ] All SQL queries use parameterized statements
