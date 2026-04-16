> [README](../../README.md) > [Docs](../) > **Build Pipeline**

# Build Pipeline

> **TL;DR** -- Stage 1: `pre-commit` hook with linter and secret scanner. Stage 2: GitHub Actions that run tests on every push. Stage 3: fresh-install checks, dependency audit, cross-platform matrix. CD (publishing, deployment, signing) is optional and only matters if you ship apps or libraries to external users.

A build pipeline automates the checks and steps between writing code and shipping it. On a solo project you can do everything manually, but once your AI writes more code than you can review per commit, automation catches what you miss.


## What CI and CD Mean

**CI** = **Continuous Integration**. Every time you push code, an automated system checks it: runs tests, runs the linter, builds the project on a clean machine. You see green or red within minutes.

**CD** = **Continuous Delivery/Deployment**. After CI is green, an automated system takes the code and turns it into a shippable artefact (binary, installer, package), then publishes or deploys it.

For most vibe-coding projects only CI is relevant early on. CD matters when you release apps or libraries to external users.


## Pre-Commit Hooks: The Local Safety Net

A pre-commit hook is a script that runs automatically before `git commit` goes through. If the script fails, the commit is blocked. This is your first line of defence, and it runs before anything leaves your machine.

Install the `pre-commit` tool once, then create `.pre-commit-config.yaml` in your repo root:

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
  - repo: https://github.com/astral-sh/ruff-pre-commit  # Python example
    rev: v0.5.0
    hooks:
      - id: ruff
      - id: ruff-format
```

Run `pre-commit install` once per clone. From then on, every commit runs the hooks automatically.

**Why?** Secret scanning as a pre-commit hook is the most important single automation you can add. It catches a hardcoded AWS key or API token before it lands in Git, which is a lot cheaper than rotating the key after a leak.


## Why CI in Addition to Local Checks

Local tests and pre-commit hooks are your first line. CI covers gaps that neither can close structurally:

- **Bypass is easy.** Local `pytest` or `cargo test` depends on you remembering. Pre-commit can be skipped with `git commit --no-verify`. CI runs always, on every push, no bypass.
- **"Works on my machine."** Your local environment has your versions, your env variables, your installed tools. Pre-commit also runs on your machine, so it inherits the same blind spot. CI starts from zero - if your code depends on something you didn't declare, it fails there.
- **Fresh install.** You installed a package locally but forgot to add it to `package.json` / `Cargo.toml` / `pyproject.toml`. Locally it still works because it's already installed. CI catches it on first build.
- **Other platforms.** You develop on Windows. A user reports "doesn't run on Linux." CI can run Linux + macOS + Windows in parallel. Classic trap: path separators (`\` vs `/`).
- **External contributors.** Someone opens a pull request. Their pre-commit setup is not your problem - but CI runs for them automatically. Green check: safe to review. Red: don't merge.

Local checks (tests + pre-commit) = fast, your machine, your discipline. CI = external safety net, fresh ground, no bypass. Different jobs, not duplicate work.


## GitHub Actions: What It Does and What It Costs

**What happens technically:**

1. You push to GitHub.
2. GitHub starts a virtual machine ("runner").
3. The runner checks out your code, installs dependencies, runs your commands.
4. You see a green or red check on the commit on GitHub.

What gets run is defined in `.github/workflows/ci.yml`. Commands like `cargo test` or `pytest` - the same ones you'd type locally. GitHub doesn't do anything magical; it runs your script on a fresh machine.

**Cost:**

- **Public repo:** free, unlimited minutes, all platforms (Linux, Windows, macOS).
- **Private repo, Free plan:** 2000 minutes/month Linux free. A typical test run is 1-3 minutes.
- **Over the limit:** around 0.008 USD/minute Linux, 2x for Windows, 10x for macOS. Rarely exceeded in practice.

For open-source projects: 0 EUR, forever. GitHub subsidises it.


## What to Automate, Per Stage

### Stage 1: Pre-commit only

If you're solo and early, pre-commit with linter + secret scanner is enough. Your local tests stay local. No GitHub Actions setup needed yet.

### Stage 2: Add GitHub Actions

When you want external contributors, or you just keep forgetting to run tests, add a minimal workflow:

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.14"
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: pytest
```

Swap the language steps for Rust (`dtolnay/rust-toolchain`), Node (`actions/setup-node`), etc. The pattern is the same.

### Stage 3: Harden it

- **Fresh-install check.** Add a step that builds from scratch (`npm ci` instead of `npm install`, `cargo clean && cargo build`). Catches missing declared dependencies.
- **Secret scan as CI step too.** Second net after pre-commit (someone might bypass the local hook with `--no-verify`).
- **Dependency audit.** `pip-audit`, `cargo audit`, `npm audit`. Catches CVEs in your dependencies.
- **Cross-platform matrix.** Run the test job on Linux, Windows, macOS. Only needed if your code is meant to run on multiple platforms.

Each step is typically 5-10 YAML lines. Don't add everything at once, add as you hit the problems they solve.


## Secret Hygiene

### What Scanners Catch

Tools like `gitleaks` and `TruffleHog` recognise hundreds of secret patterns out of the box:

- AWS access keys, GitHub tokens, Stripe keys, JWTs, private SSH keys.
- `.env` files accidentally committed.
- Hardcoded passwords in code (`password = "admin123"`).

