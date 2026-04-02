> [README](../../README.md) > [Docs](../) > **Language Conventions**

# Language Conventions

> **TL;DR** -- One table in your AGENTS.md defines which language goes where: code in English, docs in your language, AI responds in whatever you write. Stops language mixing immediately. Works across all AI tools.

When you work with AI in a language other than English, every session becomes a language negotiation. Variable names in English, comments maybe in English, docs maybe in your native language, commit messages somewhere in between. Without a rule, your AI mixes everything, and consistency drifts within minutes.

The fix is simple: one table that maps each artifact type to a language. Add it to your AGENTS.md and the problem disappears.


## Why This Matters

Language mixing is not a cosmetic issue. It causes real problems:

**Searchability.** If half your commit messages are in English and half in German, you cannot search your git history reliably. "Fix" and "Beheben" describe the same thing but never appear in the same search.

**Cognitive load.** Reading code that switches between languages forces your brain to context-switch constantly. A function called `calculate_steuer_basis` (half English, half German) is harder to parse than either `calculate_tax_base` or `berechne_steuerbasis`.

**AI drift.** Without explicit rules, AI models pick up on whatever language you used in your last message and apply it inconsistently. You write one question in German, and suddenly your commit messages, code comments, and variable names are in German too.

**Onboarding.** When someone else (or your future self) reads the project, mixed languages create unnecessary confusion. Consistent language per context makes every artifact predictable.


## The Table

Add this to your `AGENTS.md` under a `## Language Conventions` heading. Here is an example for a German developer working on an open-source project:

```markdown
## Language Conventions

| What                          | Language | Why                              |
|-------------------------------|----------|----------------------------------|
| Code (variables, functions)   | English  | Libraries and APIs expect it     |
| Code comments                 | English  | Same language as the code        |
| Commit messages               | English  | Git history searchable           |
| AGENTS.md, CLAUDE.md          | German   | My thinking tool, my language    |
| docs/ (todo, decisions)       | German   | Internal docs, scope thinking    |
| README.md                     | English  | Open-source, international audience |
| AI responses                  | German   | My working language              |
```

Adapt the languages to your situation. A private solo project might use your language for README.md too. An English-speaking team needs no table at all.

The only hard rule: **pick one language per context and stick to it.** Your AI will follow whatever you put in the table.


## Choosing Your Languages

The table above is a starting point. Adapt it to your situation. Here are the decisions that actually matter:

### Code is always English

This is not negotiable for most projects. Libraries, frameworks, and APIs use English names. Your code interacts with them constantly. Mixed-language code (`user.hole_bestellungen()`) creates friction at every integration point.

Exception: domain terms that have no natural English translation. If your business domain uses specific terms (legal terms, local regulations, cultural concepts), keeping them in the original language can be clearer than a forced translation. Document these terms in your AGENTS.md so the AI uses them consistently.

### Docs: your language is your thinking tool

This is the decision most people get wrong. They write docs in English "because it is more professional." Then they spend twice as long writing, the docs stay shallow, and nobody updates them.

Internal documentation (todo.md, decisions.md, architecture decision records) is where you think through problems. You think better in your native language. Write your docs in the language you think in. The result is sharper reasoning, faster writing, and docs that actually get maintained.

Open-source documentation is different: if your audience is international, English is the practical choice. But for private projects, solo projects, or small teams that share a language: use your language.

### Commit messages: pick one, search matters

Commit messages are a search interface. When you run `git log --grep="auth"` six months from now, you need consistent language to find what you are looking for. English is the safe default because most tooling and conventions assume it. But a team that works entirely in French can use French, as long as everyone commits in French.

### AI responses: dynamic, not fixed

The AI should respond in whatever language you write in. This is the one context where the language is not fixed. If you switch from German to English mid-conversation, the AI should follow. Most AI tools do this naturally, but adding the explicit rule prevents edge cases.


## Edge Cases

These come up in practice and are worth deciding upfront:

| Context | Recommendation | Why |
|---|---|---|
| Error messages (user-facing) | Target audience language | Users read these |
| Error messages (logs) | English | Developers grep logs, English is searchable |
| UI strings | Target audience language | Users interact with these |
| API field names | English | Consumers expect it, matches code |
| Database column names | English | Matches code, frameworks generate from these |
| Branch names | English | Git tooling assumes ASCII-safe names |
| PR titles and descriptions | Team language | Reviewers read these |

You do not need to decide all of these on day one. Add rows to your table when the question comes up. The point is having a place where the answer lives.


## How AI Tools Handle This

This approach has been tested extensively across multiple projects and AI tools. The key findings:

**The table works immediately.** Once the table is in your AGENTS.md (or equivalent config file), AI models reliably respect the language boundaries. Mixed-language drift stops within the same session.

**Explicit beats implicit.** Without the table, AI models infer language from context, and they often infer wrong. A German question about English code can produce German variable names. The table removes the guesswork.

**Corrections stick per session.** If the AI slips (rare with the table, but it happens), one correction is usually enough for the rest of the session. Without the table, you correct the same thing repeatedly.

**Works across tools.** The table format works in AGENTS.md (Claude), .cursorrules (Cursor), COPILOT.md (GitHub Copilot), and similar config files. The concept is tool-independent.


For a concrete example with Python tooling, see [languages/python.md](../languages/python.md).


---

See also: [AI Workflow](../ai-workflow.md) for session setup, [Stage 2: Grow](../grow.md) for when to add conventions, [Stage 1: Start](../start.md) for the basics.
