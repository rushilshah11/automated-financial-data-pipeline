# JWT Authentication & Authorization — Workflow Summary

This document summarises how JWT-based authentication and authorization work in this project for the Signup (register), Login and Protected routes. It includes request/response shapes, token lifecycle, error cases, security notes, and pointers to the source code that implements each step.

## Quick overview
- Clients register (signup) by sending first_name, last_name, email and password.
- Passwords are hashed (bcrypt) and stored in the DB.
- Clients login with email and password. If valid, the server returns a signed JWT.
- Clients include the JWT on subsequent requests in the `Authorization` header as `Bearer <token>`.
- The server validates the token, extracts the user id, and returns a user object (or denies access).

## Data shapes

- Register request (JSON body):

```json
{
  "first_name": "Alice",
  "last_name": "Example",
  "email": "alice@example.com",
  "password": "plaintext-password"
}
```

- Register response (UserOutput):

```json
{
  "id": 1,
  "first_name": "Alice",
  "last_name": "Example",
  "email": "alice@example.com"
}
```

- Login request (JSON body):

```json
{
  "email": "alice@example.com",
  "password": "plaintext-password"
}
```

- Login response (expected):

```json
{
  "token": "eyJhbGciOi..."
}
```

> Note: the current implementation returns a JWT (and in some versions only the token). The router expects the `UserWithToken` Pydantic model which has token. 

## Token contents and lifetime
- The token payload includes at least:
  - `user_id`: integer primary key of the authenticated user
  - `exp`: unix timestamp expiration (e.g. `time() + 900` for 15 minutes)
- Tokens are signed with the secret `JWT_SECRET_KEY` and algorithm `JWT_ALGORITHM` (configured in `app/settings.py`, read from `.env`).

## Signup flow (server-side steps)
1. Receive `UserInRegister` payload at `POST /auth/register`.
2. Validate body using Pydantic (`app/db/schemas/user_schema.py`).
3. Check for existing user with same email via `UserRepository.user_exist_by_email`.
4. Hash plaintext password using `HashHelper.get_password_hash` and replace the value in the model.
5. Create the user record with `UserRepository.create_user` (commits to DB).
6. Return `UserOutput` (id, first_name, last_name, email).

Files: `app/service/user_service.py`, `app/db/repository/user_repo.py`, `app/core/security/hashHelper.py`.

## Login flow (server-side steps)
1. Receive `UserInLogin` payload at `POST /auth/login`.
2. Validate payload via Pydantic.
3. Look up user by email (repository).
4. If user not found -> HTTP 400 (Invalid email or password).
5. Verify password with `HashHelper.verify_password(plain, hashed)` (bcrypt check).
6. If password mismatch -> HTTP 400 (Invalid password).
7. If OK, generate a JWT with `AuthHandler.encode_token(user_id=...)`.
8. Return `UserWithToken` containing the `user` output and `token`.

Files: `app/service/user_service.py`, `app/core/security/authHandler.py`, `app/core/security/hashHelper.py`.

## Protected route flow (server-side steps)
1. The client sends `Authorization: Bearer <token>` header.
2. `get_current_user` (dependency in `app/util/protect_route.py`) extracts the header, removes the `Bearer ` prefix, and decodes the token using `AuthHandler.decode_token`.
3. If decode fails or token expired -> raise HTTP 401 (Unauthorized).
4. From the token payload pull `user_id` and fetch the user via `UserService.get_user_by_id`.
5. Return a `UserOutput` instance which the protected route can use.

Files: `app/util/protect_route.py`, `app/core/security/authHandler.py`, `app/service/user_service.py`.

## Error cases and messages
- 400 Bad Request: registration with duplicate email — message: "Email already registered. Please Login!"
- 400 Bad Request: login with invalid email or password — message: "Invalid email or password. Create Account!" or "Invalid password. Please try again!"
- 401 Unauthorized: protected route when token missing/invalid/expired — message: "Invalid or expired token. Please log in again."
- 500 Internal Server Error: token generation failure (rare) — message: "Token generation failed. Please try again!"

## Security considerations
- Do NOT store plaintext passwords. Always store bcrypt (or another secure) hashes. This project uses bcrypt via `HashHelper`.
- Keep `JWT_SECRET_KEY` secret and rotate it appropriately.
- Short-lived access tokens (e.g., 15 minutes) are safer; consider issuing refresh tokens for longer sessions.
- Use HTTPS in production to protect Authorization headers in transit.
- Consider adding token revocation (blacklist) or a token version in the DB for manual logout.

## Testing checklist
- Unit test HashHelper hashing & verification.
- Unit test AuthHandler encode/decode behavior and expiration handling.
- Integration tests for register/login/protected already exist in `tests/test_auth_flow.py` — they create unique users.

## Troubleshooting tips
- If you see `ValidationError` on login response, ensure the `UserWithToken` response model matches what `login_user` returns (both `user` and `token`).
- If protected route returns 401 unexpectedly, check:
  - that the Authorization header starts with `Bearer ` (capitalization matters in the current helper),
  - token expiration time, and
  - the `JWT_SECRET_KEY` and algorithm match between encode/decode.

## Where to look in the codebase
- Register/Login endpoints: `app/routers/auth.py`
- Request/response schemas: `app/db/schemas/user_schema.py`
- Business logic: `app/service/user_service.py`
- DB repositories: `app/db/repository/*.py`
- Password hashing: `app/core/security/hashHelper.py`
- JWT handling: `app/core/security/authHandler.py`
- Protected dependency: `app/util/protect_route.py`