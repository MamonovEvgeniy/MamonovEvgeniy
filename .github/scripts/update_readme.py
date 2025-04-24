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
<h1 align="center">Hey! <img src="https://media.tenor.com/C84C_fqg7Y0AAAAj/pedro-dancing-racoon.gif" width="50"/> Welcome to my page<img src="https://emojis.slackmojis.com/emojis/images/1531849430/4246/blob-sunglasses.gif?1531849430" width="50"/></h1>

<!-- SOCIALIFY_START -->
[![Socialify](https://socialify.git.ci/MamonovEvgeniy/MamonovEvgeniy/image?description=1&font=Rokkitt&pattern=Brick%20Wall&theme=Dark&custom_description=%F0%9F%92%BE%20Old-school%20coder%20%282016-02-24%29%0A3347%20days%20of%20commits%2C%20coffee%20%26%20magic%20%E2%98%95%F0%9F%92%BB%0A%2B5%20karma%20%28helping%20external%20projects%29)](https://github.com/MamonovEvgeniy/MamonovEvgeniy)
<!-- SOCIALIFY_END -->

<!-- MEDIA_START -->
<div align="center">
  <img src="https://raw.githubusercontent.com/MamonovEvgeniy/media-assets/main/video/intro.gif" width="1200">
</div>
<!-- MEDIA_END -->

<!-- Contact_START -->
<h3 align="center">Connect with me:</h3>
<p align="center">
<a href="https://t.me/Travoltik" target="blank"><img align="center" src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/telegram.svg" alt="" height="30" width="40" /></a>
<a href="https://discordapp.com/users/542012348354002955/" target="blank"><img align="center" src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/discord.svg" alt="" height="30" width="40" /></a>
<a href="https://www.linkedin.com/in/evgenii-mamonov-62a412308/" target="blank"><img align="center" src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/linkedin.svg" alt="" height="30" width="40" /></a>
<a href="https://www.instagram.com/1neuronchik/" target="blank"><img align="center" src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/instagram.svg" alt="" height="30" width="40" /></a>
</p>
<!-- Contact_END -->
"""

    Path("README.md").write_text(readme_content, encoding="utf-8")
    print(f"✅ README updated! First date: {first_date} | Days: {days_since}")


if __name__ == "__main__":
    main()
