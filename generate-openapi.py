#!/usr/bin/env python3
import json

from fastapi.openapi.utils import get_openapi

from mount.app.api_boot import api

openapi_schema = get_openapi(
    title=api.title,
    version=api.version,
    openapi_version=api.openapi_version,
    description=api.description,
    routes=api.routes,
)

with open("openapi.json", "w+") as f:
    f.write(json.dumps(openapi_schema, indent=2))
