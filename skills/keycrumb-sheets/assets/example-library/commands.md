# Git essentials

A small reference for an existing Git working tree. Run commands yourself when appropriate.

## Inspect

| Action | Command |
| --- | --- |
| Show working tree status | `git status --short` |
| Show changes in tracked files | `git diff` |
| List recent commits | `git log -5 --oneline` |
| Show the current branch | `git branch --show-current` |
| List configured remotes | `git remote -v` |

## Undo changes

| Action | Command |
| --- | --- |
| Unstage a file, keeping its edits | `git restore --staged <file>` |
| Discard uncommitted edits to a file | `git restore <file>` |

Replace `<file>` with a path from `git status`. `git restore <file>` permanently
discards that file's uncommitted edits.

## Filter changes

Search status output for a word; replace `README` with your filename fragment:

```sh
git status --short | grep README
```

![Workflow](images/workflow.png)
