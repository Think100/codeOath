> [README](../README.md) > **AI Workflow**

# Working with Your AI

> **TL;DR** -- Start every session with "read AGENTS.md and todo.md." End with state capture and learnings. When something breaks, paste the exact error. Use multi-role reviews for quality. Automate recurring prompts as single-purpose agents.

Practical tips for working with AI day to day, so you get better results with less effort. Not about project structure (that is what start/grow/enforce cover).

**Jump to what you need:**
- **Setup once:** [Environment](#set-up-your-environment-once)
- **Each session:** [Start and End](#start-and-end-every-session-right) · [Git Safety](#keep-a-git-safety-net) · [Prompt Patterns](#prompt-patterns-that-work) · [Reviews](#get-multiple-perspectives-fast)
- **Scaling up:** [Multi-Agent](#working-with-multiple-agents) · [Automation](#automate-recurring-work-with-agents) · [Context Window](#context-window-management)
- **Long-term:** [Past Projects](#learn-from-your-past-projects) · [Experiments](#build-experiments-to-make-decisions) · [Staying Current](#stay-current-with-your-tools)


## Set Up Your Environment Once

These are one-time settings that make every session better.

### Tone and Behavior

A few rules in your global config (CLAUDE.md, .cursorrules, etc.) change how every session works:

- **Question is not a task.** "When I ask a question, answer first. Do not act unless I ask you to." Otherwise your AI starts refactoring when you just asked if it would make sense.
- **Push back when I am wrong.** "Test my reasoning. When you spot a problem in my approach, say it clearly." AIs default to compliance. You want cooperation.
- **Explain why, not just what.** "Always explain WHY you suggest a change." This prevents blind acceptance and helps you learn.
- **Prefer simple over clever.** "Prefer simple, maintainable solutions over clever ones." Without this, AIs tend toward elegant but complex approaches.
- **Check before creating.** "Check for existing patterns in the codebase before introducing new ones." Without this, your AI creates a second logging helper when one already exists.

### Language Rules

If you work in a language other than English, your AI will mix languages unpredictably unless you define the rules:

```markdown
| What | Language | Why |
|---|---|---|
| Code (variables, functions) | English | Universal, libraries expect it |
| Code comments | English | Same language as the code |
| Commit messages | English | Git history searchable |
| AGENTS.md, CLAUDE.md | Your language | Your thinking tool, your language |
| docs/ (todo, decisions) | Your language | Internal docs, scope thinking |
| README.md | Depends | Open-source: English. Private: yours |
```

The important thing is having a rule, not which rule you pick. See [language-conventions.md](resources/language-conventions.md) for a ready-to-copy version.


## Start and End Every Session Right

Most people skip this and lose context every time.

### Starting

> "Read AGENTS.md and docs/todo.md. What was I working on? What is the most important open item?"

Ten seconds. Saves you from staring at the project trying to remember where you left off.

### Ending: Capture State

Before you close the conversation:

> "Update docs/todo.md with what we accomplished and what is still open. If we made any decisions, add them to docs/decisions.md. Summarize what the next session should start with."

This is your future self's briefing. Your AI has perfect recall of the current session. You do not. Let it capture what happened while the context is fresh.

### Ending: Capture Learnings

This is the step most people skip and the one that makes the biggest difference over time.

After every session, ask yourself one question: **"What did I learn today that I did not know before?"** This can be a technical insight, a workflow pattern, a mistake you made, or a tool feature you discovered.

> "What were the key learnings from this session? What surprised us? What would we do differently next time? What worked well that we should keep doing? Were there any aha moments where something suddenly made sense?"

Write it down. Where does not matter: a note in your phone, a dedicated journal, a note-taking app. If you want a structured habit, keep a learning log as a file in your project (e.g., `docs/learnings.md`). One entry per session, a few bullet points. Over weeks and months, these small learnings compound into real expertise.

Why this works: vibe coding moves fast. You solve problems, move on, forget. Without capturing learnings, you solve the same problems again next month. With a learning log, you build on what you already figured out.

Examples of learnings worth capturing:
- "Opus over-engineers small projects. Sonnet is better for tasks under 500 lines."
- "Pre-commit hooks are cheap and prevent 80% of formatting issues. Should have set them up on day one."
- "The restaurant analogy for ports-and-adapters clicked. Chef = domain, supplier = adapter."
- "Always show AGENTS.md before first commit. Caught three wrong NOT entries."

### Handing Off Between Sessions

If your tool supports persistent memory, save learnings there too. "We tried approach X and it did not work because Y" is obvious right now but invisible tomorrow.


## Keep a Git Safety Net

AI moves fast. Sometimes too fast. A rename that touches 40 files, a "cleanup" that rewrites your folder layout, a refactor that looked right until you tried to run it. You want a way to undo all of it, even if you do not know git.

The good news: you do not need to know git. You need to know what to ask for. Your AI handles the commands.

### Commit Often

Every time your project is in a working state (feature done, test passing, a sensible stopping point), save it:

> "Commit the current state with a short message summarizing what we just did."

Every commit is a point you can come back to later. The more often you commit, the smaller the chunks you can undo. Before anything that touches many files (renames, moves, architecture changes), commit first even if the piece you just finished is small. A ten-second commit is cheaper than rebuilding an hour of lost work.

### When AI Breaks Something

Three situations, three things to say:

**One file is broken, the rest is fine:**

> "The file `path/to/thing.py` is wrong now. Roll it back to the last saved version. Leave everything else alone."

**The last change broke it, everything before was fine:**

> "The last change is wrong. Undo it completely. Go back to the previous commit."

**Something broke and you are not sure when:**

> "Something broke and I am not sure when. Show me the last few saved states and help me figure out which one was the last working version. Then go back to it."

You do not type the commands yourself. The point is knowing these options exist, so you ask for them instead of panicking.

### Second Copy as a Last Resort

If you are about to let the AI do something that feels genuinely risky and saving alone does not feel like enough, make a full copy of your project folder:

> "Before we do anything, make a copy of this entire project folder next to it, called `backup-2026-04-11`. I want a second version I can walk over to if this goes wrong."

Now you have two versions on disk. One you experiment on, one you fall back to with no git knowledge at all. If things go wrong, copy the backup folder back and continue.


## Prompt Patterns That Work

These are habits, not one-time prompts. Use them regularly and they become second nature.

### "Show me before committing"

Never let the AI commit without review:

> "Show me the AGENTS.md before committing so I can review it."

The habit: AI proposes, you approve, then it commits.

### "Stop after each step"

For multi-step operations (migrations, refactoring):

> "Move one file at a time. Stop after each move and let me review before continuing."

If step 7 of 10 breaks something, you can revert step 7 without losing steps 1-6.

### "Do not fix, just report"

For reviews and audits:

> "Review this code for security issues. Report findings sorted by severity. Do not fix anything. Discuss fixes with me before applying."

AI fixes sometimes have side effects. You want to understand the fix before it is applied.

### "Something is broken"

When your project stops working, paste the exact error message. Do not describe it in your own words, do not say "it does not work." The details you would skip are often the ones that matter.

> "[paste the full error message here]. What does this mean and how do I fix it?"

That is enough for most problems. If it is not, add what you were doing when it happened:

> "I was trying to [what you did]. I expected [what should happen]. Instead, [what actually happened]. Here is the error: [paste error]. What is wrong?"

If your AI suggests a fix, ask it to explain what the fix does and why it solves the problem. A fix you do not understand is a fix you cannot verify.

### "What am I missing?"

The most underrated prompt. After finishing a feature:

> "Read my AGENTS.md and look at what we just built. What did we forget? What edge cases are not handled? What would break if the input is empty, too large, or in the wrong format?"


## Get Multiple Perspectives Fast

The prompt patterns above help you work. This section helps you check your work. Instead of asking one AI to review something, give the same task to agents with different roles and run them in parallel. Three viewpoints in under five minutes.

### Useful Roles

> "You are a user who just installed this for the first time. Try to follow the README and use the main features. Where do you get stuck? What is confusing? What error messages are unhelpful?"

> "You are a senior fullstack developer with 20 years of experience. Review this for correctness, completeness, and dangerous simplifications. Cite line numbers."

> "You are a red team security auditor. Find vulnerabilities. Sort by severity (Critical, High, Medium, Low)."

> "You are a computer science professor. Check if the concepts are explained correctly. Suggest analogies that make complex ideas accessible."

> "You are a vibe coder with 2 months of experience. Read this guide. Where do you get lost? Where would you stop reading?"

The key insight: **different roles find different problems.** A security auditor will never tell you that your explanation confuses beginners. A beginner will never find a timing attack. You need both.

### Review Cycles

The idea: do not just write and move on. Write, let your AI review it from different angles, fix what it found, review again. This sounds slow, but with AI it takes minutes, not hours.

1. Write the first version
2. Send to 2-3 agents in parallel (different roles from above)
3. Read the findings, focus on the serious ones first
4. Fix critical and high items
5. Review again if the fixes were significant

Why the second review? Because fixes can introduce new problems. A security fix might break a feature. A performance optimization might make the code harder to read. The second pass catches what the first fix introduced.

A full cycle takes under 15 minutes with AI. The quality difference between one pass and two is massive.


## Working with Multiple Agents

Once you are comfortable with reviews and prompt patterns, you might start using multiple agents. Modern AI tools can run multiple agents at the same time. Your main agent writes code while a second agent reviews it, a third runs tests, and a fourth checks security. Most of the time, your tool decides when to start these agents automatically. You do not need to manage them.

When it matters is when two agents touch the same files. If one agent is rewriting a function while another is reviewing the old version, the review is worthless. If two agents edit the same file at the same time, you get conflicts.

Three principles that stay true regardless of which tool you use:

**One writer per file.** If an agent is changing a file, no other agent should be changing that file at the same time. Reading is fine. Writing at the same time is not. Your tool usually handles this, but if you start agents manually, keep this in mind.

**Separate jobs, not shared ones.** A good split: one agent writes code, a different agent reviews it, a third runs tests. A bad split: two agents both adding features to the same module. When in doubt, let one agent finish before the next one starts.

**The AGENTS.md is the shared rulebook.** Every agent reads it. If your rules are in AGENTS.md, every agent follows them. If your rules are only in the conversation, only the current agent knows them. This is the main reason to keep your project rules in a file, not in your head.

> "I want to run a review while you keep working. Which files are you currently changing? I will make sure the review agent does not touch those."

You do not need to understand how agents work internally. You need to understand that they are independent: they do not see each other's work until it is saved. Think of it like two people working in the same office. They can work in parallel, but they should not both be editing the same document at the same time.


## Automate Recurring Work with Agents

Once you are comfortable with agents, the next step is turning repeated prompts into reusable ones. If you give the same instruction more than twice, make it a standing agent. Each agent has one job and minimal permissions.

**Test runner** -- cannot edit files, only runs tests and reports failures:
> "Execute pytest. Report only failures. Do not suggest fixes. Do not edit files."

**Security audit** -- read-only, scans for vulnerabilities:
> "Read the entire codebase. Check for: secrets in code, missing input validation, SQL injection, XSS, error messages leaking internals. Report sorted by severity. Do not fix anything."

**Architecture check** -- read-only, verifies that code is in the right place:
> "Read AGENTS.md and check if the code follows the architecture rules. Is any code in the wrong folder? Report violations."

**Documentation check** -- read-only, compares docs vs. reality:
> "Read AGENTS.md, docs/todo.md, and docs/decisions.md. Compare with actual project state. Flag outdated decisions, completed tasks still open, documented files that do not exist."

For session wrapup and learning capture agents, see the prompts in [Start and End Every Session Right](#start-and-end-every-session-right) above.


## Context Window Management

Your AI has a context window: everything loaded into the conversation (files, rules, past messages, tool outputs) competes for the same limited space. Modern tools compress older messages automatically when things get tight, but compression flattens details, and attention already degrades long before the hard limit. The more you pile in, the less sharp the AI is about any single piece. This is a 2026 concern; context windows keep growing, so the patterns below will matter less over time.

### Keep AGENTS.md Lean

AGENTS.md loads every session, so every line costs context for the whole conversation. Past ~100 lines the AI starts skipping parts of it. Move folder-specific rules into `frontend/AGENTS.md`, `db/AGENTS.md` etc. (many tools only load them when the AI works in that folder), and add navigation hints so the AI does not scan every file to find your layout:

> "The auth code is in `src/auth`. The database code is in `src/db`. The HTTP routes are in `src/routes`. Start there before reading anything else."

### Read Large Files in Pieces

For very long files (generated code, data dumps, huge test suites), ask for a slice, not the whole thing:

> "Read lines 200-400 of `big_file.py`, I want to understand `process_batch`."

Never let a 3000-line file eat a third of your context because you forgot to ask.

### Commit Before a Context Reset

When your tool warns that context is filling up, or you notice the AI forgetting things from earlier in the session, stop. Commit what you have, run your session-end ritual (update todo.md, capture learnings), and start fresh. A long degraded session is worse than a clean new one.


## Learn from Your Past Projects

Your past projects are full of patterns that worked and mistakes worth avoiding.

> "Analyze the project at [path]. Look at git history, folder structure, AGENTS.md, and docs. What patterns were used? What worked well? What caused problems? What can we learn for our current project?"

This is how codeOath's security and performance guides were written: by analyzing a real project and extracting what actually mattered in practice. If you already learned something the hard way, capture it so you do not pay for it twice.


## Build Experiments to Make Decisions

When you are unsure about the right approach, do not debate. Build it multiple ways and compare.

1. Define a small, concrete task (buildable in one session)
2. Run it with different conditions (with/without your rules, different models)
3. Compare results against a checklist of what matters (not gut feeling, actual criteria)
4. Feed findings back into your rules

### Example

We gave the same task (build a note-taking app) to Sonnet and Opus, with and without codeOath principles. Same prompt, one variable:

| Variant | Score | Key finding |
|---|---|---|
| Sonnet + codeOath | 12/12 | Right architecture dose, complete features, no silent failures |
| Sonnet reference | 10/12 | Feature-complete but monolithic |
| Opus reference | 7/12 | Good product decisions but no structure |
| Opus + codeOath | 6/12 | Over-engineered, forgot basic features |

The lesson: adding too much structure is as bad as adding none. Match the architecture to the size of the project.


## Stay Current with Your Tools

AI tools change fast. What did not work last month might work now.

- **Check release notes** of your AI tool once a month
- **Revisit your AGENTS.md rules** quarterly. See the [Maturity Dial](resources/philosophy.md#the-maturity-dial) concept.
- **Try new capabilities** on a branch, not on main

The rules you wrote six months ago may no longer be needed. Review and remove what no longer applies.


---

See also: [Stage 1: Start](start.md) for project setup, [Prompt Cheatsheet](resources/prompts.md) for all copy-paste prompts in one place.
