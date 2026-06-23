# Menus, help systems and routing in the AI Personal Tutor Toolkit

*Status: working paper / decision record. Captures a long, branching discussion on how students should find and be helped by the right tool. The conclusions were reached incrementally; this paper keeps the reasoning, not just the verdicts, so the thinking can be resumed rather than repeated.*

---

## 1. The core problem

The toolkit has 32 tools across five libraries (Writing 10, Structure 4, Academic Thinking 10, Research Proposal 5, Study Workflow 3). Two linked difficulties:

- **Finding the right tool.** A 29-tool menu is too much. A student cannot reliably self-diagnose their fuzzy problem into a tool name.
- **Helping a stuck student.** Once in a tool, a student may be lost, short of time, want a model answer, or be overwhelmed. The tool should respond well — without doing the work for them and without locking them out.

A recurring tension framed the whole discussion:

> Routing is either **extra work for the student** (answer my questions before I help you) or it is **needed** (it replaces the harder work of finding the right tool among many). The design challenge is to get the second without the first.

A hard-won prior data point: **WT1 (the existing writing-tool router) was non-trivial to get right.** Routing is not cheap even in narrow confines. This tempered every "just add a router" instinct.

---

## 2. Two distinct trigger points (these are different features)

A help system can be triggered in two places, and conflating them is a mistake.

**A. At the menu (before any tool runs).**
The student has no output yet. "Help me" here means *"I don't know what I need"* — an orientation/routing request. This is the hard case (the WT1 problem, generalised across many tools).

**B. In the context of a tool output (mid-flow).**
The student *has* something concrete in front of them and is stuck on it. "Help me" here means *"help me with this"*, and "this" is already loaded. This is the **easy, high-value case**: context is already narrow, so routing is shallow ("don't understand / too much / I disagree / just need an example"). It needs *escalation*, not *routing*.

Design consequence: build the in-output helper as the universal, reliable feature; treat at-menu routing as the harder, more constrained problem.

---

## 3. The decisive constraint: a help system can only route to tools that are present

This reframed everything. What "help me" can do depends on **scope**:

| Scope | What "help me" can mean | Routing difficulty |
|---|---|---|
| **Single-tool prompt** | Only in-output escalation (re-explain, example, slow down, triage). Nothing to route to. | None — no routing exists |
| **Mini-library** | Narrow within-family routing (4–6 related tools) + honest "out of scope" signpost | Tractable (WT1-sized) |
| **Master prompt** | Fullest routing | Hardest |

A counter-intuitive result fell out of this:

> The **harder** the routing (master, many tools), the **less** automated routing should be attempted. The **narrower** the scope (single tool), the more "help me" collapses to simple escalation that needs no routing at all.

This inverts the naive intuition that the master library (having all the tools) is where rich routing belongs. The master is where routing is *hardest*. The **mini-library is the sweet spot** — few enough tools that routing is a short, reliable choice; enough tools that routing is worth doing.

This also dovetailed with an earlier, separate finding (from the gating/context-load work): the **mini-libraries are the unit at which behaviour is reliable**. The same five-way split keeps being the right structure for every problem — context load, instruction salience, and now routing. That recurrence is a sign the split is doing real architectural work.

---

## 4. The menu problem (29 is too many) and the "problem-first" resolution

The real fault in a 29-item menu is not the number — it is that it forces the student to **self-diagnose into the toolkit's taxonomy** before being helped. They must already know their need is called "Expert Meaning Review" to pick it. That is the wrong kind of work, imposed on the person least able to do it.

**Resolution — flip the default from menu-first to problem-first.** The entry point is an invitation, not a list:

> "Tell me what you're working on and what's bugging you — or say `list tools` if you'd rather choose yourself."

Two paths from one door:

- **Knows what they want** → `list tools` → full list. Zero imposed routing; respects the experienced user.
- **Doesn't know** → describes the problem in their own words → *that description* routes them. The model is far better at "structure feels off → ST2" than the student is at finding ST2 in a list.

This resolves the extra-work-vs-needed tension: routing is "extra work" when **imposed** (a sub-menu interrogation); it is "needed" when it **replaces** harder work (finding the right tool). The fix is to make routing **opt-in and natural-language** — one clarifying question maximum, and only if the description is genuinely ambiguous.

---

## 5. The "help me" mode triggered by the student (in-output)

