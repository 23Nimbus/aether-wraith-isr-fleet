Git hooks
=========

This directory contains client‑side Git hooks used by the Æther Wraith ISR Fleet project.  To enable these hooks for your local clone run:

```bash
git config core.hooksPath git_hooks
```

Two hooks are provided:

| Hook         | Purpose                                                    |
|--------------|------------------------------------------------------------|
| `pre-push`   | Runs a basic linter before allowing a push to proceed.    |
| `commit-msg` | Enforces a simple Conventional Commits style on messages. |

You can customise the scripts to fit your workflow.  Failed hooks will abort the push or commit.
