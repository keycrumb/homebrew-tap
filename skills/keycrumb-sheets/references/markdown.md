# Markdown authoring

Use one leading H1 as the sheet title, a short introduction and focused H2 sections.
Place UTF-8 `.md` files at the top level of the selected library, at most 2 MiB each.
Use ordinary supported Markdown: headings, paragraphs, lists, tables, code and images.
Do not rely on HTML, CSS, metadata frontmatter or embedded widgets for layout.

Small tables such as `Action | Command` or `Shortcut | Action` scan well. Omit row
numbers and index columns. Aim for roughly five useful entries per section when
that fits the topic; this is a readability target, not a format limit.

Use inline code for a single command. Escape literal table pipes with `\|`, even
inside table code. Put multiline commands, awkward backticks or complex pipe
expressions in separate fenced blocks instead. Pick a fence longer than any run
of backticks in its contents. Keep unrelated commands in separate copy targets.
Do not include shell prompts, line numbers or citations in copied command text.
Explain placeholders outside code; do not execute commands while writing a sheet.

Images must be local, decodable files inside the selected library, at most 10 MiB.
They resolve relative to the library root. PNG is a portable choice. The 256 × 256
JSON-icon requirement does not apply to Markdown illustrations. Provide useful alt
text and include the image in the deliverable:

```text
My Library/
  commands.md
  editor.keycrumb.json
  icons/editor.png
  images/workflow.png
```

The Markdown image is `![Workflow](images/workflow.png)`. `icons/` and `images/`
are conventions, not mandated folder names. Remote, absolute and escaping paths
are unsuitable. Review actual rendering and copying in KeyCrumb when possible;
text or regex checks cannot prove either behavior.

See the [complete example](../assets/example-library/commands.md).
