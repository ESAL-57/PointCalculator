# PointCalculator

React frontend with a Django API backend.

## Structure
- `frontend/`: Vite + React app for GitHub Pages.
- `backend/`: Django API server that keeps API keys private.
- `PROJECT_CONTEXT.md`: Project rules Codex should keep referencing.

## Frontend
```bash
cd frontend
npm install
npm run dev
```

Create `frontend/.env.local` when the frontend needs to call a backend:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Create `backend/.env` from `backend/.env.example` and put private values there.

## GitHub Pages
The workflow in `.github/workflows/deploy-frontend.yml` builds `frontend/` and publishes it to GitHub Pages.

In GitHub, open **Settings > Pages** and set the source to **GitHub Actions**.

Add a repository variable named `VITE_API_BASE_URL` with the deployed Django backend URL.

Example:

```env
VITE_API_BASE_URL=https://pointcalculator-api.onrender.com
```

## Backend Hosting
The Django backend must be hosted separately because GitHub Pages cannot run Python servers.

This repo includes `render.yaml` for Render Blueprint deployment.

1. Push this project to GitHub.
2. In Render, create a new Blueprint from this repository.
3. Set the `RIOT_API_KEY` environment variable in Render.
4. Replace these placeholder values after Render gives you real URLs:
   - `render.yaml`: `DJANGO_ALLOWED_HOSTS`
   - `render.yaml`: `CORS_ALLOWED_ORIGINS`
   - GitHub repository variable: `VITE_API_BASE_URL`

For GitHub Pages, the frontend URL is usually:

```text
https://YOUR_GITHUB_USERNAME.github.io/PointCalculator/
```

## API Key Safety
Do not put API keys in `frontend/`. Anything bundled into the React app can be viewed by visitors. Put keys in `backend/.env` and expose only the Django endpoint the frontend should call.

For Riot API access, set:

```env
RIOT_API_KEY=RGAPI-your-api-key
RIOT_REGION=asia
RIOT_PLATFORM=kr
```

## Calculator API
- `GET /api/options/`: positions, tiers, and point limit.
- `POST /api/calculate/`: calculates five player points and team total.
- `POST /api/calculate-player/`: calculates all five position scores for one player.
- `GET /api/riot/player/?gameName=...&tagLine=...`: looks up Riot account, summoner, and ranked entries.
- `GET /api/crawl/player/?gameName=...&tagLine=...`: looks up Riot account and extracts peak-tier data for scoring.
- `GET /api/riot-example/`: checks whether Riot API settings are loaded.

The current rule implementation is in `backend/api/calculator.py`.
