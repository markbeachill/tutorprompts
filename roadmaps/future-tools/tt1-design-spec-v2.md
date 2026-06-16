# TT1 — Whole-Work Triage: Design Spec v2

*Status: focused design spec. V1 (`tt1-triage-design-note.md`) is retained as the fuller discussion document; this v2 is the tighter reference — the chosen framework and approach, broken down by tool library, with a literature review and reading list. Where v1 reasons through the options, v2 states the decisions.*

---

## 0. Questions to resolve (start here when returning)

Open decisions, parked deliberately so they can be settled by staged build evidence rather than in the abstract. The build-sequence document (`triage-build-sequence.md`) is designed to answer most of them by what proves out at each stage.

1. **Where does triage logic live?** A thin central front-door, or per-library triage with no central tool, or both? (Resolved by build Stage 1 vs Stage 5.)
2. **Should within-library triage point *out* to another library** (the recursive escape hatch)? Always, only for the WT/ST/AT cluster, or deferred? (Resolved by build Stage 3.)
3. **Span selection (Axis B) — how far to automate?** When a student submits a whole work but the need is a *local* tool, does TT1 select the paragraphs automatically, or point to them and let the student feed them in? (See §1.1 and the build-sequence Axis-B stages. Leaning: point-and-let-student-feed first; automate last.)
4. **Spec vs tool-file division of labour.** This spec governs framework and routing; the tool file (`whole-work-triage.md`) governs scoring and output mechanics. Confirm this split is wanted, and reconcile the tool file, which currently predates the scope rule and the HOC/LOC framing.
5. **Does TT1 survive as a tool at all,** or dissolve into per-library triage capability? (Follows from Q1; Stage 5 demotes any surviving TT1 to a thin router.)
6. **The thesis gap.** The most conspicuous out-of-scope HOC. Build a thesis tool (closes the gap and gives TT1 somewhere to route), or leave as a stated boundary? (Independent of TT1's validity; see gap-analysis document.)

---

## 1. Approach in brief

TT1 triages a piece of student work by mapping its problems onto an established **order-of-concerns** framework, then routing the student to the existing focused tools in **repair-priority order**. It scores honestly (counts, not quality), declines to test what it cannot act on, and proposes rather than fixes or grades. It is a first reading for a human to validate, not a mark.

The framework is not invented. It is the **global/local order-of-concerns** tradition in composition studies, of which the writing-centre **HOC/LOC** scheme is the best-known tutoring articulation. The rest of this spec sets out that framework, breaks it down across the toolkit's five libraries, and gives the scholarship behind it.

### 1.1 Routing has two axes

Triage makes two distinct routing decisions, not one:

- **Axis A — which tool.** What *kind* of help: clarity, flow, structure, argument. This is what HOC/LOC, per-library triage, and the disambiguating question address.
- **Axis B — which span.** What *part* of the work goes to that tool. A clarity tool wants a sentence or paragraph; a structure tool wants the whole piece. If the student submits a whole work, something must select the span to feed a local tool.

Axis B's difficulty is *inversely* related to the concern level, which tells you where the work is:

- **Global tools (ST2, ST4, AT1) need no span selection** — the span is the whole work by nature; you cannot reverse-outline one paragraph.
- **Local tools (WT1, WT8, WT9) need it most** — a whole essay has many paragraphs and a flow tool can only sensibly run on the two or three that most need it.

**Submission size is itself a routing signal.** If the student submits a single paragraph, Axis B is pre-answered (the span is what they gave) and the whole-work tools are implicitly out of play — the submission size signals local help. If they submit the whole work, both axes are live and span-selection becomes the expensive part. So *what* the student submits half-answers *what kind* of help they want, without TT1 having to ask.

The recursive caveat from §2.2 still applies: a paragraph submission may reveal a global problem ("this paragraph issue is really about your overall argument — that needs the whole piece"), so the upward/cross-library pointer operates on Axis B too.

The practical consequence, staged in the build-sequence document: the cheap cases (paragraph → local tool; whole work → global tool) need *no* Axis-B logic and work first; only the whole-work → local-tool case needs span selection, and even that has a cheap fallback — TT1 points to the spans in its findings and lets the student feed them in, rather than extracting and feeding automatically.

## 2. The framework chosen

### 2.1 Global / local, and its HOC/LOC articulation

The backbone is the distinction between **global** concerns (the whole-piece, meaning-bearing elements — thesis, purpose, audience, argument, organization) and **local** concerns (sentence- and word-level surface — clarity, grammar, punctuation). The cleanest definition is by *ripple effect*: a change is global when fixing it forces changes elsewhere in the draft, local when it affects only the sentence in hand. Many institutions teach a three-band version — **global / middle / local** — and the writing-centre tradition relabels these as **Higher, Middle, and Lower Order Concerns (HOC/MOC/LOC)**.

### 2.2 The two orderings (the load-bearing distinction)

The framework's rule is "global before local" — but this governs **repair order**, not **discovery order**:

- **Repair order (top-down):** fix global before local, so effort is not wasted polishing text that a structural change will delete or rewrite.
- **Discovery order (recursive, often bottom-up):** lower-order work is frequently how a higher-order problem is *found* — a clarity tangle reveals an unformed idea; a reverse outline reveals a structural gap.

TT1 discovers with whatever probe is reliable (usually lower-order) and advises repair top-down. These are not in tension; they answer different questions. This is the single most important thing to get right, and the thing a naive reading of "global before local" gets wrong.

### 2.3 Scope rule

TT1 only tests, scores, and reports concerns it can **act on** — where it has a tool to route to or concrete advice to give. Concerns the toolkit cannot yet serve are not tested or diagnosed; TT1 states they are out of scope and, at most, gives a one-line pointer when a lower-order probe surfaces one. This keeps TT1 reliable (it avoids the meaning-level judgements it is worst at), safe (it stays clear of marking), and useful (it produces an actionable plan, not an overwhelming catalogue).

## 3. The framework broken down by library

The toolkit's five libraries already map cleanly onto the order-of-concerns bands. This mapping is what TT1 routes against. Tools are given by code and ID.

### 3.1 Higher Order Concerns — global, meaning-bearing

**Argument & reasoning (AT family) — the core HOC band.**
The Argument Tools cover the highest-order rhetorical concerns: `assignment-brief-checker` (AT1, does it answer the task), `argument-map` (AT2, claim/support/assumptions/gaps), `descriptive-analytical-check` (AT3), `evidence-gap-checker` (AT4), `concept-clarity-checker` (AT5), `literature-use-checker` (AT6), `counterargument-limitations-checker` (AT7), `source-reliability-checker` (AT8), `critical-opponent-review` (AT9), `socratic-tutor` (AT10). This is the toolkit's strongest band and covers most HOCs well.

**Whole-work structure & meaning (ST family) — global structure.**
`whole-work-structure-review` (ST2, organisation/sequence/flow/balance), `reverse-outline-mapper` (ST4, what each part does), `expert-meaning-review` (ST3, do the ideas make sense), and `paragraph-structure-review` (ST1, each paragraph across the whole draft). ST4 is also TT1's best *diagnostic probe* for global problems — a near-mechanical extraction that surfaces structural gaps.

**Known HOC gaps (out of scope — state, do not test):** there is no dedicated **thesis / central-claim** tool, no **audience/purpose** tool, no **synthesis** tool, and no **introduction/conclusion-as-framing** tool. ST3 (expert meaning) and the AT family partly cover the argument side, but the thesis gap in particular is conspicuous. Per the scope rule, TT1 does not test these; it states them as out of scope and points upward when a probe surfaces one. (See the gap analysis document for detail.)

### 3.2 Middle Order Concerns — paragraph-level development

**Paragraph logic (WT/ST overlap).**
`single-paragraph-analysis` (WT2, chain of ideas, missing links, topic-sentence alignment) and `paragraph-structure-review` (ST1, paragraphs across the draft) sit at the middle band — development and connection of ideas within and between paragraphs. This is where the chain-of-ideas method and the readiness loop live: a paragraph problem is often where a global problem first becomes visible.

### 3.3 Lower Order Concerns — local, surface

**Flow and clarity (WT family).**
`flow-and-coherence` (WT8, running-subject/hand-off flow — newest), `clarity-clinic` (WT1, one sentence or paragraph), `style-clarity-review` (WT5, readability/tone/style), and the parsing prerequisite `learn-subjects` (WT9, find subject/verb on your own sentences). These are the most reliable areas for an AI and the most clearly actionable.

**Mechanics, sources, and surface (WT family).**
`find-mistakes` (WT3, grammar/logic/clarity/spelling/punctuation/referencing — the one tool licensed to itemise in full), `teach-mistake` (WT4, micro-lesson on a WT3 mistake), `referencing-helper` (WT6, Harvard references), `paraphrase-quotation-workshop` (WT7, paraphrase/quotation/attribution). Citations and formatting are LOCs in the framework and map here.

### 3.4 Not a concern band — process & integrity (SW family)
`revision-plan` (SW1), `feedback-to-action-plan` (SW2), `ai-use-record` (SW3) are process tools, not points on the concern hierarchy. TT1 may route to SW1/SW2 as the *destination for its own output* — the triage plan is itself a revision plan — but they are not areas TT1 diagnoses.

### 3.5 The repair-priority order TT1 uses

Drawn from the mapping above, TT1 sequences its plan top-down:

> meaning/argument (AT, ST3) -> whole-work structure (ST2, ST4) -> paragraph logic (WT2, ST1) -> flow (WT8) -> sentence clarity (WT1, WT5; WT9 if needed) -> mechanics & sources (WT3, WT4, WT6, WT7)

Discovery may run in any direction; the *plan* is ordered as above. Out-of-scope HOC gaps (thesis, audience, synthesis, intro/conclusion) appear in the plan as boundary statements or upward pointers, not as tool steps.

## 4. Scoring and output (summary)

- **Score counts, not quality:** auditable density figures ("clarity: ~12 sentences, about a third"). Never a quality number.
- **Band severity, never number it:** high/medium/low, marked as judgement, paired with evidence. Never a single overall score.
- **Sequence by repair priority** (§3.5), not by score and not by discovery order.
- **Propose, do not launch; map only to real tools.**
- **Output:** read + scope statement; findings by in-scope area with counts, bands, and evidence; a short capped plan naming tools; a status line (first reading, not a mark).

(Full output spec is in the tool file `whole-work-triage.md`; this spec governs framework and routing.)

## 5. Literature review

TT1's method rests on two established strands of composition scholarship: the **order-of-concerns** tradition that gives it categories and priority, and the **recursive-process** tradition that corrects how that priority is applied.

### 5.1 Order of concerns: global/local and HOC/LOC

The idea that revision should attend to global, meaning-level matters before local, surface ones is long-standing in composition studies, and is taught under several near-synonymous vocabularies. The **global/local** distinction is the most widely shared: the *Allyn & Bacon Guide to Writing* defines a local revision as one affecting only the sentence in hand, and a global revision as one where a change in one part drives changes in others — a definition by ripple effect rather than by category, which is the sharpest available criterion for "higher-order." Teaching and assessment guides commonly extend this to three bands (global / mid-level / small-scale), placing the most weight on the global level because that is what most determines a paper's success.

The **HOC/LOC** scheme is the writing-centre articulation of the same distinction, formalised by **Reigstad and McAndrew** (*Training Tutors for Writing Conferences*, 1984) and developed in their *Tutoring Writing: A Practical Guide for Conferences* (2001), where HOCs are defined as rhetorical concerns (audience, purpose, focus, organization, development) and LOCs as rule-based concerns (grammar, punctuation, citation). **Purdue OWL**'s widely-used summary states the priority rule directly: address HOCs first, then LOCs. **Duke University**'s Writing Studio adds the **Middle Order Concerns** tier. The framework's value is practical: it gives a tutor under time pressure a defensible answer to "what do we work on first?", and it doubles as a defence against the misconception that tutoring is mere proofreading.

A related but distinct strand is **assessment scoring**: the choice between **holistic** scoring (one overall impression) and **analytic / trait-based** scoring (separate judgements per dimension — e.g. the widely-taught 6+1 Traits, or ESL frameworks evaluating dozens of textual features). The assessment literature notes that the *purpose* of the task — diagnosis, development, or promotion — should determine the scale. This bears directly on TT1: as a *diagnostic/developmental* tool it belongs with analytic, per-area feedback, and explicitly *not* with holistic single-score grading. This is independent support for TT1's "no overall score" rule.

### 5.2 The recursive model of revision

The priority rule is easily misread as a claim that writing proceeds top-down in one pass. The corrective is the **recursive model of the writing process**, whose canonical statement is **Nancy Sommers**, "Revision Strategies of Student Writers and Experienced Adult Writers" (*College Composition and Communication*, 1980). Studying twenty first-year students and twenty experienced writers, Sommers showed that the dominant *linear* models of the day were modelled on speech and effectively wrote revision out of the process; experienced writers, by contrast, revise **recursively**, treating revision as finding the form and meaning of the argument rather than correcting the surface. Her finding most relevant to TT1 is that **students lack strategies for global revision**: they manage local, surface changes but are often unable to see the larger picture of purpose and readers, tending to treat revision as word-substitution because they assume the meaning is already present. **Flower and Hayes**' "A Cognitive Process Theory of Writing" (1981) gives the complementary cognitive account of writing as recursive rather than staged.

Two consequences for TT1 follow. First, the recursive model licenses TT1's *diagnostic* use of lower-order probes: surfacing a higher-order problem through lower-order work is how skilled revision actually proceeds. Second, Sommers' finding that students are competent locally but weak globally is exactly why a tool that runs reliable local probes and then *points upward* — rather than attempting the global judgement itself — is well-aimed: it meets students where they are able and reveals what they cannot see unaided, while handing the global repair to a tutor.

### 5.3 How the strands combine

The order-of-concerns tradition supplies TT1's **categories and repair priority**; the recursive tradition supplies its **discovery process**; the assessment-scoring literature supplies the **diagnostic-not-holistic** stance. Over all three sits an AI-specific constraint established earlier in this project: detection is reliable, judgement (especially of meaning) is not, so TT1 is scoped to detection-and-routing within the bands the toolkit can act on, and declines the global judgements it would perform unreliably.

## 6. Reading list

**Order of concerns (categories and priority)**
- Reigstad, T. J., & McAndrew, D. A. (1984). *Training Tutors for Writing Conferences*. Urbana, IL: ERIC/NCTE. — Origin of HOC/LOC.
- McAndrew, D. A., & Reigstad, T. J. (2001). *Tutoring Writing: A Practical Guide for Conferences*. Portsmouth, NH: Boynton/Cook-Heinemann. ISBN 978-0-86709-518-0. — Standard citation; HOCs rhetorical, LOCs rule-based.
- Purdue OWL. "Higher Order Concerns (HOCs) and Lower Order Concerns (LOCs)." — Canonical quick reference for the priority rule.
- Duke University Writing Studio. "Revision Strategies: HOCs and LOCs." — Adds the Middle Order Concerns tier.
- Ramage, Bean, & Johnson. *The Allyn & Bacon Guide to Writing.* — Global vs local revision, defined by ripple effect.

**Recursive model of revision (discovery process)**
- Sommers, N. (1980). "Revision Strategies of Student Writers and Experienced Adult Writers." *College Composition and Communication*, 31(4), 378-388. — Revision is recursive; students lack global-revision strategies.
- Flower, L., & Hayes, J. R. (1981). "A Cognitive Process Theory of Writing." *College Composition and Communication*, 32(4), 365-387. — Cognitive account of recursive composing.

**Assessment scoring (diagnostic vs holistic)**
- Background reading on analytic vs holistic scoring and trait-based assessment (e.g. the 6+1 Traits model; ESL/L2 analytic scales). — Supports per-area diagnostic feedback over single-score grading; verify specific sources before formal citation.

**Rhetorical root (optional)**
- Bitzer, L. (1968). "The Rhetorical Situation." *Philosophy & Rhetoric*, 1(1), 1-14. — Source of the rhetorical concerns (audience, purpose, exigence, genre) that define the HOCs.

*Sourcing note: framework and Sommers references are confirmed against multiple sources. The Allyn & Bacon definition, Flower & Hayes, and the assessment-scoring sources are included on the strength of secondary citation and standard disciplinary knowledge; verify against originals before formal use. Author surname is **Reigstad** (often mis-rendered "Registad" in secondary sources).*

---

## 7. WT0 — notes from the first experimental build

A minimal experimental router (`wt-router-1.md`) was built and test-run as the smallest viable slice of the per-library triage idea (build-sequence Stages 1-2, Writing Tutor family only). These notes record what was learned, for future development.

### 7.1 What it is

Deliberately tiny: it takes a small unit of text, works out which Writing Tutor tool(s) fit, and hands the student over with the exact text to submit to each. It routes (Axis A) and does the within-unit span hand-off, but does not run the tools, diagnose, fix, or grade. It is the concrete test of whether per-library routing works before anything larger is committed.

### 7.2 The input scope was corrected: not "one paragraph" but a small unit

The first build asked for "one paragraph." This was wrong: the WT tools accept a **sentence, a couple of sentences, or a paragraph**, and the router should accept the same range. The opening prompt was changed to state this up front and to redirect whole pieces elsewhere:

> "Give me a paragraph, a sentence, or a couple of sentences and I'll suggest which tools to run and what to submit. If you have more than that, just pick one paragraph. (For an entire piece, you can use WT3 — Find My Mistakes, WT5 — Style and Clarity Review, or one of the Structure Tutor tools.)"

This matters for the wider triage design: **the routable unit is whatever the destination tools accept, not a fixed "paragraph".** Whole pieces are explicitly out of scope for this router and are sent to WT3, WT5 or one of the Structure Tutor tools. A future router for the ST/AT families would have a *different* natural unit (the whole piece), which is consistent with the Axis-B point in §1.1 that span follows tool level.

### 7.3 Tone was the main lesson: signpost, not verdict

Test runs surfaced a tone fault that turned out to be the most important finding. When the router was made terse, its one-line reasons became **verdicts** — "your sentences don't add up to one point", "your subjects don't match" — which read as definitive, faintly dismissive, and crude. The fault was that the router has *not* analysed the text (the tool it points to will do that), so stating a finding about the writing is both presumptuous and out of lane.

The fix was to change the **grammatical mood** from declarative-verdict to tentative-signpost, naming the *kind of question* rather than pronouncing on the writing:

- not "your sentences don't add up to one point" -> "this looks like a point-and-connection question; WT2 is built for that"
- not "each sentence opens on a different subject" -> "there may be a flow question here; that's WT8"

This had a second benefit: naming the *area as a possibility* ("this looks like an X question") rather than the *fault as a fact* ("your writing does Y") also keeps the router from doing the tool's diagnostic job. The general rule for any router: **make claims about which tool fits, never claims about what is wrong with the writing.** Hedges ("looks like", "may", "if", "probably") do the tone work at almost no cost in length.

### 7.4 The persistent tensions (unresolved, for future work)

- **Diagnosis-creep.** The one place the spec still allows prose — the ordering line ("I'd probably start with WT2 because...") — is where the router drifts back toward reasoning about the writing. It is hedged now, but it remains the spot to watch. A stricter router would state order without justifying it.
- **Brevity vs honesty on short, ambiguous input.** A clear paragraph routes tightly and cleanly. A *short, vague* input (e.g. two sentences of empty throat-clearing) is genuinely ambiguous between a surface problem and a substance problem, so honest routing has to mention two tools plus an upward pointer — which costs length. This is intrinsic, not a trimming failure. An open option, not yet adopted: **if the input is very short and the signals are ambiguous, ask for a bit more text before recommending, rather than hedging across several tools.**
- **The cross-family pointer kept proving valuable.** Across test inputs (a dense PhD paragraph, empty throat-clearing, a clean-but-loaded sentence, a list-like dissertation opening), the single most useful line was often the pointer *out* of the WT family — "this may be more about your argument than this paragraph's writing." This is informal evidence for building the cross-library pointer (build-sequence Stage 3) sooner rather than later: the families blur exactly where predicted, and honest routing has to be able to point across them. Note the user's caveat: it was not always the *most* useful line, but it is important that it is present.

### 7.5 Status

Accepted as an initial routing/triage tool to run with, acknowledged as slightly verbose. It stands as the working prototype for the per-library pattern; the lessons above (input unit follows tool scope; signpost-not-verdict register; the brevity/honesty tension on short input) carry forward to any further router or triage work.
