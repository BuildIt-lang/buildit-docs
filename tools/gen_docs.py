#!/usr/bin/env python3
"""Generate static API documentation from Markdown sources."""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SRC = ROOT / "src"
DEFAULT_TEMPLATES = ROOT / "templates"
DEFAULT_ASSETS = ROOT / "assets"
DEFAULT_BUILD = ROOT / "build"


@dataclass
class Page:
    source: Path
    rel_source: Path
    rel_output: Path
    output: Path
    metadata: dict[str, str]
    body: str
    title: str


ORDERED_DIR_RE = re.compile(r"^(\d{2})_(.+)$")

CPP_KEYWORDS = {
    "alignas",
    "alignof",
    "and",
    "asm",
    "auto",
    "bool",
    "break",
    "case",
    "catch",
    "char",
    "class",
    "const",
    "constexpr",
    "continue",
    "decltype",
    "default",
    "delete",
    "do",
    "double",
    "else",
    "enum",
    "explicit",
    "extern",
    "false",
    "float",
    "for",
    "friend",
    "if",
    "inline",
    "int",
    "long",
    "mutable",
    "namespace",
    "new",
    "noexcept",
    "nullptr",
    "operator",
    "private",
    "protected",
    "public",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "struct",
    "switch",
    "template",
    "this",
    "throw",
    "true",
    "try",
    "typedef",
    "typename",
    "union",
    "unsigned",
    "using",
    "virtual",
    "void",
    "volatile",
    "while",
}

CPP_TYPES = {
    "int8_t",
    "int16_t",
    "int32_t",
    "int64_t",
    "uint8_t",
    "uint16_t",
    "uint32_t",
    "uint64_t",
    "size_t",
    "std",
    "string",
    "vector",
    "function",
}

CPP_LANGS = {"c", "cc", "cpp", "c++", "cxx", "h", "hpp", "h++", "hxx"}


INDEX_PAGE = Page(
    source=DEFAULT_SRC / "__generated_index__.md",
    rel_source=Path("__generated_index__.md"),
    rel_output=Path("index.html"),
    output=DEFAULT_BUILD / "index.html",
    metadata={
        "title": "Buildit Reference",
        "kind": "reference index",
    },
    body="",
    title="Buildit Reference",
)


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    raw = text[4:end]
    body = text[end + 5 :]
    metadata: dict[str, str] = {}

    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")

    return metadata, body


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9 _.-]+", "", value).strip().lower()
    slug = re.sub(r"[\s_]+", "-", slug)
    return slug or "section"


def unique_id(value: str, used_ids: set[str]) -> str:
    base = slugify(value)
    ident = base
    counter = 2
    while ident in used_ids:
        ident = f"{base}-{counter}"
        counter += 1
    used_ids.add(ident)
    return ident


def first_heading(markdown: str) -> str | None:
    for line in markdown.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return strip_inline_markup(match.group(1))
    return None


def body_without_first_h1(markdown: str, title: str) -> str:
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if not match:
            if line.strip():
                return markdown
            continue
        if strip_inline_markup(match.group(1)) == title:
            del lines[index]
            if index < len(lines) and not lines[index].strip():
                del lines[index]
            return "\n".join(lines)
        return markdown
    return markdown


def strip_inline_markup(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"\*([^*]+)\*", r"\1", value)
    return value.strip()


LinkResolver = Callable[[str], str]


def inline_markdown(text: str, link_resolver: LinkResolver | None = None) -> str:
    link_resolver = link_resolver or (lambda target: target)
    placeholders: list[str] = []

    def save_code(match: re.Match[str]) -> str:
        placeholders.append(f"<code>{match.group(1)}</code>")
        return f"\x00{len(placeholders) - 1}\x00"

    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", save_code, escaped)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{html.escape(link_resolver(html.unescape(m.group(2))), quote=True)}">{m.group(1)}</a>',
        escaped,
    )
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)

    for index, replacement in enumerate(placeholders):
        escaped = escaped.replace(f"\x00{index}\x00", replacement)

    return escaped


