// Minimal deterministic tests for collector-to-snippet.
// Run: node src/examples-tools/test-collector-to-snippet.mjs
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const C = require("./collector-to-snippet.js");

let failures = 0;
function check(name, cond) {
  if (cond) { console.log("  ok   " + name); }
  else { console.log("  FAIL " + name); failures++; }
}

const record = `# Test record: WT2 — Clarity Clinic

## Metadata

| Field | Value |
|---|---|
| Test code | WT2 |
| Tool tested | Clarity Clinic |

## Transcript

### Turn 1 — Toolkit
\`\`\`\`
# WT2 — Clarity Clinic v4.2

Paste a sentence.
\`\`\`\`

### Turn 1 — Student
\`\`\`\`
This area has many factors.
\`\`\`\`

### Turn 2 — Toolkit
\`\`\`\`
**Note:**

> This area has many factors.

1. What area?
2. Which factors?

| A | B |
|---|---|
| x | y |
\`\`\`\`
`;

const r = C.convert(record);
check("code derived", r.code === "WT2");
check("title from metadata", r.title === "Clarity Clinic");
check("filename", r.filename === "wt2-example-chat.html");
check("three turns", r.turns.length === 3);
check("no warnings", r.warnings.length === 0);
check("first turn chatbot", r.turns[0].role === "chatbot");
check("second turn user", r.turns[1].role === "user");
check("wrapper present", r.html.includes('<div class="ai-chat-page">'));
check("bold rendered", r.html.includes("<strong>Note:</strong>"));
check("blockquote rendered", r.html.includes("<blockquote>"));
check("ordered list rendered", r.html.includes("<ol>") && r.html.includes("<li>What area?</li>"));
check("table rendered", r.html.includes("<table>") && r.html.includes("<th>A</th>"));
check("lead placeholder present", r.html.includes("<!-- lead:"));

// determinism: same input -> identical output
const r2 = C.convert(record);
check("deterministic", r.html === r2.html);

// missing code path
const noCode = C.convert("### Turn 1 — Student\n\`\`\`\`\nhi\n\`\`\`\`");
check("warns when no code", noCode.warnings.some(w => /tool code/i.test(w)));

console.log(failures === 0 ? "\nAll tests passed." : "\n" + failures + " test(s) failed.");
process.exit(failures === 0 ? 0 : 1);
