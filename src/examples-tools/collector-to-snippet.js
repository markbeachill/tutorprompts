/*
 * collector-to-snippet.js
 * Deterministic converter: AI Personal Tutor Toolkit output-collector record
 * (Markdown) -> ai-chat-page example snippet (HTML).
 *
 * No dependencies. Works in the browser and under Node. This is the canonical
 * source; the create-examples page (docs/create-examples/index.html) inlines a
 * copy of this exact code, so the two never drift. If you edit this file, re-run
 * scripts/build_create_examples_page.py to refresh the page.
 *
 * Input  : the full Markdown produced by the output collector prompt.
 * Output : { code, title, turns, html, filename, warnings }
 *   - html     : the chat-region snippet to save in src/examples/
 *   - filename : suggested snippet filename, e.g. "wt2-example-chat.html"
 *
 * Markdown scope (what toolkit bubbles contain): headings, ordered/unordered
 * lists, blockquotes, GitHub tables, fenced code, paragraphs, and inline
 * **bold**, *italic*, `code`. Small and predictable, not a general engine.
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.CollectorToSnippet = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderInline(text) {
    var codes = [];
    text = text.replace(/`([^`]+)`/g, function (_, c) {
      codes.push(c);
      return "\u0000" + (codes.length - 1) + "\u0000";
    });
    text = escapeHtml(text);
    text = text.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    text = text.replace(/(^|[^*])\*([^*]+)\*/g, "$1<em>$2</em>");
    text = text.replace(/\u0000(\d+)\u0000/g, function (_, i) {
      return "<code>" + escapeHtml(codes[+i]) + "</code>";
    });
    return text;
  }

  function isTableSeparator(line) {
    return /^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)+\|?\s*$/.test(line);
  }

  function splitRow(line) {
    var t = line.trim().replace(/^\|/, "").replace(/\|$/, "");
    return t.split("|").map(function (c) {
      return c.trim();
    });
  }

  function renderMarkdown(md) {
    var lines = md.replace(/\r\n/g, "\n").split("\n");
    var out = [];
    var i = 0;
    function push(html) {
      out.push(html);
    }
    while (i < lines.length) {
      var line = lines[i];
      if (/^\s*$/.test(line)) {
        i++;
        continue;
      }
      var fence = line.match(/^\s*(```|~~~)(.*)$/);
      if (fence) {
        var marker = fence[1];
        var buf = [];
        i++;
        while (i < lines.length && lines[i].indexOf(marker) !== 0) {
          buf.push(lines[i]);
          i++;
        }
        i++;
        push("<pre><code>" + escapeHtml(buf.join("\n")) + "</code></pre>");
        continue;
      }
      var h = line.match(/^(#{1,6})\s+(.*)$/);
      if (h) {
        var level = h[1].length;
        push("<h" + level + ">" + renderInline(h[2].trim()) + "</h" + level + ">");
        i++;
        continue;
      }
      if (line.indexOf("|") !== -1 && i + 1 < lines.length && isTableSeparator(lines[i + 1])) {
        var header = splitRow(line);
        i += 2;
        var bodyRows = [];
        while (i < lines.length && lines[i].indexOf("|") !== -1 && !/^\s*$/.test(lines[i])) {
          bodyRows.push(splitRow(lines[i]));
          i++;
        }
        var tbl = ["<table>", "<thead><tr>"];
        header.forEach(function (c) {
          tbl.push("<th>" + renderInline(c) + "</th>");
        });
        tbl.push("</tr></thead>", "<tbody>");
        bodyRows.forEach(function (r) {
          tbl.push("<tr>");
          r.forEach(function (c) {
            tbl.push("<td>" + renderInline(c) + "</td>");
          });
          tbl.push("</tr>");
        });
        tbl.push("</tbody>", "</table>");
        push(tbl.join("\n"));
        continue;
      }
      if (/^\s*>/.test(line)) {
        var quote = [];
        while (i < lines.length && /^\s*>/.test(lines[i])) {
          quote.push(lines[i].replace(/^\s*>\s?/, ""));
          i++;
        }
        push("<blockquote>" + renderMarkdown(quote.join("\n")) + "</blockquote>");
        continue;
      }
      if (/^\s*\d+\.\s+/.test(line)) {
        var oItems = [];
        while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
          oItems.push(lines[i].replace(/^\s*\d+\.\s+/, ""));
          i++;
        }
        push("<ol>");
        oItems.forEach(function (it) {
          push("<li>" + renderInline(it) + "</li>");
        });
        push("</ol>");
        continue;
      }
      if (/^\s*[-*+]\s+/.test(line)) {
        var uItems = [];
        while (i < lines.length && /^\s*[-*+]\s+/.test(lines[i])) {
          uItems.push(lines[i].replace(/^\s*[-*+]\s+/, ""));
          i++;
        }
        push("<ul>");
        uItems.forEach(function (it) {
          push("<li>" + renderInline(it) + "</li>");
        });
        push("</ul>");
        continue;
      }
      var para = [];
      while (
        i < lines.length &&
        !/^\s*$/.test(lines[i]) &&
        !/^(#{1,6})\s+/.test(lines[i]) &&
        !/^\s*>/.test(lines[i]) &&
        !/^\s*[-*+]\s+/.test(lines[i]) &&
        !/^\s*\d+\.\s+/.test(lines[i]) &&
        !/^\s*(```|~~~)/.test(lines[i])
      ) {
        para.push(lines[i]);
        i++;
      }
      push("<p>" + renderInline(para.join(" ").trim()) + "</p>");
    }
    return out.join("\n");
  }

  function parseMetadata(md) {
    var meta = {};
    var rowRe = /^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$/gm;
    var m;
    while ((m = rowRe.exec(md)) !== null) {
      var key = m[1].trim().toLowerCase();
      var val = m[2].trim();
      if (key && key !== "field" && !/^:?-+:?$/.test(key)) meta[key] = val;
    }
    return meta;
  }

  function deriveCode(meta, md, warnings) {
    var code = (meta["test code"] || "").trim();
    if (!code) {
      var t = md.match(/^#\s*Test record:\s*([A-Za-z]{2}\d{1,2})\b/m);
      if (t) code = t[1];
    }
    if (!code) {
      var b = md.match(/\b([A-Za-z]{2}\d{1,2})\s*[—-]\s/);
      if (b) code = b[1];
    }
    if (!code) warnings.push("Could not determine the tool code; set it manually.");
    return code.toUpperCase();
  }

  function parseTurns(md, warnings) {
    var turns = [];
    var headRe = /^###\s*Turn\s*\d+\s*[—-]\s*(Student|Toolkit|User|Chatbot|AI)\b.*$/gim;
    var matches = [];
    var m;
    while ((m = headRe.exec(md)) !== null) {
      matches.push({ index: m.index, end: headRe.lastIndex, role: m[1].toLowerCase() });
    }
    for (var k = 0; k < matches.length; k++) {
      var start = matches[k].end;
      var stop = k + 1 < matches.length ? matches[k + 1].index : md.length;
      var segment = md.slice(start, stop);
      var fenceRe = /(`{4,}|~{4,}|`{3}|~{3})\s*\n([\s\S]*?)\n\1/;
      var fm = segment.match(fenceRe);
      var content;
      if (fm) {
        content = fm[2];
      } else {
        content = segment.trim();
        warnings.push("Turn " + (k + 1) + ": no fenced block found; used raw text.");
      }
      var role = matches[k].role;
      var isUser = role === "student" || role === "user";
      turns.push({ role: isUser ? "user" : "chatbot", markdown: content });
    }
    if (!turns.length) {
      warnings.push("No turns found. Is this a collector record with '### Turn N — Role' headers?");
    }
    return turns;
  }

  function indentBlock(html, pad) {
    return html
      .split("\n")
      .map(function (l) {
        return l.length ? pad + l : l;
      })
      .join("\n");
  }

  function renderTurn(turn) {
    var roleClass =
      turn.role === "user"
        ? "ai-chat-turn ai-chat-turn--user ai-chat-user"
        : "ai-chat-turn ai-chat-turn--chatbot ai-chat-chatbot";
    var roleLabel = turn.role === "user" ? "User" : "Chatbot";
    var body = renderMarkdown(turn.markdown);
    return (
      '    <section class="' + roleClass + '">\n' +
      '      <div class="ai-chat-role">' + roleLabel + "</div>\n" +
      '      <div class="ai-chat-bubble">\n' +
      indentBlock(body, "        ") + "\n" +
      "      </div>\n" +
      "    </section>"
    );
  }

  function buildSnippet(code, lead, turns) {
    var rows = turns.map(renderTurn).join("\n\n");
    var leadComment =
      "<!-- lead: " + (lead || "REPLACE ME WITH A ONE-LINE INTRODUCTION TO THIS EXAMPLE.") + " -->\n";
    return (
      leadComment +
      '<div class="ai-chat-page">\n' +
      '  <div class="ai-chat-window">\n' +
      '  <div class="ai-chat-log">\n' +
      rows + "\n" +
      "  </div>\n" +
      "  </div>\n" +
      "</div>\n"
    );
  }

  function convert(collectorMarkdown, options) {
    options = options || {};
    var warnings = [];
    var md = String(collectorMarkdown || "");
    var meta = parseMetadata(md);
    var code = options.code || deriveCode(meta, md, warnings);
    var title = (meta["tool tested"] || "").trim();
    var turns = parseTurns(md, warnings);
    var html = buildSnippet(code, options.lead || "", turns);
    var filename = code ? code.toLowerCase() + "-example-chat.html" : "UNKNOWN-example-chat.html";
    return { code: code, title: title, turns: turns, html: html, filename: filename, warnings: warnings };
  }

  return { convert: convert, renderMarkdown: renderMarkdown };
});