def span(class_name: str, value: str) -> str:
    return f'<span class="{class_name}">{html.escape(value)}</span>'


def highlight_cpp_line(line: str) -> str:
    index = 0
    out: list[str] = []
    at_line_start = True

    while index < len(line):
        char = line[index]

        if at_line_start and char.isspace():
            out.append(html.escape(char))
            index += 1
            continue

        if at_line_start and char == "#":
            out.append(span("tok-preprocessor", line[index:]))
            break

        at_line_start = False

        if line.startswith("//", index):
            out.append(span("tok-comment", line[index:]))
            break

        if line.startswith("/*", index):
            end = line.find("*/", index + 2)
            if end == -1:
                out.append(span("tok-comment", line[index:]))
                break
            out.append(span("tok-comment", line[index : end + 2]))
            index = end + 2
            continue

        if char in ('"', "'"):
            quote = char
            end = index + 1
            escaped = False
            while end < len(line):
                current = line[end]
                if escaped:
                    escaped = False
                elif current == "\\":
                    escaped = True
                elif current == quote:
                    end += 1
                    break
                end += 1
            out.append(span("tok-string", line[index:end]))
            index = end
            continue

        if char.isdigit():
            match = re.match(r"\d[\w.']*", line[index:])
            assert match is not None
            value = match.group(0)
            out.append(span("tok-number", value))
            index += len(value)
            continue

        if char.isalpha() or char == "_":
            match = re.match(r"[A-Za-z_][A-Za-z0-9_]*", line[index:])
            assert match is not None
            word = match.group(0)
            if word in CPP_KEYWORDS:
                out.append(span("tok-keyword", word))
            elif word in CPP_TYPES:
                out.append(span("tok-type", word))
            else:
                out.append(html.escape(word))
            index += len(word)
            continue

        out.append(html.escape(char))
        index += 1

    return "".join(out)


def highlight_code(code: str, lang: str) -> str:
    if lang.strip().lower() not in CPP_LANGS:
        return html.escape(code)
    return "\n".join(highlight_cpp_line(line) for line in code.splitlines())


def parse_table(
    lines: list[str],
    start: int,
    link_resolver: LinkResolver | None = None,
    used_ids: set[str] | None = None,
) -> tuple[str | None, int]:
    if start + 1 >= len(lines):
        return None, start

    header = lines[start]
    divider = lines[start + 1]
    if "|" not in header or not re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", divider):
        return None, start

    def cells(line: str) -> list[str]:
        return [part.strip() for part in line.strip().strip("|").split("|")]

    headers = cells(header)
    rows: list[list[str]] = []
    index = start + 2
    while index < len(lines) and "|" in lines[index].strip():
        rows.append(cells(lines[index]))
        index += 1

    out = ['<table class="doc-table">', "<thead><tr>"]
    out.extend(f"<th>{inline_markdown(cell, link_resolver)}</th>" for cell in headers)
    out.append("</tr></thead>")
    if rows:
        out.append("<tbody>")
        for row in rows:
            row_id = ""
            if row and used_ids is not None:
                row_id = f' id="{unique_id(strip_inline_markup(row[0]), used_ids)}"'
            out.append(f"<tr{row_id}>")
            out.extend(f"<td>{inline_markdown(cell, link_resolver)}</td>" for cell in row)
            out.append("</tr>")
        out.append("</tbody>")
    out.append("</table>")
    return "\n".join(out), index


