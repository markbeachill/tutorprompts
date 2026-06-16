# Routing WT8 and WT9 into the Toolkit — Discussion & Handoff Note

*Status: discussion document for handoff. The integrating AI should read this in full before editing the launcher or router. It assumes Task A (below) is going ahead; it does not assume B or C. Nothing in the library has been edited yet — these are findings and options, not changes.*

---

## 0. Purpose of this note

Two new Writing Tutor tools — **WT8 (Flow and Coherence)** and **WT9 (Learn Subjects)** — are ready as tool files but are **not yet wired into the library's routing**. This note sets out what must change for students to reach them, what is currently wrong or missing, and which further changes are optional improvements rather than necessary fixes. It exists so that a second AI can complete the integration without re-deriving the analysis.

The original question that prompted this was "is the Writing Tutor family now too big (9 tools) for a student to navigate and for an LLM to follow the rules?" The short answer changed the framing, and that reframing matters, so it is recorded first.

---

## 1. Reframing the "too big" question

The worry was that nine WT tools is too many. Two facts reframe it:

1. **The library is already 29 tools across five families** (WT, ST, AT, RP, SW). WT is one family. Adding WT8 and WT9 moves WT from 7 to 9 and the whole library from 27 to 29 — a marginal increase on an already-large set, not a step change.

2. **The model never holds all tools at once.** The router uses `run_policy: selected_only`: when a tool is chosen, the model applies the global rules plus that one tool file, and explicitly does not blend other tools. So rule-following is unaffected by the total count — the model executes one tool whether the library holds 9 or 29.

**Conclusion on the model side:** there is no model-side rule-following problem from adding two tools. The architecture was built for this scale. WT8/WT9 follow the same `selected_only` pattern and do not change that.

**The real issue is student-side routing**, addressed below. The burden is not on the model holding too many rules; it is on the *student* having to know which of several similar tools they need.

---

## 2. What routing a student currently has to do themselves

There are three entry paths in the current router. Their burdens differ:

- **Number / code / title** (e.g. "8", "WT8", "Clarity Clinic"). Assumes the student already knows which tool they want. Fine for returning users; heavy for new users, because choosing correctly requires already understanding distinctions between tools they have not used.
- **Natural-language intent** (e.g. "my essay doesn't flow"). The router maps the description to a tool. This is the path most new students will use, and the launcher explicitly invites it: *"Not sure which tool? Describe your problem in a sentence and I will suggest one or two."* Its quality depends entirely on the intent-routing table behind it.
- **`prompt` / menu** to see the full list. Low burden but only useful once the student can self-identify their tool from titles.

**The front-door already exists in principle** — the "describe your problem" line — so the highest-value work is making the intent-routing behind it correct and complete, not building new machinery.

---

## 3. What is currently wrong or missing (necessary fixes)

These are not optional. Shipping WT8/WT9 without them leaves the tools mis-routed or unreachable-by-description.

### 3.1 The launcher menu does not list WT8 or WT9

They must be added under **Writing Tutor tools**. Suggested entries, in the menu's existing style:

> **WT8 — Flow and Coherence** — test why a paragraph feels jumpy by tracking the subject at the start of each sentence.
>
> **WT9 — Learn Subjects** — practise finding the subject and verb in your own sentences, so the other tools click.

### 3.2 The natural-language routing table mis-routes "flow"

The current table contains:

> structure, flow, paragraph order → paragraph-structure-review or whole-work-structure-review

This now sends "flow" to the **structure** tools, which is wrong: "flow" between sentences is exactly WT8's job. This line must be split so "flow / jumpy / hard to follow between sentences" routes to WT8, while "paragraph order / overall structure" stays with the ST tools.

### 3.3 The table has no entry for WT9

There is currently nothing routing "can't find the subject", "confused by grammar terms", or "grammar feels shaky" to WT9. This must be added.

### 3.4 Suggested corrected WT-relevant routing lines

For the integrating AI to adapt to the table's exact format:

> - paragraph feels jumpy / doesn't flow / hard to follow between sentences → `flow-and-coherence` (WT8)
> - paragraph order, overall structure, how sections fit together → `paragraph-structure-review` or `whole-work-structure-review`
> - can't find the subject or verb, confused by grammar terms, grammar feels shaky → `learn-subjects` (WT9)
> - paragraph doesn't make its point / ideas don't connect → `single-paragraph-analysis` (WT2)

The last line is included because "doesn't flow" (WT8) and "doesn't connect" (WT2) sound identical to a student but route differently — see §5.

---

## 4. The numbering decision (must be made before editing the menu)

