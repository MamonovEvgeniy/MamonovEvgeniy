#!/bin/bash
owner=$1

# Функция для безопасного вывода
safe_echo() {
    if ! echo "$1"; then
        echo "Error in echo" >&2
        return 1
    fi
}

# Method 1: GitHub GraphQL API (основные репозитории)
echo -e "\n=== Method 1: GitHub GraphQL API ===" >&2
query1='{
  user(login: "'$owner'") {
    contributionsCollection {
      totalCommitContributions
    }
  }
}'
method1=$(curl -s -H "Authorization: bearer $GITHUB_TOKEN" \
  -X POST -d "{\"query\":\"$query1\"}" \
  https://api.github.com/graphql | \
  jq -r '.data.user.contributionsCollection.totalCommitContributions' || echo 0)
safe_echo "$method1" || exit 1

# Method 2: GitHub REST API (по репозиториям)
echo -e "\n=== Method 2: GitHub REST API ===" >&2
repos=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/users/$owner/repos?per_page=100" | \
  jq -r '.[].name')

method2=0
for repo in $repos; do
  count=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/repos/$owner/$repo/contributors" | \
    jq ".[] | select(.login == \"$owner\") | .contributions" || echo 0)
  method2=$((method2 + ${count:-0}))
  echo "Repo $repo: $count commits" >&2
done
safe_echo "$method2" || exit 1

# Method 3: Локальный подсчет через git rev-list (самый точный)
echo -e "\n=== Method 3: Локальный подсчет ===" >&2
method3=0
for repo in $repos; do
  git clone --depth 1 "https://github.com/$owner/$repo.git" "temp_$repo" 2>/dev/null
  if [ -d "temp_$repo" ]; then
    cd "temp_$repo"
    count=$(git rev-list --count --all || echo 0)
    method3=$((method3 + count))
    cd ..
    rm -rf "temp_$repo"
    echo "Repo $repo: $count commits" >&2
  else
    echo "Repo $repo: не удалось клонировать" >&2
  fi
done
safe_echo "$method3" || exit 1

# Вывод всех результатов
echo -e "\n=== Final Results ===" >&2
echo "Method 1 (GraphQL): $method1" >&2
echo "Method 2 (REST API): $method2" >&2
echo "Method 3 (Local git): $method3" >&2

# Выбираем наиболее достоверный метод
if [ "$method3" -ne 0 ]; then
  selected=$method3
elif [ "$method2" -ne 0 ]; then
  selected=$method2
else
  selected=$method1
fi

safe_echo "$selected" || exit 1