def markdown_to_html(
    markdown: str,
    link_resolver: LinkResolver | None = None,
    used_ids: set[str] | None = None,
) -> str:
    used_ids = used_ids if used_ids is not None else set()
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_stack: list[str] = []
    in_code = False
    code_lang = ""
    code_lines: list[str] = []
    index = 0

    def close_paragraph() -> None:
        if paragraph:
            out.append(f"<p>{inline_markdown(' '.join(paragraph), link_resolver)}</p>")
            paragraph.clear()

    def close_lists() -> None:
        while list_stack:
            out.append(f"</{list_stack.pop()}>")

    while index < len(lines):
        line = lines[index]

        if in_code:
            if line.startswith("```"):
                klass = f' class="language-{html.escape(code_lang, quote=True)}"' if code_lang else ""
                out.append(f"<pre><code{klass}>{highlight_code(chr(10).join(code_lines), code_lang)}</code></pre>")
                in_code = False
                code_lang = ""
                code_lines = []
            else:
                code_lines.append(line)
            index += 1
            continue

        if line.startswith("```"):
            close_paragraph()
            close_lists()
            in_code = True
            code_lang = line[3:].strip()
            index += 1
            continue

        table_html, next_index = parse_table(lines, index, link_resolver, used_ids)
        if table_html:
            close_paragraph()
            close_lists()
            out.append(table_html)
            index = next_index
            continue

        stripped = line.strip()

        if not stripped:
            close_paragraph()
            close_lists()
            index += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            close_paragraph()
            close_lists()
            level = len(heading.group(1))
            text = heading.group(2)
            tryit_url = ""
            tryit_match = re.search(r"\s*\{\{\s*tryit:\s*([^}]+?)\s*\}\}\s*$", text)
            if tryit_match:
                tryit_url = tryit_match.group(1).strip()
                text = text[: tryit_match.start()].rstrip()
            ident = unique_id(strip_inline_markup(text), used_ids)
            rendered_text = inline_markdown(text, link_resolver)
            tryit = ""
            if tryit_url:
                tryit = f' <a class="tryit-link" href="{html.escape(tryit_url, quote=True)}">TryIt</a>'
            out.append(f'<h{level} id="{ident}"><a class="heading-anchor" href="#{ident}">{rendered_text}</a>{tryit}</h{level}>')
            index += 1
            continue

        if stripped == "---":
            close_paragraph()
            close_lists()
            out.append("<hr>")
            index += 1
            continue

        if stripped.startswith("> "):
            close_paragraph()
            close_lists()
            quote_lines = [stripped[2:]]
            index += 1
            while index < len(lines) and lines[index].strip().startswith("> "):
                quote_lines.append(lines[index].strip()[2:])
                index += 1
            out.append(f"<blockquote>{markdown_to_html(chr(10).join(quote_lines), link_resolver)}</blockquote>")
            continue

        ordered = re.match(r"^\s*\d+\.\s+(.+)$", line)
        unordered = re.match(r"^\s*[-*]\s+(.+)$", line)
        if ordered or unordered:
            close_paragraph()
            kind = "ol" if ordered else "ul"
            text = (ordered or unordered).group(1)
            if not list_stack or list_stack[-1] != kind:
                close_lists()
                list_stack.append(kind)
                out.append(f"<{kind}>")
            out.append(f"<li>{inline_markdown(text, link_resolver)}</li>")
            index += 1
            continue

        close_lists()
        paragraph.append(stripped)
        index += 1

    close_paragraph()
    close_lists()
    if in_code:
        klass = f' class="language-{html.escape(code_lang, quote=True)}"' if code_lang else ""
        out.append(f"<pre><code{klass}>{highlight_code(chr(10).join(code_lines), code_lang)}</code></pre>")

    return "\n".join(out)


def load_pages(src: Path, build: Path) -> list[Page]:
    pages: list[Page] = []
    for source in src.rglob("*.md"):
        rel_source = source.relative_to(src)
        if rel_source == Path("index.md"):
            raise RuntimeError("src/index.md is not supported; index.html is generated from discovered pages")
        rel_output = output_path_for_source(rel_source)
        output = build / rel_output
        text = source.read_text(encoding="utf-8")
        metadata, body = parse_front_matter(text)
        title = metadata.get("title") or first_heading(body) or rel_source.stem.replace("-", " ").title()
        pages.append(Page(source, rel_source, rel_output, output, metadata, body, title))
    return sorted(pages, key=page_sort_key)


def parse_ordered_dir(part: str, rel_source: Path) -> tuple[int, str]:
    match = ORDERED_DIR_RE.match(part)
    if not match:
        raise RuntimeError(
            f"{rel_source}: source directories must be prefixed as NN_name, for example 01_builder"
        )
    return int(match.group(1)), match.group(2)


