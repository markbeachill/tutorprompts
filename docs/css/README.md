# AI Chat CSS files

These files are for site integration.

Use them when you want to paste generated chat HTML into an existing website and keep the chat styling separate from your site CSS.

## Chat-style CSS

- `aichat.css` — default chat CSS.
- `aichat-default.css` — same as `aichat.css`, included for explicit naming.
- `aichat-minimal.css` — minimal chat style.
- `aichat-dark.css` — dark chat style.
- `aichat-warm.css` — warm chat style.

## Word-friendly CSS

- `aichat-word.css` — default Word-friendly CSS.
- `aichat-word-default.css` — same as `aichat-word.css`, included for explicit naming.
- `aichat-word-plain.css` — plain Word-friendly CSS.
- `aichat-word-compact.css` — compact Word-friendly CSS.

## How to use

In the online converter, choose **Separate file** for CSS. Copy the generated HTML into your page, then link one of these CSS files from the page head:

```html
<link rel="stylesheet" href="css/aichat.css">
```

The chat CSS is scoped under `.ai-chat-page`, so it is designed not to affect the rest of your site. Your site CSS can still affect the page around the chat, but the generated chat content should remain visually consistent.

For Word-friendly output, use one of the `aichat-word*.css` files with Word-mode HTML. The Word route also includes inline styles where possible because Word and LibreOffice preserve inline styling more reliably than external CSS.
