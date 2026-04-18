#!/usr/bin/env bash

curl -X POST \
    --header "Content-Type: application/json" \
    --data '{"module": {"code": "code"}, "project": {"name": "name"}, "content": []}' \
    http://127.0.0.1:8000/group-page