def parse_optional_ordered_name(name: str) -> tuple[int, str]:
    match = ORDERED_DIR_RE.match(name)
    if not match:
        return 100, name
    return int(match.group(1)), match.group(2)


def output_path_for_source(rel_source: Path) -> Path:
    parent_parts = rel_source.parts[:-1]
    output_dirs = [parse_ordered_dir(part, rel_source)[1] for part in parent_parts]
    _, output_stem = parse_optional_ordered_name(rel_source.stem)
    output_name = f"{output_stem}.html"
    return Path(*output_dirs, output_name) if output_dirs else Path(output_name)


def page_sort_key(page: Page) -> tuple[int, tuple[tuple[int, str], ...], int, str]:
    is_root = str(page.rel_output.parent) == "."
    parent = () if is_root else tuple(parse_ordered_dir(part, page.rel_source) for part in page.rel_source.parts[:-1])
    file_order, _ = parse_optional_ordered_name(page.rel_source.stem)
    return (0 if is_root else 1, parent, file_order, page.title)


def page_group_label(path: Path) -> str:
    return "Reference" if str(path) == "." else str(path).replace("/", " / ")


def render_nav(pages: Iterable[Page], current: Page) -> str:
    out = ['<nav class="side-nav" aria-label="Documentation">']
    current_group = current.rel_output.parent if current.rel_output != Path("index.html") else None

    def open_group(directory: Path) -> None:
        label = page_group_label(directory)
        is_open = " open" if directory == current_group else ""
        out.append(f'<details class="nav-group"{is_open}>')
        out.append(f"<summary>{html.escape(label)}</summary>")
        out.append("<ul>")

    def search_text(page: Page) -> str:
        parts = [
            page.title,
            page.metadata.get("kind", ""),
            page.metadata.get("namespace", ""),
            page.metadata.get("header", ""),
            *metadata_list(page, "keywords"),
        ]
        return " ".join(part for part in parts if part)

    index_active = ' class="active"' if current.rel_output == Path("index.html") else ""
    out.append('<ul class="nav-root">')
    out.append(f'<li><a{index_active} href="{html.escape(relative_url(current.rel_output.parent, Path("index.html")), quote=True)}" data-search="Index">Index</a></li>')
    out.append("</ul>")

    current_dir: Path | None = None
    for page in pages:
        directory = page.rel_output.parent
        if directory != current_dir:
            if current_dir is not None:
                out.append("</ul>")
                out.append("</details>")
            open_group(directory)
            current_dir = directory

        href = relative_url(current.rel_output.parent, page.rel_output)
        active = ' class="active"' if page.rel_output == current.rel_output else ""
        out.append(
            f'<li><a{active} href="{html.escape(href, quote=True)}" '
            f'data-search="{html.escape(search_text(page), quote=True)}">{html.escape(page.title)}</a></li>'
        )

    if current_dir is not None:
        out.append("</ul>")
        out.append("</details>")
    out.append("</nav>")
    return "\n".join(out)


def render_index_content(pages: Iterable[Page], current: Page) -> str:
    out = [
        "<p>Browse documentation pages grouped by topic.</p>",
        '<section class="reference-index">',
    ]
    current_dir: Path | None = None

    for page in pages:
        directory = page.rel_output.parent
        if directory != current_dir:
            if current_dir is not None:
                out.append("</tbody></table>")
            out.append(f"<h2>{html.escape(page_group_label(directory))}</h2>")
            out.append('<table class="doc-table index-table">')
            out.append("<thead><tr><th>Page</th><th>Kind</th><th>Header</th></tr></thead><tbody>")
            current_dir = directory

        href = relative_url(current.rel_output.parent, page.rel_output)
        out.append("<tr>")
        out.append(f'<td><a href="{html.escape(href, quote=True)}">{html.escape(page.title)}</a></td>')
        out.append(f"<td>{html.escape(page.metadata.get('kind', ''))}</td>")
        header = page.metadata.get("header", "")
        header_html = f"<code>{html.escape(header)}</code>" if header else ""
        out.append(f"<td>{header_html}</td>")
        out.append("</tr>")

    if current_dir is None:
        out.append("<p>No documentation pages found.</p>")
    else:
        out.append("</tbody></table>")

    out.append("</section>")
    return "\n".join(out)


