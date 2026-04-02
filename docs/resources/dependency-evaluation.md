> [README](../../README.md) > [Docs](../) > **Dependency Evaluation**

# Dependency Evaluation

> **TL;DR** -- Every library you add is a decision you will live with. Before you install anything, check three things: is it real, is it maintained, and is the license compatible. Your AI suggests libraries constantly. This guide teaches you when to say yes, when to say no, and how to use your AI to check.

A library is code that someone else already wrote and published for others to use. Instead of writing your own date calculator, you install a library that already handles dates, time zones, and edge cases. Your AI does this all the time: "Let me add this package for date handling." "I will install this library for HTTP requests." "This module makes database access easier."

Every suggestion sounds reasonable. Most of the time, it is. But every library you add becomes part of your project. If that library has a bug, your project has a bug. If that library stops being maintained, you have a problem. If that library has a license that conflicts with yours, you have a legal problem. And if the library does not actually exist and your AI hallucinated the name, you might install malware.

You do not need to understand how libraries work internally. You need to know which questions to ask before saying "yes, install it."


## When to Add a Library

Not every problem needs a library. The decision comes down to one question: **is this something my AI can write in a few minutes, or is it genuinely complex?**

**Add a library when:**
- The problem is well-known and has tricky edge cases you would miss (dates, time zones, encryption, image processing)
- You would need hundreds of lines of code to replicate what the library does
- The library is widely used and battle-tested (thousands of projects depend on it)
- You need to interact with an external service that provides an official library (e.g., Stripe for payments, AWS for cloud)

**Let your AI write it when:**
- You need a small helper (format a string, filter a list, parse a simple file)
- The library would add dozens of dependencies of its own for a feature you barely use
- Your AI can write the solution in under 30 lines and you can verify it works

**Analogy:** You need a hole in your wall. A drill is the right tool. But if you only need to hang one picture, maybe a nail and a hammer are enough. You do not need to buy a toolbox for every task.

Watch out for libraries that bring a crowd. Some libraries are small and focused. Others drag in dozens of their own dependencies (called "transitive dependencies"). You invite one friend to dinner. That friend brings five friends, and each of them brings three more. Suddenly you are cooking for 20 people and you do not know half of them. Each transitive dependency is code you did not choose, did not review, and do not control.

> "I need to [describe the problem]. Should I use a library for this, or can you write a small solution directly? If a library, which one and why? How many dependencies does it bring with it? If not, write the solution and explain it."

The key habit: **ask before your AI installs.** Add this to your AGENTS.md rules:

```markdown
- New dependencies: ask first, explain why it is needed (AI rule)
```


## Three Checks Before You Install

When your AI suggests a library, run through these checks. Your AI can do most of the work for you.

### 1. Is It Real?

AI models sometimes invent package names that do not exist. The name sounds plausible, the description makes sense, but the package was never published. Worse: attackers watch for commonly hallucinated names and register them with malicious code inside. You type `install some-helper-lib`, and you get malware.

> "Before installing [package name]: verify that this package actually exists on the official package registry for my language. Show me the official page, the number of downloads, and when it was last published. If you are not 100% certain it exists, say so."

### 2. Is It Maintained?

A library that was last updated three years ago is not necessarily dead. But it is a risk. If a security vulnerability is found tomorrow, nobody will fix it. If it breaks with a newer version of your language, nobody will update it.

Signs of a healthy library:
- Recent commits (within the last 6 months)
- Issues are responded to (not hundreds of unanswered issues)
- More than one maintainer (if the only maintainer disappears, the project dies)
- Regular releases

Signs of trouble:
- Last commit over a year ago
- Dozens of open issues with no responses
- Single maintainer, no activity
- Archived or marked as deprecated

> "Check the health of [package name]. When was the last release? When was the last commit? How many open issues are there, and are maintainers responding? How many maintainers are there? Would you call this actively maintained?"

### 3. Is the License Compatible?

Every library has a license. The license tells you what you are allowed to do with it. This matters more than most people think, especially if you ever plan to sell your software, use it commercially, or share it publicly.

Common licenses, simplified:

| License | What it means for you |
|---|---|
| MIT, BSD, Apache 2.0 | Use freely, even in commercial projects. Just keep the license notice. |
| LGPL | Use freely in most cases. If you modify the library itself, you must share those modifications. |
| GPL | If you use it, your entire project must also be GPL. Problematic for commercial or closed-source projects. |
| AGPL | Like GPL, but also applies if your software runs as a web service. The strictest common license. |
| No license | Legally, you have no permission to use it. No license does not mean "free to use." It means "all rights reserved." |
| Custom / proprietary | Read carefully. May restrict commercial use, redistribution, or modification. |

**The rule of thumb:** MIT, BSD, and Apache are safe for almost everything. GPL and AGPL require careful thought. No license means do not use it.

> "What license does [package name] use? Is it compatible with [your project's license, e.g., MIT, CC BY 4.0]? Are there any restrictions I need to know about? If the license is GPL or AGPL, explain what that means for my project."


## When to Remove a Library

Libraries accumulate. You added one for a feature, the feature changed, but the library stayed. Over time, your project carries dead weight: libraries that are imported but barely used, or not used at all.

Signs a library should go:
- You only use one small function from a large library
- Your AI can replace the library's functionality with a few lines of code
- The library is no longer maintained and has known vulnerabilities
- The library's license changed and is no longer compatible

> "Review my dependency list. For each library, tell me: what do we actually use from it? Could we replace it with a small amount of custom code? Are any libraries unused or barely used? Which ones would you recommend removing, and why?"


## Keeping Dependencies Healthy

The checks above help you decide before you install. But dependencies also need attention over time.

**Version pinning** means writing down the exact version of every library you use. Without it, the next person who sets up your project might get a different version that behaves differently or breaks things. Make sure your AI pins exact versions when it adds a library. If you are unsure whether your versions are pinned, ask:

> "Show me all dependencies in this project with their exact versions. Are any unpinned or using version ranges? If so, pin them."

**Ongoing maintenance** is not something you check every session. Whether your libraries are still maintained, up to date, and free of known vulnerabilities belongs in your maintenance routine (see [grow.md Routines](../grow.md#your-task-list-grows-up)) and your [release checklist](release-checklist.md).


---

See also: [Security](security.md) for hallucinated dependencies and supply chain risks, [AI Code Review](ai-code-review.md) for reviewing AI output, [Stage 1: Start](../start.md) for project setup basics.
