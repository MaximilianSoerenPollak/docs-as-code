#!/usr/bin/env python3

import os
from pathlib import Path

def get_github_base_url(project_root: Path) -> str:
    repo = get_github_repo_info(Path(project_root))
    return f"https://github.com/{repo}"


def parse_git_output(str_line: str) -> str:
    if len(str_line.split()) < 2:
        logger.warning(
            f"Got wrong input line from 'get_github_repo_info'. Input: {str_line}. Expected example: 'origin git@github.com:user/repo.git'"
        )
        return ""
    url = str_line.split()[1]  # Get the URL part
    # Handle SSH format (git@github.com:user/repo.git)
    if url.startswith("git@"):
        path = url.split(":")[1]
    else:
        path = "/".join(url.split("/")[3:])  # Get part after github.com/
    return path.replace(".git", "")


def get_github_repo_info(git_root_cwd: Path) -> str:
    process = subprocess.run(
        ["git", "remote", "-v"], capture_output=True, text=True, cwd=git_root_cwd
    )
    repo = ""
    for line in process.stdout.split("\n"):
        if "origin" in line and "(fetch)" in line:
            repo = parse_git_output(line)
            break
    else:
        # If we do not find 'origin' we just take the first line
        logger.info(
            "Did not find origin remote name. Will now take first result from: 'git remote -v'"
        )
        repo = parse_git_output(process.stdout.split("\n")[0])
    assert repo != "",(
        "Remote repository is not defined. Make sure you have a remote set. Check this via 'git remote -v'"
    )
    return repo


if __name__ == "__main__":
    workspace_root = Path(os.getcwd())
    print("========PATH WE FOUND=========")
    repo = get_github_base_url(workspace_root)
    print("===========REPO FOUND=============")

