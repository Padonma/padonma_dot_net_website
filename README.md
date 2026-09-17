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

## Production deployment

Build and validate the production Hugo site locally with:

```sh
scripts/deploy.sh build
```

Deployment targets a private S3 bucket behind CloudFront. AWS provisioning,
required permissions, dry-run, deployment, and cache verification are described
in [docs/aws-deployment.md](docs/aws-deployment.md). Local builds do not require
AWS credentials; `plan` and `deploy` are the only credentialed actions.
