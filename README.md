# testing

Internal test tooling for the SwayRider platform.

## Contents

- [Bruno Collections](#bruno-collections)
- [Local Redis](#local-redis)

## Bruno Collections

Two Bruno collections, covering the two ways to reach SwayRider services locally:

| Folder | Surface | Contents |
|---|---|---|
| `bruno/internal/` | Direct per-service calls, bypassing the gateway | `Login/`, `AuthService/` (including `MFA/`), `MailService/`, `RegionService/`, `RouterService/`, `SearchService/`, `TilesService/`, `Valhalla-Pelias/` (direct Valhalla/Pelias testing) |
| `bruno/public/` | Gateway-facing surface, routed through `swayrider-api` | `API/` — `Login/`, `Auth/` (including `MFA/` and admin), `Search/`, `Region/`, `Route/`, `Tiles/`, `Web/`, `OpenAPI`, `Health` |

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

### MFA flow (TOTP second factor)

Run the requests in **Auth/MFA** in order — enrollment, then challenge/verify:

1. **Setup MFA [L]** — returns the base32 `secret` (captured to `mfa_secret`), the otpauth URL, and a QR PNG. Add the secret to an authenticator app, or generate codes with a CLI tool (`oathtool --base32 --totp <secret>`).
2. **Enable MFA [L]** — enter a current TOTP code in the `mfa_code` environment variable and run; the fresh backup-code set is returned (captured to `mfa_backup_codes`). Save these — they are shown only once.
3. **MFA Status [L]** — should now return `{"enabled": true}`.
4. **Login (MFA enabled) [-]** — the account now has MFA, so login returns `mfa_required: true` plus a single-use `mfa_token` (captured automatically) and **no** tokens or cookies.
5. **Verify MFA [-]** — set `mfa_code` to a current TOTP code (or a backup code) and run; on success the normal `access_token`/`refresh_token` pair is returned and captured, exactly like a completed login.
6. **Regenerate Backup Codes [L]** — replaces the backup-code set (old codes stop working) and returns the new ones once.
7. **Disable MFA [L]** — removes MFA from the account (requires the account password); login returns tokens again afterwards.

Notes:

- `mfa_code` must be entered manually in the environment and refreshed per request — TOTP codes rotate every 30 seconds and a challenge/backup code is single-use.
- `mfa_token`, `mfa_secret`, and `mfa_backup_codes` are captured by the request scripts; they do not need to be declared in the environment.
- The **internal** collection's `AuthService/MFA` folder exercises the same flow directly against authservice (camelCase JSON, per grpc-gateway's marshaling), bypassing the gateway — useful for isolating a service-side failure from a gateway one.

The public collection now has one or more requests for every gateway route, including the OpenAPI document, all admin operations, all region operations, all three tile shapes (ping/styles/tile), the MFA flow, and the gateway web pages.

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
| `mfa_code` | Current TOTP code (or backup code) for the MFA flow — must be refreshed manually per request |

`access_token` and `refresh_token` are populated automatically after a successful login.

## Local Redis

`infra/redis/compose.yml` runs a local Redis instance on port `36379`, needed when exercising `swayrider-api`'s rate limiting and Redis Streams queue against the **public** Bruno collection (the gateway requires Redis to be reachable; direct per-service testing via the internal collection does not need it).

```bash
docker compose -f infra/redis/compose.yml up -d
```

## Local Postgres

`infra/postgres/compose.yml` runs a local Postgres instance on port `35432`, needed when running `authservice` locally (it runs the DB migrations at startup). The container's credentials come from the `SWAYRIDER_LOCAL_POSTGRES_USER` / `SWAYRIDER_LOCAL_POSTGRES_PASSWORD` / `SWAYRIDER_LOCAL_POSTGRES_DB` vars (defaults `postgresadmin` / `postgrespassword` / `authdb`, matching `.vscode/environment.example`), so no extra configuration is required — and they are deliberately separate from the deployed dev system's `SWAYRIDER_DB_*` secrets.

```bash
docker compose -f infra/postgres/compose.yml up -d
```

Data is persisted in the `sw-test-postgres-data` named volume. To start from a clean slate:

```bash
docker compose -f infra/postgres/compose.yml down -v
docker compose -f infra/postgres/compose.yml up -d
```
