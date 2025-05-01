#!/usr/bin/env python3
import datetime
from pathlib import Path
import os
import sys
from urllib.parse import quote
import subprocess


def calculate_days_since():
    try:
        first_commit_date = os.getenv('FIRST_COMMIT_DATE')
        if not first_commit_date:
            raise ValueError("FIRST_COMMIT_DATE not set")
        
        days = (datetime.datetime.now() - datetime.datetime.strptime(first_commit_date, "%Y-%m-%d")).days
        return first_commit_date, days
    except Exception as e:
        print(f"⚠️ Error calculating days: {e}", file=sys.stderr)
        return None, None


def get_commit_stats(owner):
    try:
        # Используем значения из переменных окружения
        external_commits = int(os.getenv('EXTERNAL_COMMITS', 0))
        print(f"External commits from env: {external_commits}")
        
        return external_commits
    except Exception as e:
        print(f"Error getting commit stats: {e}", file=sys.stderr)
        return None


def generate_socialify_url(days_since, first_date, external_commits):
    description = f"💾 Old-school coder ({first_date})\n{days_since} days of commits, coffee & magic ☕💻\n+{external_commits} karma (helping external projects)"
    encoded_desc = quote(description)
    return (
        f"https://socialify.git.ci/MamonovEvgeniy/MamonovEvgeniy/image"
        f"?description=1&font=Rokkitt&pattern=Brick%20Wall&theme=Dark"
        f"&custom_description={encoded_desc}"
    )


def main():
    first_date, days_since = calculate_days_since()
    print(f"first_date: {first_date}")
    print(f"days_since: {days_since}")
    if not first_date:
        sys.exit("❌ Could not determine first commit date")
    
    owner = os.getenv('GITHUB_REPOSITORY_OWNER', 'MamonovEvgeniy')
    external_commits = get_commit_stats(owner)

    socialify_url = generate_socialify_url(days_since, first_date, external_commits or 0)
    print(f"Generated Socialify URL: {socialify_url}")

    # Читаем шаблон
    template_path = Path(".github/scripts/README-template.md")
    template_content = template_path.read_text(encoding="utf-8")

    # Генерируем новый контент
    new_content = template_content.replace(
        "<!-- SOCIALIFY_PLACEHOLDER -->",
        f"<!-- SOCIALIFY_START -->\n[![Socialify]({socialify_url})](https://github.com/MamonovEvgeniy/MamonovEvgeniy)\n<!-- SOCIALIFY_END -->"
    )

    # Читаем текущий README для сравнения
    readme_path = Path("README.md")
    current_content = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

    if new_content != current_content:
        readme_path.write_text(new_content, encoding="utf-8")
        print(f"✅ README updated with new Socialify URL!")
    else:
        print("⚠️ No changes needed in README.md")

    print(f"First date: {first_date} | Days: {days_since} | External commits: {external_commits}")


if __name__ == "__main__":
    main()
