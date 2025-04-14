#!/bin/bash
owner=$1

# Дата регистрации через GitHub API
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/users/$owner" | \
  jq -r '.created_at' | \
  cut -d'T' -f1
