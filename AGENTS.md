# AGENTS.md

Codex agents working in this repository should follow these guidelines:

## Commit messages

- Use Conventional Commits where reasonable (`feat:`, `fix:`, `refactor:`, `docs:`, etc.)
- Keep them short and present tense
- Describe the change clearly

## Quality checks

- Run `ruff format` and `ruff check` on Python files before committing.
- Run the unit tests with `uv run pytest` or by activating the venv and running `pytest`.
- Prefer `uv run` for all command execution so the environment stays in sync with Metta/DAF lockfiles.
- Treat `daf/` as the meta-Metta control plane: business logic belongs under `daf/src/daf/**` and top-level scripts should remain thin wrappers.

## Real Metta Methods Only

- **DAF uses only real Metta methods** - no mocks, no simulations, no extra adjectives
- All DAF components are thin orchestration layers that delegate to actual Metta functionality
- Tests verify real integration with actual Metta classes and methods
- Documentation generation analyzes real Metta source code with complete signatures
- No "enhanced", "extended", or "wrapper" terminology - DAF simply orchestrates real Metta

## Type Annotations

- Always add type annotations to function parameters
- Add return type annotations to public API functions
- Follow selective annotation guidelines (see CLAUDE.md for details)
- Run mypy to check type consistency before committing

## Pull request notes

- Mention relevant file paths when describing changes.
- Include test output or note why tests were skipped.
