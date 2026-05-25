# buildit-docs

A small static documentation generator with a cppreference-inspired layout.

## Layout

- `src/**/*.md`: source documentation pages. Do not create `src/index.md`;
  `build/index.html` is always generated from the discovered page list.
  Directories under `src/` must be prefixed as `NN_name` to define ordering;
  the generated output trims the prefix.
- `templates/*.html` and `templates/*.html.inc`: page templates and reusable includes.
- `assets/`: CSS, JavaScript, and other static files copied incrementally by
  `make` into `build/assets/`.
- `build/`: generated deployable site.

## Build

```sh
make
```

This copies changed assets into `build/assets/`, generates `build/index.html`
automatically, then mirrors the `src/` tree into `build/`, converting every
Markdown file into an HTML page and trimming numeric directory prefixes. For
example:

```text
src/01_builder/dyn-var.md -> build/builder/dyn-var.html
```

Run a local server with:

```sh
make serve
```

## Markdown Metadata

Pages may start with a simple front matter block:

```md
---
title: vector
kind: class template
namespace: buildit
since: 1.0
header: buildit/vector.h
keywords: dynamic array, container, sequence
template: page.html
---
```

If `title` is omitted, the generator uses the first `# Heading` in the file,
then falls back to the filename.

`keywords` is an optional comma- or semicolon-separated list used by the
generated search index.

Available template variables include `title`, `kind`, `namespace`, `since`,
`metadata`, `content`, `nav`, `breadcrumbs`, `asset_path`, and `root_path`.
The `nav` sidebar and generated `build/index.html` page are both compiled from
the full list of discovered Markdown files.

## Links Between Pages

Use normal Markdown links to `.md` source files:

```md
[`builder::dyn_var`](dyn-var.md)
[`block::stmt`](../02_block/stmt.md)
```

The generator validates those targets and rewrites them to the correct `.html`
paths in `build/`. Fragments are preserved, so `dyn-var.md#member-functions`
becomes the matching generated HTML link.

## Template Includes

Templates support:

```html
{{ include "head.html.inc" }}
{{ title }}
{{ content }}
```

Includes are resolved from the `templates/` directory.
