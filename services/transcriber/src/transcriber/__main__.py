"""Run the transcription service with `python -m transcriber`."""

import os

import uvicorn

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9000


def main() -> None:
    """Start the HTTP server using the network settings from the environment."""
    host = os.environ.get("TRANSCRIBER_HOST", DEFAULT_HOST)
    port = int(os.environ.get("TRANSCRIBER_PORT", DEFAULT_PORT))
    uvicorn.run("transcriber.main:app", host=host, port=port)


if __name__ == "__main__":
    main()
