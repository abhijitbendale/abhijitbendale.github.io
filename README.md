# Site workflow

This site now has a lightweight workflow for generating project metadata and previewing locally.

## Local commands

- `./scripts/build.sh`
  - regenerates `assets/projects/projects-data.json` from the markdown manifest and metadata files

- `./scripts/serve.sh`
  - regenerates `projects-data.json`
  - starts a local server on http://localhost:8000

## How it works

- The browser loads `assets/projects/projects-data.json` directly for the Projects / Media page.
- `fetch(..., { cache: "no-store" })` is used so the browser always requests the latest files.
- If JSON generation fails, the page falls back to reading `assets/projects/projects-index.md` and the individual `.md` files.

## GitHub workflow

A GitHub Actions workflow runs on push, pull request, or manual dispatch and regenerates `assets/projects/projects-data.json`.
If the generated JSON changes, it is committed back to `main` automatically.
