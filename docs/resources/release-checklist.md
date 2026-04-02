> [README](../../README.md) > [Docs](../) > **Release Checklist**

# Release Checklist

> **TL;DR** -- Before you publish: name and license settled, you tested it yourself, someone else tested it, docs are complete, security and performance checklists passed, repo is clean. This list is sequential. Do not skip ahead.

This checklist is for the moment you go from "works on my machine" to "other people will use this." It covers what to check before publishing a project. Some items are technical (your AI can help). Some require your judgment (no AI can replace them).

Work through this list top to bottom. Later sections assume earlier ones are done.


## Identity and Legal

Changing a name or license after people depend on your project is painful. Name conflicts lead to legal disputes or confused users who install the wrong package. Settle this before anything else is public.

- [ ] Project name is available (check GitHub, PyPI/npm/crates.io, domain registrars, internet search)
- [ ] Project name does not conflict with existing trademarks
- [ ] License chosen and `LICENSE` file in repo root
- [ ] License referenced in `pyproject.toml` / `package.json` / `Cargo.toml`
- [ ] If accepting contributions: contribution terms documented (CLA, DCO, or license clause in CONTRIBUTING.md)
- [ ] Author / maintainer contact visible (email, GitHub profile, or issue tracker)


## You Test It Yourself

Automated tests check logic. They do not check whether a real person can install and use your project. A missing dependency, a wrong path, a confusing error message: you only find these by doing it yourself, on a clean machine, as if you have never seen the project before.

Before anyone else sees it, run through this yourself. Not your AI, not your tests. You.

- [ ] Fresh install from scratch (clone, install, run) on a clean environment
- [ ] Every documented command in README actually works
- [ ] Every example produces the expected output
- [ ] Error cases show helpful messages (not stack traces)
- [ ] Uninstall / cleanup leaves no artifacts behind


## Someone Else Tests It

You know how your project works, so you unconsciously skip steps and fill in gaps. Someone else does not. If they cannot get it running from your README alone, your users will not either. This is the single most valuable step on this list.

- [ ] At least one person outside the project has tried it
- [ ] They followed only the README (no verbal instructions from you)
- [ ] Their feedback is documented and addressed (or consciously deferred)
- [ ] Edge cases they found are either fixed or documented as known limitations


## Code Quality

First impressions matter. If someone opens your repo and sees failing tests, TODO comments, or leftover debug prints, they close the tab. Clean code signals that the project is maintained and trustworthy.

- [ ] All tests pass
- [ ] Linter and formatter run clean (no warnings, no ignores without reason)
- [ ] Type checker passes (if used)
- [ ] No TODO/FIXME left that blocks release (audit with `grep -r "TODO\|FIXME"`)
- [ ] No dead code, no commented-out blocks, no leftover debug prints
- [ ] Architecture boundaries enforced (no import violations)


## Security

A leaked API key in your git history is public forever. A missing input validation is an open door. Security bugs discovered after release damage trust in a way that feature bugs do not. Catch them now.

Run through the [security checklist](security.md#checklist). Key items for release:

- [ ] No secrets in code or git history (run a secret scanner)
- [ ] `.gitignore` covers credential files, `.env`, keys
- [ ] Dependencies up to date, no known CVEs (see [dependency evaluation](dependency-evaluation.md))
- [ ] All dependencies still maintained (last activity within 12 months)
- [ ] If web-facing: OWASP Top 10 reviewed
- [ ] Adversarial testing run at least once (see [security.md](security.md#adversarial-testing))


## Performance

Your project works with 10 rows in development. Your first user has 10,000. A missing timeout, a query without LIMIT, or an unbounded list can turn a working project into an unusable one under real conditions.

Run through the [performance checklist](performance.md#checklist). Key items for release:

- [ ] No obvious bottlenecks (measured, not guessed)
- [ ] External calls have timeouts
- [ ] Database queries have limits and indexes where needed
- [ ] No unbounded memory growth


## Documentation

Your README is the front door. If it does not explain what the project does and how to use it, people leave without trying. Internal notes, placeholder text, or outdated architecture docs make the project look abandoned.

- [ ] README explains what the project does, how to install, how to use
- [ ] README includes requirements (language version, OS, dependencies)
- [ ] AGENTS.md is up to date (matches actual project state)
- [ ] decisions.md reflects current architecture decisions
- [ ] Known limitations documented (what does NOT work, what is out of scope)
- [ ] CHANGELOG exists with at least the first release entry
- [ ] No internal notes, draft text, or placeholder content left in docs


## Repository Hygiene

People will browse your repo, not just use your tool. WIP commits, large binaries, or files with your local paths in them look unprofessional and can leak information you did not intend to share.

- [ ] Default branch is clean (no work-in-progress commits)
- [ ] Commit history is understandable (no "fix fix fix" chains)
- [ ] No large binary files committed (images, databases, models)
- [ ] `.gitignore` is complete (build artifacts, caches, IDE files)
- [ ] No files with sensitive paths or usernames in them
- [ ] CI pipeline runs (tests, linting, security scanning)


## Final Go / No-Go

This is the gut check. Everything above is technical. This is about whether you are ready to stand behind what you are publishing.

- [ ] You would be comfortable if a stranger reads every file in this repo
- [ ] Version number set (first release: `0.1.0` or `1.0.0`, decide which)
- [ ] Git tag created for the release version
- [ ] Release notes written (what is included, what is not yet)


---

See also: [Security Checklist](security.md#checklist), [Performance Checklist](performance.md#checklist), [Stage 3: Enforce](../enforce.md) for automated checks.