The launcher is a **numbered list 1–29**, and the number routing table maps those numbers to tool codes. WT8/WT9 can be inserted two ways, and the choice has a real cost either way:

**Option 1 — Insert mid-list, after WT7.** WT8 and WT9 become menu numbers 8 and 9, and **every subsequent tool renumbers** (old 8→10, old 9→11, … old 29→31). This keeps the menu grouped logically (all WT tools together, numbered consecutively) but requires editing 21 downstream rows in the number-routing table and the menu, and breaks any external references to the old numbers.

**Option 2 — Append at the end.** WT8/WT9 become menu numbers 30 and 31. No existing number changes. But the menu's visual grouping breaks: the two newest WT tools sit at the bottom under the SW tools, away from WT1–WT7.

**Trade-off:** Option 1 is cleaner for the student (logical grouping) but costs a full renumber and invalidates old number references. Option 2 is safe and cheap but visually disjoints the WT family.

A possible third path: **keep menu display grouped but decouple display order from the routing number** — i.e. show WT8/WT9 under the WT heading, but assign them stable codes/IDs that the router keys on, so numbers matter less. This depends on whether the router can route reliably on `WT8`/`tool-id` without depending on the menu integer. The integrating AI should check whether number-routing is the primary key or whether code/ID routing is equally supported (the router table suggests all three are accepted: number, code, title/ID).

**Recommendation to the integrator:** confirm whether anything external depends on the current integers. If not, Option 1 (grouped) is best for students. If old numbers are referenced elsewhere, Option 2 or the decoupled third path avoids breakage. **This decision is not yet made — flag it to the human before choosing.**

---

## 5. The sentence/paragraph cluster — the one place students genuinely cannot self-route

Most of the 29 tools are distinct enough that the intent table alone suffices: nobody confuses "Harvard references" with "viva practice". But four tools form a genuinely confusable cluster, all touching "my writing isn't working at the sentence/paragraph level":

- **WT1 — Clarity Clinic:** one sentence won't come out clearly.
- **WT9 — Learn Subjects:** can't find the subject/verb at all.
- **WT8 — Flow and Coherence:** sentences are each fine but the paragraph jumps.
- **WT2 — Single Paragraph Analysis:** the paragraph doesn't make its point / ideas don't connect.

A student cannot reliably tell these apart from their own symptom, because "it doesn't flow", "it doesn't make sense", and "it's not clear" are used interchangeably by non-specialists. This is the cluster where routing-for-the-student adds the most value.

---

## 6. Options for routing-for-the-student (graded by ambition)

### Option A — Fix the table only (necessary, low effort)
Do §3 and §4. Rely on the existing rule: *"name at most two tools, say why each fits, ask the student to confirm."* For most requests this is enough. **This is the floor; it must happen regardless.**

### Option B — Add a disambiguating-question rule for the cluster (recommended improvement)
Add one short routing rule to the router: when a request could be WT1/WT2/WT8/WT9, the router asks a single discriminating question before routing. Draft:

> **Disambiguating the sentence/paragraph cluster.** If a student's description could be WT1, WT2, WT8 or WT9, do not guess. Ask one question:
> *"Is the trouble mostly — (a) one sentence that won't come out clearly, (b) finding the subject/verb at all, (c) a paragraph whose sentences are each fine but jump around, or (d) a paragraph that doesn't quite make its point?"*
> Route: (a) → WT1, (b) → WT9, (c) → WT8, (d) → WT2. Then confirm before starting.

This reuses the discriminating-question pattern already built into the tools (WT8's Stage C question routes between WT8 and WT2; WT9's on-ramp trigger routes into WT9). It fires only for the confusable cluster, and keeps the confirm-before-starting safety valve. It routes *toward* a choice without making the choice silently.

### Option C — A triage tool that reads the student's writing and recommends (not recommended)
A tool that ingests a sample and names which tool(s) to run. Powerful but risky: the model tends to over-reach (diagnosing problems it then tries to fix), and it duplicates judgement the individual tools already make. **Advise against** unless there is a specific reason to want automated triage.

---

## 7. Design principle that must be preserved

Whatever level is chosen, keep the toolkit's existing safety valve: **route toward a choice; do not make the choice silently.** The current rule — name at most two tools, say why, ask the student to confirm — should govern any new routing logic. The more the router decides for the student, the more it can decide wrong and send them confidently down the wrong path. The disambiguating question in Option B is safe precisely because it ends in the student choosing, not the router committing.

This mirrors the whole toolkit ethos and the WT8/WT9 design: the tool proposes, the student decides.

---

## 8. Interaction with the existing tool-to-tool handoffs