def metadata_list(page: Page, key: str) -> list[str]:
    value = page.metadata.get(key, "")
    if not value:
        return []
    return [item.strip() for item in re.split(r"[,;]", value) if item.strip()]


def write_search_index(pages: Iterable[Page], build: Path) -> None:
    entries = []
    for page in pages:
        entries.append(
            {
                "title": page.title,
                "url": page.rel_output.as_posix(),
                "kind": page.metadata.get("kind", ""),
                "namespace": page.metadata.get("namespace", ""),
                "header": page.metadata.get("header", ""),
                "keywords": metadata_list(page, "keywords"),
            }
        )

    destination = build / "assets" / "search-index.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp_destination = destination.with_suffix(destination.suffix + ".tmp")
    tmp_destination.write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if destination.exists() and destination.read_text(encoding="utf-8") == tmp_destination.read_text(encoding="utf-8"):
        tmp_destination.unlink()
        return

    tmp_destination.replace(destination)


def render_metadata(page: Page) -> str:
    rows = []
    for label, key in (("Namespace", "namespace"), ("Header", "header"), ("Since", "since")):
        value = page.metadata.get(key, "")
        if value:
            rows.append(
                "<div>"
                f"<dt>{html.escape(label)}</dt>"
                f"<dd>{html.escape(value)}</dd>"
                "</div>"
            )
    if not rows:
        return ""
    return '<dl class="doc-meta">' + "\n".join(rows) + "</dl>"


def render_breadcrumbs(page: Page) -> str:
    parts = list(page.rel_output.with_suffix("").parts)
    if not parts:
        return ""

    crumbs = ['<nav class="breadcrumbs" aria-label="Breadcrumbs"><ol>']
    crumbs.append('<li><a href="' + html.escape(relative_url(page.rel_output.parent, Path("index.html")), quote=True) + '">Index</a></li>')
    for idx, part in enumerate(parts):
        if idx == len(parts) - 1:
            crumbs.append(f"<li>{html.escape(page.title)}</li>")
        else:
            label = part.replace("-", " ")
            crumbs.append(f"<li>{html.escape(label)}</li>")
    crumbs.append("</ol></nav>")
    return "\n".join(crumbs)


def relative_url(from_dir: Path, target: Path) -> str:
    start = "." if str(from_dir) == "." else from_dir.as_posix()
    return posixpath.relpath(target.as_posix(), start=start)


def split_fragment(target: str) -> tuple[str, str]:
    path, separator, fragment = target.partition("#")
    return path, separator + fragment if separator else ""


def is_external_link(target: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target)) or target.startswith("//")


def normalize_source_path(path: Path) -> Path:
    parts: list[str] = []
    for part in path.parts:
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            else:
                parts.append(part)
            continue
        parts.append(part)
    return Path(*parts) if parts else Path(".")


def make_doc_link_resolver(current: Page, pages: Iterable[Page]) -> LinkResolver:
    pages_by_source = {page.rel_source: page for page in pages}

    def resolve(target: str) -> str:
        if is_external_link(target) or target.startswith("#"):
            return target

        raw_path, fragment = split_fragment(target)
        if not raw_path.endswith(".md"):
            return target

        source_path = Path(raw_path)
        if source_path.is_absolute():
            source_path = Path(*source_path.parts[1:])
        else:
            source_path = normalize_source_path(current.rel_source.parent / source_path)

        linked_page = pages_by_source.get(source_path)
        if linked_page is None:
            raise RuntimeError(f"{current.rel_source}: Markdown link points to missing source page: {target}")

        return relative_url(current.rel_output.parent, linked_page.rel_output) + fragment

    return resolve


