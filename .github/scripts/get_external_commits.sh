#!/bin/bash
owner=$1

# Method 1: GitHub Search API excluding own repos
echo "=== Method 1: GitHub Search API excluding own repos ===" >&2
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/search/commits?q=author:$owner+-user:$owner&per_page=100" | \
  jq -r '.total_count'
