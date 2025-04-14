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
    if not first_date:
        sys.exit("❌ Could not determine first commit date")
    
    owner = os.getenv('GITHUB_REPOSITORY_OWNER', 'MamonovEvgeniy')
    external_commits = get_commit_stats(owner)

    socialify_url = generate_socialify_url(days_since, first_date, external_commits or 0)

    readme_content = f"""
<h1 align="center">Hey! <img src="" width="30"/> Welcome to my page<img src="https://emojis.slackmojis.com/emojis/images/1531849430/4246/blob-sunglasses.gif?1531849430" width="30"/></h1>

<!-- SOCIALIFY_START -->
[![Socialify]({socialify_url})](https://github.com/MamonovEvgeniy/MamonovEvgeniy)
<!-- SOCIALIFY_END -->

"""

    Path("README.md").write_text(readme_content, encoding="utf-8")
    print(f"✅ README updated! First date: {first_date} | Days: {days_since}")


if __name__ == "__main__":
    main()