WT8 and WT9 already contain internal routing the integrator should be aware of, so the front-door and the in-tool handoffs are consistent rather than contradictory:

- **WT8 → WT2:** WT8's Stage C asks whether a flow break is an unwritten connection (stay in WT8) or a not-yet-worked-out idea (go to WT2). This is the WT8/WT2 loop from the design note.
- **WT8/WT1 → WT9:** if a student visibly cannot find a subject mid-tool, WT8 and WT1 should hand off to WT9, which teaches the skill and routes them back.
- **WT9 → originating tool:** WT9 sends the student back where they came from once the skill is solid.

The front-door routing (§6) should land students in the right place *first*; these in-tool handoffs catch cases where the initial routing was approximately right but the student needs an adjacent tool. Both layers use the same discriminating logic, so they reinforce rather than conflict.

---

## 9. Summary of what the integrating AI should do

**Must do (assumes Task A):**
1. Add WT8 and WT9 to the launcher menu (§3.1), after resolving the numbering decision (§4).
2. Fix the natural-language routing table: split the "flow" line and add the WT9 line (§3.2–3.4).
3. Add WT8/WT9 to the number-routing table with codes and tool IDs (`flow-and-coherence`, `learn-subjects`).
4. Confirm the public routing metadata in each tool file (already present as header comments) matches the table entries.

**Should consider (recommended):**
5. Add the disambiguating-question rule for the WT1/WT2/WT8/WT9 cluster (§6 Option B).

**Flag to the human before acting:**
6. The numbering decision (§4) — mid-list renumber vs append vs decouple. Do not choose unilaterally if external references to current numbers may exist.

**Advise against unless asked:**
7. The triage tool (§6 Option C).

**Do not change:** the `selected_only` activation model, the confirm-before-starting safety valve, or the in-tool handoffs in WT8/WT9 — these are correct as they stand.

---
---

# Part Two — A tutor-facing triage tool (separate proposal)

*Status: forward-looking design discussion, separable from the WT8/WT9 routing task above. This is NOT part of the required integration and should not block it. It revisits §6 Option C in more depth and refines the earlier "advise against" into a more precise position: the naive version is still inadvisable, but a carefully-scoped, humble version is worth building. Read this as a proposal for a future tool, not a handoff task.*

## T0. Relationship to Option C above

Section 6 Option C advised against "a triage tool that reads the student's writing and recommends," on the grounds that it over-reaches and duplicates the individual tools' judgement. That advice still holds **for the naive version** — a tool that confidently diagnoses and starts fixing. What follows refines the position: there is a *different* framing of the same idea that is both buildable and valuable, because it is honest about what an AI can and cannot do. The distinction is entirely in the framing, so it is worth setting out carefully.

## T1. The idea, stated clearly

A human tutor receiving a piece of student work does not start by fixing the first error they see. They read the whole thing as a diagnostician. They form an impression of what the writing is trying to do, then notice where it falls down — at every level at once: a muddled sentence here, a paragraph that never makes its point, a structural problem where the argument doubles back, a claim whose meaning does not survive scrutiny. Crucially, they then **triage**: they decide which problems matter most, which are symptoms of deeper ones, and what the student should work on first, second, third. They sequence the help. And they hold the whole thing in a working relationship — discussing meaning, explaining a grammar point, talking through why a paragraph is not landing.

The proposal is to give *that triage role* to an AI. Not a single tool fixing a single thing, but a **tutor-facing diagnostic pass**: the AI reads the work, identifies the issues across all levels, extracts the specific offending sentences and paragraphs, decides what to tackle in what order, and presents a **plan** — which the student (and their tutor) then works through, by feeding the prioritised items into the focused tools already built.

So the question is precise: **can an AI do the triage and sequencing that a tutor does — reading the whole, judging what matters most, and producing an ordered plan — rather than just executing the individual fixes once someone else has decided what they are?**

## T2. The answer: partly, and the split is the whole point

The answer divides along the line the toolkit has been drawing throughout — between *detection* and *judgement*. An AI is strong on one side and weak on the other, and the value and the danger of this tool live entirely in how it handles the weak side.

**What the AI can genuinely do — detection and extraction.** Reading a whole piece and surfacing candidate issues at every level is within reach. It can find the unclear sentences, flag paragraphs whose subject string scatters or whose point never forms, notice where structure doubles back, spot unsupported claims, and extract and locate the specific offending passages. This is the labour-intensive part of what a tutor does, and the AI does it fast and comprehensively. It produces the *raw findings*: here are the issues a careful reader noticed, quoted and located. The existing tools already half-do this one lens at a time; a triage pass runs them across the whole work at once.

