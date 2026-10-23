# Git essentials

A small reference for an existing Git working tree. Run commands yourself when appropriate.

## Inspect

| Action | Command |
| --- | --- |
| Working tree status | `git status --short` |
| Changes in tracked files | `git diff` |
| Recent commits | `git log -5 --oneline` |
| Current branch | `git branch --show-current` |
| Configured remotes | `git remote -v` |

## Filter changes

Search status output for a word; replace `README` with your filename fragment:

```sh
git status --short | rg README
```

![Workflow](images/workflow.png)
