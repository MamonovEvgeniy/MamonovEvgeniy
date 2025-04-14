#!/bin/bash
owner=$1
current_year=$(date +%Y)

# Method 1: GitHub API events with since parameter
echo "Method 1: GitHub API events with since" >&2
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/users/$owner/events?since=$current_year-01-01T00:00:00Z&per_page=100" | \
  jq -r '[.[] | select(.type == "PushEvent") | .payload.commits[] | {message: .message, sha: .sha, url: .url}] | unique_by(.sha)'

# Method 2: GitHub Search API with date range
echo -e "\nMethod 2: GitHub Search API with date range" >&2
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/search/commits?q=author:$owner+committer-date:>=$current_year-01-01&per_page=100" | \
  jq -r '[.items[] | {message: .commit.message, sha: .sha, html_url: .html_url}] | unique_by(.sha)'

# Method 3: Using GitHub REST API per repo with since parameter
echo -e "\nMethod 3: GitHub REST API per repo with since" >&2
repos=$(curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/users/$owner/repos?per_page=100" | \
  jq -r '.[].name')

all_repo_commits=()
for repo in $repos; do
  repo_commits=$(curl -s \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/$owner/$repo/commits?since=$current_year-01-01T00:00:00Z&per_page=100" | \
    jq -r '[.[] | {message: .commit.message, sha: .sha, html_url: .html_url}]')
  all_repo_commits+=("$repo_commits")
done

printf '%s\n' "${all_repo_commits[@]}" | jq -s 'add | unique_by(.sha)'

# Method 4: Using GitHub GraphQL API with date filter (fixed)
echo -e "\nMethod 4: GitHub GraphQL API with date filter" >&2
query=$(cat <<EOF
{
  user(login: "$owner") {
    contributionsCollection(from: "$current_year-01-01T00:00:00Z") {
      commitContributionsByRepository {
        repository {
          name
        }
        contributions(first: 100) {
          nodes {
            commit {
              message
              oid
              url
            }
          }
        }
      }
    }
  }
}
EOF
)
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  -X POST \
  -d "{\"query\": \"$(echo $query | sed 's/"/\\"/g')\"}" \
  https://api.github.com/graphql | \
  jq -r '[.data.user.contributionsCollection.commitContributionsByRepository[].contributions.nodes[].commit | {message: .message, sha: .oid, url: .url}] | unique_by(.sha)'
