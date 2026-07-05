# group-exporter

Export all of your projects and groups from the Epitech Intranet.

# Setup

`server`:

Using `uv`

```sh
# Install dependencies
uv sync

# Create venv
uv venv
source .venv/bin/activate

# Launch the server locally
fastapi dev
```

`extension`:

> [!WARNING]
> The extension requires the Intranet to be set in English language.

```sh
make
```

> Modify the `SERVER_URL` if needed
