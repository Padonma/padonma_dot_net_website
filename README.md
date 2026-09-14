# Padonma.net

This repository contains the Padonma.net Hugo site and a few development
utilities, including the rMQR-code generator in `bandgrinder/`.

## Python utilities

The Python dependencies are managed with [uv](https://docs.astral.sh/uv/).
After cloning the repository, install the pinned development environment:

```sh
uv sync
```

Run the rMQR generator in that environment:

```sh
uv run python bandgrinder/bandgrinder.py
```

`uv.lock` is committed so that every developer receives the same resolved
dependency versions. Do not commit the generated `.venv/` directory.