**Where it gets shaky — prioritisation.** Deciding what matters *most* is a judgement, not a detection, and it depends on things the AI cannot see. A tutor prioritises against the *student* (a first-year who cannot yet form a paragraph point needs different sequencing from a finalist polishing prose); against the *assignment* (a brilliant argument that does not answer the brief has one problem that dwarfs fifty comma splices); and against *what is teachable now* (fixing the structure first makes half the sentence-level problems disappear, so polishing those sentences first wastes the student's effort). The AI can approximate this with rules — structure before sentences, meaning before mechanics, the readiness-gate logic from the design note — and those rules get it roughly right surprisingly often. But "roughly right" is doing heavy lifting, and the AI cannot tell when it is wrong, because being wrong here requires knowing the student and the brief, which it does not.

**Where it is weakest — the thing that looks easiest.** The most seductive failure is *meaning*. A tutor's most valuable triage judgement is often "this paragraph is clearly written but the underlying point is mistaken, or thin, or misunderstands the source." That requires genuine subject expertise — knowing the field well enough to tell a sound argument from a plausible-sounding wrong one. This is where AI is least reliable and most confident, the failure mode WA1's design already names: it will fluently flag "weak argument" where the argument is fine, and miss genuinely broken reasoning because it reads as fluent. So the one part of triage a tutor most prizes is the part the AI does worst, while sounding authoritative about it.

**The part it cannot do at all — the relationship.** A tutor's plan is not a document; it is the opening move in a conversation that adapts. They notice what the student grasps, and change the plan when the real problem turns out to be confidence, not commas. The AI can produce the *artefact* (the plan) but not the *adaptation* that makes a tutor's triage live. This matters because a plan presented as finished invites the student to treat it as authoritative and complete, when its actual status is "a fast first reading that needs a human to validate and adjust."

## T3. Can it be built? Yes — but only honestly framed

The tool is buildable and worth building, on one condition: it must be designed around what the AI is good at and be explicitly humble about what it is not. Concretely:

- **Present it as a first-pass triage for a tutor to validate, not a verdict for a student to obey.** The "tutor-facing" framing is load-bearing: the natural user is the tutor, or the student acting as their own first reader, and the output is a draft plan to be checked, not a syllabus to follow.

- **Be confident about detection and visibly tentative about prioritisation and meaning** — the standing-labels discipline from WA1. "Here are the issues I found" (high confidence) versus "here is the order I would suggest, and why — but this depends on your level and brief, which I cannot see" (flagged as judgement) versus "this argument reads as thin to me, but I am a generalist reader, not an expert in your field — check this one yourself" (flagged as least reliable). The tool's honesty about its own confidence is what makes it safe.

- **Route into the focused tools rather than do everything itself.** Its job ends at the plan: "work on these structural issues first (ST tools), then these paragraphs (WT2/WT8), then a clarity pass (WT1)." It triages and sequences; the existing tools execute. This prevents the over-reach failure where a triage tool starts fixing what it should only have flagged, and it fits the existing architecture.

- **Respect the readiness logic already worked out.** The sequencing rules are not guesses: the design note's loop (reasoning before polish, but flow-analysis as a probe that finds reasoning gaps) is exactly the principled ordering a triage tool needs. The prioritisation logic already built for the sentence/paragraph cluster generalises to the whole piece.

## T4. Verdict

An AI can do the **reading, finding, extracting, and a principled first-cut ordering** — the comprehensive, tireless part of triage — and can do it genuinely well. It cannot reliably do the **meaning-level judgement and student-aware prioritisation** that are a tutor's highest skill, and it cannot do the **adaptive relationship** at all. So the buildable tool is not "an AI tutor that decides what the student needs." It is a **fast, comprehensive first-reader that proposes a plan for a human to validate** — powerful precisely because it is honest about which of its lines are findings and which are guesses. Framed that way, it is one of the more valuable things the toolkit could add. Framed as a tutor-replacement, it is exactly the confident-but-wrong machine the rest of the design has been building guardrails against.

## T5. If this is taken forward

It would warrant its own design document (scope, the detection/judgement split, the standing-labels framing, the routing-into-existing-tools behaviour, and the failure modes to guard against), in the style of this note. It should be developed *after* WT8/WT9 integration, not bundled with it, because it depends on the focused tools existing and stable to route into. It also raises an integrity question the toolkit already takes seriously: a whole-piece triage plan sits closer to "doing the assessment of the work" than the single-issue tools do, so its tutor-facing framing and its "validate this, do not obey it" stance are not just safety niceties but part of keeping it within the academic-integrity boundary.
