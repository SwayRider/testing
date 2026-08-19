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
| `bruno/public/` | Gateway-facing surface, routed through `swayrider-api` | `API/` — `Login/`, `Auth/`, `Search/`, `Region/`, `Route/`, `Health` |

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

### Environment Variables

All variables are defined in each collection's `environments/*.bru.example` file. Typical variables:

| Variable | Description |
|---|---|
| `AUTHSERVICE_HOST` / `AUTHSERVICE_PORT` | Auth service address (internal collection) |
| `API_HOST` / `API_PORT` | Gateway address (public collection) |
| `ADMIN_USER` / `ADMIN_PASSWORD` | Admin credentials |
| `USER_EMAIL` / `USER_PASSWORD` | Regular user credentials |

`access_token` and `refresh_token` are populated automatically after a successful login.

## Local Redis

`infra/redis/compose.yml` runs a local Redis instance on port `36379`, needed when exercising `swayrider-api`'s rate limiting and Redis Streams queue against the **public** Bruno collection (the gateway requires Redis to be reachable; direct per-service testing via the internal collection does not need it).

```bash
docker compose -f infra/redis/compose.yml up -d
```
