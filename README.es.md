# TranscriptDeck

> **Requiere una Mac con Apple Silicon (M1 o posterior).** El servicio de transcripción utiliza la GPU de Apple y no funciona en Mac con procesador Intel, Linux ni Windows.

[Read in English](README.md)

TranscriptDeck es una aplicación web de código abierto que transcribe videos de forma local en su Mac. Ningún dato sale de su equipo.

El proyecto se encuentra en una etapa inicial: esta versión contiene la estructura base del proyecto y la comprobación de estado entre sus tres servicios. La transcripción se incorporará en fases posteriores.

## Requisitos previos

- Una Mac con Apple Silicon
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (ejecuta la aplicación web y la API)
- [uv](https://docs.astral.sh/uv/) (ejecuta el servicio de transcripción de forma nativa)
- [ffmpeg](https://ffmpeg.org/) (`brew install ffmpeg`; se utilizará en fases posteriores)

## Inicio rápido

1. Inicie el servicio de transcripción de forma nativa. Los contenedores en macOS no tienen acceso a la GPU, por lo que este servicio se ejecuta fuera de Docker:

   ```sh
   cd services/transcriber
   uv run python -m transcriber
   ```

2. En otra terminal, inicie la aplicación web y la API desde la raíz del repositorio:

   ```sh
   docker compose up --build
   ```

3. Abra <http://localhost:8080>. La página muestra el estado de la API y del servicio de transcripción.

### Configuración de red del servicio de transcripción

De forma predeterminada, el servicio de transcripción escucha en `127.0.0.1:9000`. Ambos valores se pueden cambiar mediante variables de entorno:

| Variable           | Valor predeterminado | Descripción                              |
| ------------------ | -------------------- | ---------------------------------------- |
| `TRANSCRIBER_HOST` | `127.0.0.1`          | Dirección en la que escucha el servicio  |
| `TRANSCRIBER_PORT` | `9000`               | Puerto en el que escucha el servicio     |

El contenedor de la API accede al servicio en `http://host.docker.internal:9000` (definido mediante `TRANSCRIBER_URL` en `docker-compose.yml`).

## Estructura del proyecto

```text
apps/web               Interfaz web (React, Vite, TypeScript, Tailwind CSS). Se ejecuta en Docker.
apps/api               Servidor (Python, FastAPI). Se ejecuta en Docker.
services/transcriber   Servicio de transcripción (Python, FastAPI). Se ejecuta de forma nativa en macOS.
```

Los tres proyectos son independientes y se comunican entre sí únicamente mediante HTTP:

| Servicio    | Puerto | Notas                                                        |
| ----------- | ------ | ------------------------------------------------------------ |
| web         | 8080   | nginx sirve la aplicación y redirige `/api` hacia la API     |
| api         | 8000   | obtiene la dirección del servicio de transcripción de `TRANSCRIBER_URL` |
| transcriber | 9000   | se ejecuta en el equipo anfitrión                            |

## Desarrollo

### Web (`apps/web`)

```sh
npm install
npm run dev         # servidor de desarrollo; redirige /api a http://localhost:8000
npm run test        # pruebas unitarias (una sola ejecución)
npm run check       # análisis estático y verificación de formato con Biome
npm run typecheck   # TypeScript
npm run build       # compilación de producción
```

### API (`apps/api`) y servicio de transcripción (`services/transcriber`)

Ejecute estos comandos dentro del directorio de cada proyecto:

```sh
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Para ejecutar la API fuera de Docker:

```sh
cd apps/api
uv run uvicorn api.main:app --port 8000
```

### Hooks de Git

El repositorio utiliza [Lefthook](https://lefthook.dev/) para analizar los archivos preparados antes de cada commit (Biome para la aplicación web, Ruff para Python). Instale los hooks una vez después de clonar el repositorio:

```sh
brew install lefthook
lefthook install
```

## Licencia

[MIT](LICENSE)
