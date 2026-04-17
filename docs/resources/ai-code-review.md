> [README](../../README.md) > [Docs](../) > **AI Code Review**

# AI Code Review

> **TL;DR** -- AI writes code that works. But "works" is not enough. AI hides errors instead of showing them, adds complexity you do not need, and makes decisions without telling you. You do not need to read code to catch these problems. You need the right questions. This guide gives you those questions, and the prompts to let your AI answer them for you.

You told your AI to build a feature. It wrote code. It runs. No errors. You commit it, move on. Two weeks later, something breaks and nobody can figure out why.

What happened? The AI made decisions you never saw. It decided to silently ignore errors instead of stopping. It decided to return empty results instead of telling you the database was unreachable. It decided to add 150 lines of "safety" code that hides the real problems.

This is not a rare edge case. It is the default behavior of every AI model when writing code.

The good news: you do not need to become a programmer to catch these problems. You need to understand what can go wrong, and you need to know which prompts to use so your AI checks its own work.


## The One Rule: Errors Must Be Visible

Think of your code like a car dashboard. When the engine overheats, the temperature warning lights up. You pull over, you fix it, no damage done.

Now imagine a car where someone disconnected all the warning lights. The engine overheats, nothing on the dashboard changes. You keep driving. The engine dies on the highway.

AI code often disconnects the warning lights. Not on purpose, but because it optimizes for "no error messages" instead of "correct behavior." It catches errors and throws them away. Your program keeps running, but it is running wrong.

The rule is simple: **when something goes wrong, the program should stop and tell you.** Not continue silently. Not pretend everything is fine. Stop and say what happened. This is called "fail fast" and it is the single most important principle for reliable software.

You send a letter. The post office loses it. Instead of telling you, they mark it as "delivered." You think everything is fine. The recipient never gets the letter. That is what hidden errors do to your code. The program says "done" when it actually failed.

AI does this because it optimizes for "no crash." For the AI, a program that runs without error messages feels like success, even if it silently lost your data. You need to teach it otherwise.

> "Review the code you just wrote. Is there any place where an error is caught and ignored? Any place where the code continues as if nothing happened after something went wrong? I want errors to be visible, not hidden. Show me every place where a problem could happen silently."


## Five Problems AI Creates (and How to Catch Them)

You do not need to understand the code to spot these. You need to ask your AI the right question. Each problem below has an explanation in plain language, a real-world analogy, and a prompt you can copy.

### 1. Fake Safety

**What it means:** The AI adds dozens of checks for things that cannot actually happen. "What if this value is missing? What if it is the wrong type? What if it is empty?" These checks look responsible, but they do real harm: they make the code longer, harder to understand, and they hide actual problems behind a wall of unnecessary logic.

**Analogy:** Imagine a restaurant kitchen where the chef checks every tomato 12 times. Is it a tomato? Is it really a tomato? Is it not a cucumber pretending to be a tomato? Meanwhile, the steak is burning. The real problem gets lost in fake caution.

**Why AI does this:** AI has seen millions of bug reports caused by unexpected values. It overcompensates by checking everything, everywhere, even when the values come from code it just wrote itself.

**How to catch it:**

> "Look at the code you just wrote. Are there checks for impossible situations? For example: checking if a value is missing when you just created it one line above, or checking the type of something that already has a fixed type. Remove the checks that can never trigger. Explain which ones you removed and why they were unnecessary."

### 2. Guessing Instead of Failing

**What it means:** Something is missing or broken, and instead of stopping to tell you, the AI's code invents a replacement. The configuration file is missing? Use defaults. The database is unreachable? Return an empty list. The user is not found? Return a blank user.

**Analogy:** You ask your assistant to bring you the contract from the filing cabinet. The cabinet is locked. Instead of telling you, they hand you a blank piece of paper. You sign it thinking it is the contract.

**Why AI does this:** AI prioritizes "the program keeps running" over "the program is correct." A crash feels like failure to the AI. But running with wrong data is far worse than stopping.

**How to catch it:**

> "Check the code for fallback values. Are there places where the code returns a default (like an empty list, zero, or a blank value) when the real data is not available? For each case, tell me: is the fallback actually safe, or could it cause wrong results? If missing data means something is broken, the code should stop, not guess."

### 3. Code That Goes On Forever

**What it means:** The AI adds retry logic (try again if something fails) but forgets to set a limit. If the database is down, the code tries to connect every 5 seconds forever. Your program hangs. Nothing else can run.

**Analogy:** You call a phone number. Nobody picks up. So you call again. And again. And again. You never stop, never call a different number, never leave a message. You just keep dialing forever.

**Why AI does this:** Retry logic looks professional. The AI adds it because it learned that retrying is better than failing immediately. But retry without a limit is worse than both.

**How to catch it:**

> "Does the code retry anything (network calls, database connections, sending emails)? If yes: is there a maximum number of attempts? What happens after the maximum is reached? If there is no limit, add one. Three retries is a good default. After that, stop and report the error."

