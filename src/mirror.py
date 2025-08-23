#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import subprocess
import shutil
from pathlib import Path
import requests

USERNAME = os.getenv("GITHUB_USERNAME", "").strip()
TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
INTERVAL_MIN = int(os.getenv("INTERVAL_MINUTES", "10"))
INCLUDE_FORKS = os.getenv("INCLUDE_FORKS", "false").lower() == "true"
EXCLUDE_ARCHIVED = os.getenv("EXCLUDE_ARCHIVED", "true").lower() == "true"

MIRROR_BASE = Path(f"/volume1/github-save/github-mirror/{USERNAME}")
API = "https://api.github.com/user/repos"

def gh_get_repos():
    repos = []
    page = 1
    while True:
        url = f"{API}?per_page=100&page={page}&sort=updated"
        r = requests.get(url, auth=(USERNAME, TOKEN), timeout=30)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        for repo in batch:
            if not INCLUDE_FORKS and repo.get("fork"):
                continue
            if EXCLUDE_ARCHIVED and repo.get("archived"):
                continue
            repos.append({
                "name": repo["name"],
                "full_name": repo["full_name"],
                "default_branch": repo.get("default_branch", "main")
            })
        page += 1
    return repos

def clone_url(full_name):
    return f"https://{USERNAME}:{TOKEN}@github.com/{full_name}.git"

def safe_print(*args):
    safe_args = []
    for a in args:
        if isinstance(a, str):
            safe_args.append(a.encode('utf-8', errors='replace').decode('utf-8'))
        else:
            safe_args.append(str(a))
    print(*safe_args)

def ensure_repo_checked_out(repo):
    name = repo["name"]
    local_path = MIRROR_BASE / name
    local_path.parent.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"

    try:
        if not local_path.exists():
            safe_print(f"[INFO] Cloning {repo['full_name']} ...")
            subprocess.run(
                ["git", "clone", "--no-tags", "--depth", "1", clone_url(repo["full_name"]), str(local_path)],
                check=True, env=env, timeout=300
            )
        else:
            safe_print(f"[INFO] Updating {repo['full_name']} ...")
            subprocess.run(["git", "-C", str(local_path), "fetch", "--all", "--prune"], check=True, env=env, timeout=300)
            subprocess.run(["git", "-C", str(local_path), "reset", "--hard", f"origin/{repo['default_branch']}"], check=True, env=env, timeout=300)
    except subprocess.TimeoutExpired:
        safe_print(f"[WARN] Git operation for {repo['full_name']} timed out.")
        return
    except subprocess.CalledProcessError as e:
        safe_print(f"[ERROR] Git operation failed for {repo['full_name']}: {e}")
        return

    safe_print(f"[INFO] Repo {repo['full_name']} is up to date at {local_path}")

def run_once():
    if not USERNAME or not TOKEN:
        raise RuntimeError("GITHUB_USERNAME / GITHUB_TOKEN missing")
    repos = gh_get_repos()
    for repo in repos:
        ensure_repo_checked_out(repo)

if __name__ == "__main__":
    while True:
        run_once()
        if INTERVAL_MIN <= 0:
            break
        time.sleep(INTERVAL_MIN * 60)
