# TranscriptDeck

> **Requires a Mac with Apple Silicon (M1 or later).** The transcription service uses the Apple GPU and does not run on Intel Macs, Linux or Windows.

[Leer en español](README.es.md)

TranscriptDeck is an open-source web app that transcribes videos locally on your Mac. Nothing leaves your machine.

The project is in an early stage: this version contains the project skeleton and the health wiring between its three services. Transcription itself arrives in later phases.

## Prerequisites

- A Mac with Apple Silicon
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (runs the web app and the API)
- [uv](https://docs.astral.sh/uv/) (runs the transcription service natively)
- [Node.js](https://nodejs.org/) with npm (web development commands and the Biome Git hook; CI uses Node.js 24; not needed to run the app with Docker)
- [ffmpeg](https://ffmpeg.org/) (`brew install ffmpeg`; used by later phases)

## Quick start

1. Start the transcription service natively. Containers on macOS have no GPU access, so this service runs outside Docker:

   ```sh
   cd services/transcriber
   uv run python -m transcriber
   ```

2. In another terminal, start the web app and the API from the repository root:

   ```sh
   docker compose up --build
   ```

3. Open <http://localhost:8080>. The page shows the status of the API and of the transcription service.

### Transcriber network settings

The transcription service listens on `127.0.0.1:9000` by default. Both values can be changed with environment variables:

| Variable           | Default     | Description               |
| ------------------ | ----------- | ------------------------- |
| `TRANSCRIBER_HOST` | `127.0.0.1` | Address the service binds |
| `TRANSCRIBER_PORT` | `9000`      | Port the service binds    |

The API container reaches the service at `http://host.docker.internal:9000` (set through `TRANSCRIBER_URL` in `docker-compose.yml`).

## Project layout

```text
apps/web               Front end (React, Vite, TypeScript, Tailwind CSS). Runs in Docker.
apps/api               Back end (Python, FastAPI). Runs in Docker.
services/transcriber   Transcription service (Python, FastAPI). Runs natively on macOS.
```

The three projects are independent and talk to each other only over HTTP:

| Service     | Port | Notes                                         |
| ----------- | ---- | --------------------------------------------- |
| web         | 8080 | nginx serves the app and proxies `/api`       |
| api         | 8000 | reads the transcriber address from `TRANSCRIBER_URL` |
| transcriber | 9000 | runs on the host                              |

## Development

### Web (`apps/web`)

Run these from `apps/web`:

```sh
cd apps/web
npm install
npm run dev         # dev server; proxies /api to http://localhost:8000
npm run test        # unit tests (single run)
npm run check       # Biome lint and format check
npm run typecheck   # TypeScript
npm run build       # production build
```

### API (`apps/api`) and transcriber (`services/transcriber`)

Run these from the directory of the project you are working on:

```sh
cd apps/api        # or: cd services/transcriber
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

To run the API outside Docker:

```sh
cd apps/api
uv run uvicorn api.main:app --port 8000
```

### Git hooks

The repository uses [Lefthook](https://lefthook.dev/) to lint staged files before each commit (Biome for the web app, Ruff for Python). Install the hooks once after cloning, from the repository root:

```sh
brew install lefthook
lefthook install
```

The Biome hook uses the copy installed in `apps/web/node_modules`, so run `npm install` in `apps/web` before committing web files.

## License

[MIT](LICENSE)