GitHub itself also scans public repos automatically and revokes the token at the provider's end if you, for instance, commit an AWS key. Lifesaver, but it only works after push.

### What Scanners Miss

- **Internal hostnames, staging URLs, infrastructure details.** These are not patterns, just strings. Scanners can't guess them. You need custom rules or discipline.
- **Business-logic leaks** (proprietary algorithms, internal conventions).
- **Binaries, screenshots with tokens visible, zipped archives.** Often skipped by scanners.

### If a Secret Got Pushed

**Watch out:** Deleting the commit isn't enough. Git keeps history. The only correct response: **rotate the secret at the provider immediately** (invalidate the AWS key, rotate the API token, change the password), regardless of whether you revert the commit. Assume anyone could have seen it.


## Preventing Internal Packages from Leaking

Three common scenarios, three different fixes:

### `node_modules/` should not be committed

Standard. Add to `.gitignore`:

```text
node_modules/
```

Same for Python's `.venv/`, Rust's `target/`.

### Internal package names should not appear in a public repo

Your `package.json` might reference `@mycompany/internal-tool` or `file:../debug-helper`. Even if the package itself isn't in the repo, the name is visible in `package.json` and `package-lock.json`.

Options:

- **Manual review** before each push: `git diff package.json package-lock.json`.
- **Custom gitleaks rules** that flag your company's naming patterns (`@mycompany/*`, internal Git URLs).
- **CI check** that scans the manifest against a blocklist. A small script that fails the build if a forbidden pattern appears.

### Your package should not accidentally get published to npmjs.com

Set in `package.json`:

```json
"private": true
```

`npm publish` will refuse to run. Relevant for apps and internal tools that aren't meant to be libraries.

### `.npmrc` / `.pypirc` contains auth tokens

Never commit these. Add to `.gitignore`:

```text
.npmrc
.pypirc
```

Commit a `.npmrc.example` with placeholder values so others know the format.


## Continuous Delivery (When You Need It)

The CD chain picks up where CI ends:

- **Build.** Source code becomes the shippable artefact (binary, installer, Docker image, npm package).
- **Sign.** Especially for desktop/mobile apps. Without a signature, macOS/Windows warn users ("unknown developer").
- **Version.** Set a Git tag, generate release notes from the CHANGELOG.
- **Publish.** Upload the artefact: GitHub Releases, crates.io, npm, PyPI, Docker Hub, app stores.
- **Deploy.** (Only for server apps.) Push the code to the production server.
- **Smoke test.** A quick ping after deploy to confirm the service is actually up.

For most vibe-coding projects only Build + GitHub Release + Publish are relevant. Everything else (server deployment, blue/green, canary releases) only applies when you run servers.

**Watch out for scope creep:** Kubernetes, Terraform, multi-stage environments (dev/staging/prod), service meshes - none of this belongs in a Stage 1-2 vibe-coding project. Add only when a concrete problem demands it.


## Code Signing (When You Need It)

Only relevant if you ship desktop or mobile apps. CLIs and libraries via package registries (npm, PyPI, crates.io) don't need separate signing.

### Paid (you pay)

- **Windows Code Signing:** annual fee from providers like Sectigo, DigiCert, GlobalSign.
- **Windows EV Code Signing:** higher annual fee. Removes SmartScreen warnings immediately. Requires a hardware USB key, which makes CI automation awkward.
- **Apple Developer Program:** annual fee. Mandatory for macOS signing, notarisation, Mac App Store, and iOS. No alternative provider.
- **Google Play:** one-time fee for a publisher account.

### Free for open-source

- **SignPath Foundation (Windows):** free code-signing certificate for open-source projects. Funded by sponsors (JetBrains, GitHub, and others). You apply; they sign your releases through CI. The realistic path for public Tauri/Electron apps on Windows.
- **Sigstore / cosign:** free signing system for containers and package artefacts (npm, PyPI). Not accepted by Windows/macOS as desktop installer signing.

### What does not work

- **Self-signed certificates:** users still get an "unknown publisher" warning. Practically useless except on a closed network.
- **Let's Encrypt:** TLS only (websites), not code signing. Common misunderstanding.
- **macOS signing without Apple Developer Program:** impossible. Apple is the sole gatekeeper.


## When Do You Need This?

| Stage | What to set up | Why |
|---|---|---|
| **1. Start** | Pre-commit hook with linter + secret scanner | Catches hardcoded secrets before they leave your machine. Almost free to set up, high value. |
| **2. Grow** | GitHub Actions: tests + linter on every push | Second net for forgotten local runs. Prerequisite for accepting contributions. |
| **3. Enforce** | Fresh-install check, dependency audit, secret scan, cross-platform matrix | Each solves a concrete class of failure. Add as problems surface, not preemptively. |
| **CD (any stage)** | Only if you publish artefacts or deploy servers | Optional. Most vibe-coding projects never need it. |

Start with pre-commit. Add GitHub Actions when you hit the first "I forgot to run tests" moment. Add the rest reactively, one problem at a time.


---

See also: [AI Code Review](ai-code-review.md) for the review prompts that complement the automated checks, [Security](security.md) for the general security guide, [Release Checklist](release-checklist.md) for pre-release manual steps, [Dependency Evaluation](dependency-evaluation.md) for deciding whether a dependency is worth adding in the first place.
