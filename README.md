# testing

Internal test tooling for the SwayRider platform.

## Contents

- [Bruno Collections](#bruno-collections)
- [Local Redis](#local-redis)

## Bruno Collections

Two Bruno collections, covering the two ways to reach SwayRider services locally:

| Folder | Surface | Contents |
|---|---|---|
| `bruno/internal/` | Direct per-service calls, bypassing the gateway | `Login/`, `AuthService/`, `MailService/`, `RegionService/`, `RouterService/`, `SearchService/`, `TilesService/`, `Valhalla-Pelias/` (direct Valhalla/Pelias testing) |
| `bruno/public/` | Gateway-facing surface, routed through `swayrider-api` | `API/` — `Login/`, `Auth/` (including admin), `Search/`, `Region/`, `Route/`, `Tiles/`, `Web/`, `OpenAPI`, `Health` |

Both share the same login/token-extraction pattern; login and token capture live in the `Login` folder of each collection.

### Getting Started

1. Install [Bruno](https://www.usebruno.com/).
2. Open the collection: **File → Open Collection** → select `bruno/internal/` or `bruno/public/` depending on which surface you're testing.
3. Copy the environment template and fill in your values, e.g. for the internal collection:
   ```bash
   cp bruno/internal/environments/SwayRider-Dev.bru.example \
      bruno/internal/environments/SwayRider-Dev.bru
   ```
   (same pattern for `bruno/public/environments/`). These files are gitignored (`bruno/**/environments/*.bru` in `.gitignore`) and never committed.
4. Run **Login/Login User** or **Login/Login Admin** — `access_token` and `refresh_token` are captured automatically for subsequent requests.

### Public collection manual test order

For a complete gateway pass, use a verified user token for `[L]` requests and an admin token for `[A]` requests. The request suffixes are a quick guide: `[-]` public, `[L]` logged-in/verified user, `[A]` admin, and `[T]` requires a token copied from an email or another response.

1. Run **Health**, **OpenAPI Spec**, **Auth/Public Keys**, and the public web requests.
2. Run **Login/Login User** with a verified user, then run **Auth/Who Am I**, **Auth/Me**, password management, all **Search**, **Region**, **Route**, and **Tiles** requests. Region and tiles are protected by the gateway even when their upstream endpoint is public.
3. Run **Auth/Login Admin**, then run every request in **Auth/Admin**, **Auth/Service Clients**, and **Auth/Invites**. Create/list/delete the service client in that order; invite/list/revoke the invite in that order.
4. For registration, password reset, and email verification, use fresh addresses and copy the `user_id`/token values from the email into `verification_user_id`, `verification_token`, `reset_password_user_id`, and `reset_password_token` before running the `[T]` requests. The request endpoints only send email; they do not return the token.
5. Run **Auth/Logout** last for the session being tested. Re-run login if the single-use refresh token has already been rotated.

The public collection now has one or more requests for every gateway route, including the OpenAPI document, all admin operations, all region operations, all three tile shapes (ping/styles/tile), and the gateway web pages.

### Environment Variables

All variables are defined in each collection's `environments/*.bru.example` file. Typical variables:

| Variable | Description |
|---|---|
| `AUTHSERVICE_HOST` / `AUTHSERVICE_PORT` | Auth service address (internal collection) |
| `API_HOST` / `API_PORT` | Gateway address (public collection) |
| `ADMIN_USER` / `ADMIN_PASSWORD` | Admin credentials |
| `USER_EMAIL` / `USER_PASSWORD` | Regular user credentials |
| `REGISTER_EMAIL` | Fresh address used by the registration request |
| `INVITE_EMAIL` | Address used by the admin invite lifecycle |
| `NEW_ADMIN_EMAIL` | Fresh address used by the create-admin request |
| `verification_user_id` / `verification_token` | Values copied from a verification email for the `[T]` web request |
| `reset_password_user_id` / `reset_password_token` | Values copied from a password-reset email for the `[T]` requests |

`access_token` and `refresh_token` are populated automatically after a successful login.

## Local Redis

`infra/redis/compose.yml` runs a local Redis instance on port `36379`, needed when exercising `swayrider-api`'s rate limiting and Redis Streams queue against the **public** Bruno collection (the gateway requires Redis to be reachable; direct per-service testing via the internal collection does not need it).

```bash
docker compose -f infra/redis/compose.yml up -d
```
