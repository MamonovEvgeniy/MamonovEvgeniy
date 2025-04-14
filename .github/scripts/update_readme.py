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
        total_commits = int(os.getenv('TOTAL_COMMITS', 0))
        current_year_commits = int(os.getenv('YEAR_COMMITS', 0))
        external_commits = int(os.getenv('EXTERNAL_COMMITS', 0))
        
        print(f"Total commits from env: {total_commits}")
        print(f"Current year commits from env: {current_year_commits}")
        print(f"External commits from env: {external_commits}")
        
        return total_commits, current_year_commits, external_commits
    except Exception as e:
        print(f"Error getting commit stats: {e}", file=sys.stderr)
        return None, None, None


def generate_socialify_url(days_since):
    description = f"⏳ На GitHub: {days_since} дней"
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
    total_commits, current_year_commits, external_commits = get_commit_stats(owner)

    socialify_url = generate_socialify_url(days_since)

    readme_content = f"""
<h1 align="center">Hey! <img src="" width="30"/> Welcome to my page<img src="https://emojis.slackmojis.com/emojis/images/1531849430/4246/blob-sunglasses.gif?1531849430" width="30"/></h1>

📅 Дата регистрации на GitHub: {first_date}  
⏳ На GitHub: {days_since} дней 

📊 Коммиты:  
- Всего: {total_commits or 'N/A'}  
- В этом году: {current_year_commits or 'N/A'}  
- Во внешних репозиториях: {external_commits or 'N/A'} 

<!-- SOCIALIFY_START -->
[![Socialify]({socialify_url})](https://github.com/MamonovEvgeniy/MamonovEvgeniy)
<!-- SOCIALIFY_END -->

<!-- activity_graph_START -->
[![activity graph](https://github-readme-activity-graph.vercel.app/graph?username=MamonovEvgeniy&theme=github-dark-dimmed&custom_title=MamonovEvgeniy%20Activity%20Graph&hide_border=true)](https://github.com/ashutosh00710/github-readme-activity-graph)
<!-- activity_graph_END -->
"""

    Path("README.md").write_text(readme_content, encoding="utf-8")
    print(f"✅ README updated! First date: {first_date} | Days: {days_since}")

if __name__ == "__main__":
    main()