def render_template(template_name: str, templates: Path, context: dict[str, str], seen: set[str] | None = None) -> str:
    seen = seen or set()
    if template_name in seen:
        raise RuntimeError(f"recursive template include: {template_name}")
    seen.add(template_name)

    path = templates / template_name
    if not path.exists():
        raise FileNotFoundError(f"template not found: {path}")

    text = path.read_text(encoding="utf-8")

    def include(match: re.Match[str]) -> str:
        return render_template(match.group(1), templates, context, seen.copy())

    text = re.sub(r'{{\s*include\s+"([^"]+)"\s*}}', include, text)
    def asset(match: re.Match[str]) -> str:
        name = match.group(1)
        return context.get(
            f"asset:{name}",
            html.escape(f"{context.get('asset_path', './assets')}/{name}", quote=True),
        )

    text = re.sub(r'{{\s*asset\s+"([^"]+)"\s*}}', asset, text)

    def variable(match: re.Match[str]) -> str:
        name = match.group(1).strip()
        return context.get(name, "")

    return re.sub(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}", variable, text)


def asset_versions(asset_root: Path) -> dict[str, str]:
    versions: dict[str, str] = {}
    if not asset_root.exists():
        return versions

    for path in asset_root.rglob("*"):
        if not path.is_file():
            continue
        rel_path = path.relative_to(asset_root).as_posix()
        versions[rel_path] = str(int(path.stat().st_mtime))
    return versions


def versioned_asset_url(root_path: str, versions: dict[str, str], asset_name: str) -> str:
    url = f"{root_path}/assets/{asset_name}"
    version = versions.get(asset_name)
    if version:
        url = f"{url}?v={version}"
    return html.escape(url, quote=True)


def build_site(src: Path, templates: Path, assets: Path, build: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"source directory not found: {src}")
    if not templates.exists():
        raise FileNotFoundError(f"templates directory not found: {templates}")

    build.mkdir(parents=True, exist_ok=True)
    versions = asset_versions(build / "assets")

    pages = load_pages(src, build)
    write_search_index(pages, build)
    search_index = build / "assets" / "search-index.json"
    if search_index.exists():
        versions["search-index.json"] = str(int(search_index.stat().st_mtime))
    index_page = Page(
        source=src / "__generated_index__.md",
        rel_source=Path("__generated_index__.md"),
        rel_output=Path("index.html"),
        output=build / "index.html",
        metadata=INDEX_PAGE.metadata,
        body="",
        title=INDEX_PAGE.title,
    )
    pages_to_render = [index_page, *pages]

    for page in pages_to_render:
        page.output.parent.mkdir(parents=True, exist_ok=True)
        depth = 0 if str(page.rel_output.parent) == "." else len(page.rel_output.parent.parts)
        root_path = "." if depth == 0 else "/".join([".."] * depth)
        content = (
            render_index_content(pages, page)
            if page.rel_output == Path("index.html")
            else markdown_to_html(body_without_first_h1(page.body, page.title), make_doc_link_resolver(page, pages))
        )
        context = {
            "title": html.escape(page.title),
            "kind": html.escape(page.metadata.get("kind", "")),
            "namespace": html.escape(page.metadata.get("namespace", "")),
            "since": html.escape(page.metadata.get("since", "")),
            "metadata": render_metadata(page),
            "content": content,
            "nav": render_nav(pages, page),
            "breadcrumbs": render_breadcrumbs(page),
            "asset_path": f"{root_path}/assets",
            "root_path": root_path,
        }
        for asset_name in versions:
            context[f"asset:{asset_name}"] = versioned_asset_url(root_path, versions, asset_name)
        template_name = page.metadata.get("template", "page.html")
        page.output.write_text(render_template(template_name, templates, context), encoding="utf-8")
        if page.rel_output == Path("index.html"):
            print(f"[generated index] -> {page.rel_output}")
        else:
            print(f"{page.rel_source} -> {page.rel_output}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC)
    parser.add_argument("--templates", type=Path, default=DEFAULT_TEMPLATES)
    parser.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    parser.add_argument("--build", type=Path, default=DEFAULT_BUILD)
    args = parser.parse_args()

    build_site(args.src, args.templates, args.assets, args.build)


if __name__ == "__main__":
    main()
