# group-exporter

Export all of your projects and groups from the Epitech Intranet.

## Setup

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

UserScript:

> [!WARNING]
> This requires the Intranet to be set in English language.

> [!NOTE]
> If you have modified the server port, you might need to modify the `SERVER_URL` if needed

Install [Tampermonkey](https://tampermonkey.net) and then import the `group-exporter.user.js` script.

