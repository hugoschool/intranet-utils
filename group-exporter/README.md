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

```sh
make
```

> Modify the `SERVER_URL` if needed