### 4. Everything in One Place

**What it means:** The AI puts all the logic into one giant block. Input validation, business rules, database calls, email sending, error handling, everything mixed together. When one part fails, it is impossible to tell what went wrong. When you want to change one thing, you risk breaking everything else.

**Analogy:** You have one room in your house. The kitchen, bedroom, bathroom, and office are all in the same room. When the sink leaks, your bed gets wet. When you cook, your paperwork smells like garlic.

**Why AI does this:** AI generates code in one pass, top to bottom. It does not naturally go back and split things apart. The result works, but it is fragile.

**How to catch it:**

> "Look at the code you just wrote. Is there any function or block that does more than one job? For example: a function that validates input AND saves to the database AND sends an email. Split these into separate pieces. Each piece should do one thing. If one piece fails (email sending), the other pieces (saving the order) should not be affected."

### 5. Not What You Asked For

**What it means:** You asked for a login page. The AI built a login page, a registration page, a password reset flow, an email verification system, and an admin dashboard. Or the opposite: you asked for a complete user management system and the AI built only the login page and skipped the rest.

AI does not stick to your request. It expands scope (adds things you did not ask for) or silently drops requirements (skips the hard parts). Both are dangerous. Extra features mean extra code to maintain and extra places for bugs. Missing features mean your project is not what you think it is.

**Analogy:** You hire a painter to paint your living room blue. You come home and the living room is blue, but they also repainted the kitchen green, moved your furniture, and installed a new light fixture. Or worse: they painted three walls and went home, and you did not notice the fourth wall until the weekend.

**Why AI does this:** AI models try to be helpful. "Helpful" often means "do more than asked." They also sometimes avoid hard requirements by building something similar but easier. They do not tell you about either decision.

**How to catch it:**

> "Compare what you just built against what I asked for. List every requirement I gave you, and for each one, tell me: is it fully implemented, partially implemented, or missing? Then list everything you added that I did not ask for. I want an honest comparison, not a summary of what you built."


## Your Review Workflow

You do not need to review code yourself. You need to ask your AI to review its own work. The trick is knowing which questions to ask, and when to ask them. Stopping after every AI response breaks the flow that makes vibe-coding fast. Review at natural checkpoints instead: before you commit, and before you release.

### Before You Commit

A commit is the natural moment to pause. Three prompts, about two minutes total. First the general sanity check, then scope, then secrets:

> "Before we continue: check what you just wrote. Are there hidden errors (failures that I would not notice)? Unnecessary checks (for things that cannot happen)? Fallback values that could give me wrong results? Be honest, not defensive."

The last sentence matters. Without it, the AI tends to defend its own code.

> "Compare what you built against what I originally asked for. Did you implement everything? Did you add anything I did not ask for? Did you skip anything? Be specific."

> "Is there any password, API key, token, or secret hardcoded in the code? Check every string that looks like a credential. If you find any, tell me, do not just fix them."

### Before You Release

For important milestones (first release, sharing with users, going live), run a full review:

> "Read AGENTS.md. Then review the entire codebase in six passes and report findings for each:
> 1. Hidden errors: where can something fail without me knowing?
> 2. Fake safety: where are there checks for impossible situations?
> 3. Wrong assumptions: where does the code guess instead of fail?
> 4. Scope: is everything I asked for implemented? Is there anything I did not ask for?
> 5. Secrets: any credentials in the code?
> 6. Structure: does the code follow the architecture rules in AGENTS.md?
> Do not fix anything. Report only. I will decide what to fix."

For the full release process (build, tests, publishing), see [release-checklist.md](release-checklist.md) and [build-pipeline.md](build-pipeline.md).


## Adding Review Rules to Your Project

Once you have a feel for which problems show up in your project, encode the rules in your AGENTS.md. That way, every AI session follows them automatically:

```markdown
## Rules
- Errors must be visible. Never catch an error and continue silently.
- No fallback values for missing data. If something is missing, stop and report.
- No checks for impossible situations. Validate input at the boundary, trust internal code.
- Every function does one job. If it does two, split it.
```

These rules prevent problems instead of catching them after the fact. Your AI reads AGENTS.md at the start of every session and follows the rules while writing code, not just during review.


## When You Get Comfortable

As you review more AI code, you will start noticing patterns without needing the prompts. You will see your AI add a fallback and think "wait, is that actually safe?" You will spot a 100-line function and think "this does too many things."

That intuition is the real goal. The prompts are training wheels. They teach you what to look for. Over time, you will ask the questions naturally, in the middle of the conversation, before the AI even finishes writing.

You do not need to become a programmer. You need to become a good reviewer. And good reviewers do not read every line. They know where to look.


---

See also: [AI Workflow](../ai-workflow.md) for session habits and multi-role reviews, [Security](security.md) for the full security guide, [Stage 1: Start](../start.md) for project setup basics.
