# testing

Internal test tooling for the SwayRider platform.

## Contents

- [REST API Collections](#rest-api-collections)

## REST API Collections

Bruno-based REST collections for all SwayRider services, in `REST/`.
A single unified collection covers every service; login and token extraction
logic is shared rather than duplicated per service.

### Getting Started

1. Install [Bruno](https://www.usebruno.com/).
2. Open the collection: **File → Open Collection** → select the `REST/` folder.
3. Copy the environment template and fill in your values:
   ```bash
   cp REST/environments/SwayRider-Dev.bru.example \
      REST/environments/SwayRider-Dev.bru
   ```
   This file is gitignored and never committed.
4. Run **Login/Login User** or **Login/Login Admin** — `access_token` and
   `refresh_token` are captured automatically for subsequent requests.

### Collection Structure

| Folder | Contents |
|---|---|
| `Login/` | Shared login requests (user, admin, service client token) |
| `AuthService/` | User management, JWT tokens, service clients, email verification |
| `MailService/` | Email sending endpoints |
| `RegionService/` | Spatial region queries and border crossings |
| `RouterService/` | Multi-region route planning |
| `SearchService/` | Geocoding and reverse geocoding |
| `TilesService/` | Map style endpoints |
| `Valhalla-Pelias/` | Direct Valhalla routing and Pelias geocoding (external dep testing) |

### Environment Variables

All variables are defined in `REST/environments/SwayRider-Dev.bru.example`.

| Variable | Description |
|---|---|
| `AUTHSERVICE_HOST` / `AUTHSERVICE_PORT` | Auth service address |
| `AUTHSERVICE_WEB_PORT` | Auth service web port (verification pages) |
| `AUTHSERVICE_ADMIN_USER` / `AUTHSERVICE_ADMIN_PASSWORD` | Admin credentials |
| `USER_EMAIL` / `USER_PASSWORD` | Regular user credentials |
| `MAILSERVICE_HOST` / `MAILSERVICE_PORT` | Mail service address |
| `MAIL_SEND_SERVICE_CLIENT_ID` / `MAIL_SEND_SERVICE_CLIENT_SECRET` | Service client for mail |
| `REGIONSERVICE_HOST` / `REGIONSERVICE_PORT` | Region service address |
| `ROUTERSERVICE_HOST` / `ROUTERSERVICE_PORT` | Router service address |
| `SEARCHSERVICE_HOST` / `SEARCHSERVICE_PORT` | Search service address |
| `TILESSERVICE_HOST` / `TILESSERVICE_PORT` | Tiles service address |

`access_token` and `refresh_token` are populated automatically after a successful login.