A student-triggered help mode is stronger than a model-detected one, because it removes the model's two weakest jobs: **detecting** that the student is stuck, and **inferring why**. The student declares it and picks the reason. This is the `ask, don't guess` principle as a feature, and it only loads when invoked, so it does not compete for context every turn — likely the **most reliable** mechanism discussed.

### 5a. Expected student stuck-states (menu options)

Starting set (proposed):

- **I'm short on time** → triage mode (highest-impact fixes only; links to existing panicking-student advice)
- **I don't understand the feedback** → re-explain the tool's last output in plainer terms, with an example *(label precisely: "don't understand what you told me", not "don't understand the topic")*
- **I just need a model / example** → worked example on *parallel* material
- **Too much information** → collapse to the single most important thing *(note: this is the student manually triggering the tiering the tool tries to do itself)*

Additions identified, in rough priority:

- **I don't know where to start** → pick the single first action, nothing else. *The most common real stuck-state; none of the original four catch it. Arguably the highest-value option.*
- **I disagree with the feedback / this doesn't fit my essay** → routes to the existing "take the challenge seriously, re-read before responding" behaviour. *Without this, a student who thinks the tool is wrong has nowhere to go but to abandon it.*
- **I'm stuck on one specific bit** → narrow single-point focus, not a full re-run. *Prevents overwhelm from re-triggering a big tool for a small need.*
- **English isn't my first language / the wording is hard** → surfaces the existing EAL behaviour as a student opt-in (better than the model trying to detect it).
- **Not sure this is allowed / worried it's cheating** → routes to honest-use guidance + AI-use record + "check with your tutor". *Addresses student guilt/confusion about legitimate use, which the literature flags as real. Turns the AI-use record into something the anxious-but-honest student reaches for.*

Considered but held back:

- **Just check it's good enough (reassurance)** → risky: invites a verdict, which shades into grading (which the toolkit avoids). Include only if worded to route to "how to judge it yourself against criteria", never "it's fine".
- **I want to argue with you** → redundant with "I disagree"; fold together.

Menu-size guidance: **5–7 options.** Too many becomes its own "too much information" problem and is more instruction competing for context. Suggested tight set: *don't know where to start / short on time / don't understand the feedback / just need an example / too much detail / not sure this is allowed.* Each must route to a behaviour that **already exists or is cheap to add** — the menu is mostly a *router to existing behaviours*, which is what makes it cheap and reliable.

### 5b. Expected student goal-states (a different kind of request)

A second cluster surfaced that is *not* a stuck-state but a **goal**:

- "How do I improve it?"
- "I just want to improve my paper"
- "I want to improve my grade — what do you think?"
- "I don't have much time and I want a better essay"

Key realisation: these are **one underlying request — *make my essay better* — at different urgency and directness**, forming a spectrum from "teach me to improve it" to "improve it for me, fast". They should be **one menu option that then asks a clarifying question**, not four rows.

Two carry a specific trap:

- **"What do you think? / improve my grade"** invites a **verdict** the toolkit deliberately doesn't give. Route to *criteria and self-assessment* ("I can't predict your grade, but I can show you what the mark scheme rewards and where yours is strong/weak"), never to a judgement.
- **"Don't have much time, want a better essay"** is the closest to "do it for me". Route to **deadline triage** (existing panicking-student behaviour): the 2–3 highest-impact fixes, *named not written*. Time pressure changes *prioritisation*, not *what the tool will do*.

Proposed handling: a single **"I want to improve my essay"** option (possibly the most prominent), routing by one question — *"Do you want to know how to improve it yourself, see what's rewarded and where yours stands, or are you short on time and need the highest-impact fixes first?"* — which absorbs all four phrasings into three branches (how / what's-rewarded / fastest-fixes).

Crucial stance: **every one of these is legitimate.** "I want a better essay" is what the tool is *for*. The anxiety about answer-seeking must not curdle into treating "improve my essay" with suspicion. Routing exists to make the *student's own improvement* the route to the better essay — not to gatekeep the goal.

### 5c. One menu or two?

Stuck-states (obstacles) and goal-states differ logically. Options: merge into one "help me" menu (mixes obstacle + goal — slightly untidy) or keep two menus (tidy but makes the student first classify their own problem). **Lean: one menu**, because a student in trouble wants help, not a taxonomy. The untidiness is worth it for the student.

---

## 6. The rejected idea: the "poison pill" self-lock

A proposed deterrent: if a student keeps demanding answers, trigger a mode that **disables the toolkit**. Rejected for three reasons:

- **Unreliable.** A soft, multi-turn, self-overriding instruction — the hardest kind for the model to hold, first to fail under context load (same fragility as the gating gate).
- **Unenforceable.** A custom GPT or pasted library has **no durable cross-session state**. "Lock" can only mean "this chat"; a new conversation clears it. Real enforcement lives below the prompt layer, which the toolkit doesn't have.
- **Miscalibrated.** It punishes the wrong people. A stuck/panicking/blunt-but-sincere student looks identical to an extractor, so the lock catches the **vulnerable**; the determined offloader simply leaves for a plain chatbot. *The pill poisons the cooperative user and waves the defector through.*

---

## 7. The accepted replacement: escalate-and-route (never refuse, never lock)

The sound instinct in the poison pill — *respond* to repeated answer-seeking — was kept; the response was changed from **locking** to **escalating the help**. This works because it runs **with** the model's helpfulness rather than against it, so it fires reliably and cannot misfire into punishing a stuck student (the trigger outcome is *more* help, not less).

**Pattern:**

1. **First request** — normal tool behaviour.
2. **Second request** (wants it done) — do not refuse. Offer a **collaborative or parallel-example** version: do one instance *with* them, or show a worked example on *different* material. Serves the stuck student and the example-seeker at once; already permitted by the "small teaching example" rule.
3. **Still pressing** — do not lock. **Ask one routing question** distinguishing motives the model can't reliably infer: *"a worked example to see the moves, or short on time and need the fastest fixes to your own draft?"* Serve the matching mode.

The artefact they asked for is **approached every time**, but always in a form where the student's own judgement does the last step.

### Worked cases

- **WT4 (Find My Mistakes), keeps asking for the corrected text:** escalate to doing one correction *together* (state the rule → student applies it to one sentence → confirm), then offer the fast collaborative path through all of them. Ends with both a corrected essay *and* the skill. Never hand over a fully corrected copy.
- **ST2 (Whole-Work Structure), keeps asking for the fixed structure:** "give me the fixed version" has several honest motives — to see one worked, as a guide, as an example, or a deadline. **Branch by asking.** Worked reverse-outline on a *parallel* essay for the learner; ruthless 2–3-change **triage** on *their* draft for the deadline case. Never hand over a finished restructure of their own essay.

### Principles
- **Ask, don't guess.** Don't silently judge lazy vs stuck vs panicking. Route by one question → removes false-positive risk entirely (nobody mislabelled because nobody labelled).
- **Win by being the most useful thing in the room**, not by holding a line. A deadline-panicked student served well has no reason to defect.
- **Place the rule centrally** (always-present instruction layer), compactly — it is multi-turn behaviour the model holds weakly under load, so it must not be buried per-tool.
- **Let the AI-use record do the honest work** — as transparency, not threat. It records the pattern for the student's own reflection and any tutor. Deterrence by record is fair because it documents rather than judges.

### Caveats noted for testing
- This is multi-turn, state-tracking behaviour → expect *less* reliability than single-turn instructions; test in the **master**, not just a mini, where it is weakest.
- ST2's deadline-triage path sits close to the line — "name the moves, don't write the sections" is the boundary, and the most likely place this leaks into doing the work.
- "Repeated" is fuzzy — second? third? Set the dial **empirically**; pinning it too hard makes the tool count requests pedantically instead of reading the room.

---

## 8. Self-contained but self-aware libraries (the cross-library boundary)

Decision: **mini-libraries are self-contained but self-aware.** Each does its own job; when the need falls outside its scope it says so honestly and points elsewhere, rather than pretending or bodging.

This removes the hardest thing from the table — **no cross-library routing is needed.** A library need only know (a) what it has and (b) that other libraries exist. The signpost is a **static statement plus a pointer**, not a routing engine — robust precisely because it is "dumb":

> "I only have these tools. What you're describing sounds like an *argument* problem — you may want the Academic Thinking library, or another writing tutor tool."

**Calibration is the one risk** (not the boundary itself): too eager to signpost → pushes away students it could help; too reluctant → bodges out-of-scope problems. **Lean: try first, signpost second** — handle what you reasonably can, and when signposting, offer partial help *alongside* the pointer, not instead of it. The signpost must be a genuine "you'll do better elsewhere", never an easy "not my problem" exit (the same escape-hatch risk seen with `expand` and routing deferral).

Property worth designing for: this **degrades gracefully with scope.** Single tool → "I do one thing; for anything else, here's where to look." Mini → narrow within-family routing + signpost. Master → fullest routing. Each does the most it can reliably do and is honest about the rest. **The honesty *is* the robustness.**

---

## 9. Master-level routing: "which library?"

A routing the author insists on at master level: **which of the libraries do you want to use** — a 5-way choice, not a 29-way one. This is WT1-sized and tractable. It reframes the master library as **a router to the families, plus the families underneath** — a two-stage funnel:

- Stage 1: ~5 libraries → reliable.
- Stage 2: ~4–6 tools within the chosen family → the WT1 case.

Never a 1-in-29 decision; always 1-in-5 then 1-in-6.

Same problem-first escape hatch applies: "pick a library if you know which, or tell me what you're working on and I'll point you to the right one." The describe-it path does a **5-way** natural-language classification (reliable size), then hands into the family.

### Open architectural fork (not resolved)
Does selecting a library mean the master **loads** that library (back to the full ~5,450-line file in context → the gating-under-load problem returns) or **hands off** to the mini-library (student switches to a 53KB file where behaviour provably holds)? The gating findings point hard at **hand-off** — implying the thing students run is a **lightweight router**, and the big "master library" becomes a *distribution bundle* rather than a *runtime prompt*. This needs an explicit decision.

---

## 10. Where routing effort actually belongs (the asymmetry)

A late correction reshaped the whole plan: **the libraries do not have a symmetric routing need.**

- **Writing (10 tools)** — the **primary** routing case, and the **tractable** one. Targets are *crisp and distinct* (mistakes vs references vs style vs flow), which is what makes a WT1-style router gettable (if hard). WT1 wisely scopes itself to *small-unit* tools only ("a sentence, a few sentences, one paragraph") — bounded twice over: small set, small unit.
- **Academic Thinking (10 tools)** — the **secondary** case, and the **genuinely fuzzy** one. The tools *overlap by construction* (AT2 gaps, AT4 evidence, AT5 concepts, AT7 objections all surface adjacent things; ST3 overlaps too). Routing is hard here not because the router is weak but because the **territory overlaps**. → Lean *against* a confident router; toward **honest-overlap handling** ("here's what each emphasises; several overlap"), or "run one, let the consolidated summary show if you need another".
- **Structure (4), Research Proposal (5), Study Workflow (3)** — **thin**. A short visible menu *is* the routing; building routers here is effort where there's no problem. RP and SW are also *ordered/sequenced* (RP1→RP5; SW plan→action→record), so they need a sense of **sequence**, not branching routing.

Principle drawn out: **don't make the router more developed — make the scope narrower.** WT1 worked because it routed in narrow confines; "more developed" has historically meant "wider", which is where routing breaks. The mini-library split is therefore also the unit at which routing is tractable.

> The amount of routing machinery should match the difficulty and worth of the routing — and in most places that is "very little". The real world is **lumpy**: one library needs a hard-won router (Writing), one needs honest ambiguity-handling (AT), the rest need a list. Design for the lumpy truth, not a tidy symmetric model.

---

## 11. Consolidated design (current best position)

**In-output "help me"** — available everywhere (master, mini, single tool); needs **escalation, not routing**; scope-aware targets:
- single tool → only that tool's escalations
- mini → escalations + suggest a sibling tool + honest out-of-family signpost
- master → escalations + suggest any tool
- One tight menu (5–7) mixing stuck-states and the single "improve my essay" goal-option; every item routes to an existing behaviour.

**At-menu / master routing** — **problem-first** ("describe it, or `list tools`"); natural-language; one clarifying question max; routing done at **family granularity first** (5-way, reliable), then narrow tool routing inside the family.

**Cross-library** — self-contained but self-aware; static "I only have these; you may want X" signpost; try-first, signpost-second.

**Effort allocation** — a real router for **Writing**; honest-overlap handling for **AT**; plain menus (with sequence) for the thin three; a thin 5-way router at master level.

**Underlying mechanics** — student-triggered (removes detect + infer); central placement for multi-turn rules; AI-use record as honest transparency; escalate-and-route, never refuse or lock.

---

## 12. Open questions to resolve later

1. **Master = runtime or bundle?** Load-and-proceed (gating risk returns) vs hand-off to minis (thin router; minis stay small). Gating evidence favours hand-off.
2. **One help menu or two** (obstacles vs goals)? Leaning one.
3. **AT routing form** — honest-overlap description vs "run one then consolidate". Possibly both; needs the AT tools' real relationships mapped.
4. **"Repeated" threshold** for escalate-and-route — set empirically.
5. **Reassurance option** ("is it good enough?") — include only with a self-assessment-against-criteria framing, or omit?
6. **Reliability test** — all multi-turn help/routing behaviour must be tested in the **master/large-file** condition, where it is weakest, not only in minis.

---

## One-line summary

Help and routing should be **student-triggered, problem-first, scope-aware, and proportionate**: escalate (don't refuse or lock) when a student is stuck; route in natural language at family granularity (5-way) then within a family (WT1-sized); keep libraries self-contained but honestly self-aware; and spend routing effort only where tools are many and distinct (Writing), handling overlap honestly where they aren't (AT), and using plain menus everywhere else.
