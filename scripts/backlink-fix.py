"""
Fix asymmetric wikilinks in the knowledge base: if A links to B but B doesn't
link back to A, append the missing backlink under B's "## Related Concepts"
section (creating the section if it's missing). Pure text manipulation, no
LLM calls.

Usage:
    uv run python scripts/backlink-fix.py            # dry run
    uv run python scripts/backlink-fix.py --apply     # apply changes
"""

from __future__ import annotations

import sys
from pathlib import Path

from config import KNOWLEDGE_DIR
from utils import extract_wikilinks, list_wiki_articles, wiki_article_exists

RELATED_HEADERS = ("## Related Concepts", "## Пов'язані концепти")


def find_missing_backlinks() -> dict[str, list[str]]:
    """Map target article (relative link) -> list of source links missing a backlink to it."""
    missing: dict[str, list[str]] = {}
    for article in list_wiki_articles():
        content = article.read_text(encoding="utf-8")
        rel = article.relative_to(KNOWLEDGE_DIR)
        source_link = str(rel).replace(".md", "").replace("\\", "/")

        for link in extract_wikilinks(content):
            if link.startswith("daily/") or link == source_link:
                continue
            if not wiki_article_exists(link):
                continue
            target_path = KNOWLEDGE_DIR / f"{link}.md"
            target_content = target_path.read_text(encoding="utf-8")
            if f"[[{source_link}]]" in target_content or f"[[{source_link}|" in target_content:
                continue
            missing.setdefault(link, [])
            if source_link not in missing[link]:
                missing[link].append(source_link)
    return missing


def apply_backlink(target_link: str, source_links: list[str], apply_changes: bool) -> None:
    target_path = KNOWLEDGE_DIR / f"{target_link}.md"
    content = target_path.read_text(encoding="utf-8")

    new_lines = "\n".join(f"- [[{s}]]" for s in source_links)

    header_found = None
    for header in RELATED_HEADERS:
        if header in content:
            header_found = header
            break

    if header_found:
        # Insert right after the header line (and its blank line, if any).
        idx = content.index(header_found) + len(header_found)
        # Skip a single following newline so we insert as the section's first lines.
        rest = content[idx:]
        insert_at = idx + (1 if rest.startswith("\n") else 0)
        new_content = content[:insert_at] + "\n" + new_lines + content[insert_at:]
    else:
        sep = "\n" if content.endswith("\n") else "\n\n"
        new_content = content.rstrip("\n") + f"\n\n---\n\n## Related Concepts\n\n{new_lines}\n"

    print(f"{target_link}.md  (+{len(source_links)} backlink(s))")
    for s in source_links:
        print(f"    <- {s}")

    if apply_changes:
        target_path.write_text(new_content, encoding="utf-8")


def main() -> None:
    apply_changes = "--apply" in sys.argv
    missing = find_missing_backlinks()

    if not missing:
        print("No missing backlinks found.")
        return

    total = sum(len(v) for v in missing.values())
    for target_link, source_links in sorted(missing.items()):
        apply_backlink(target_link, source_links, apply_changes)

    action = f"Applied {total} backlink(s) across {len(missing)} file(s)" if apply_changes else \
        f"[dry-run] {total} backlink(s) across {len(missing)} file(s) - add --apply"
    print(f"\n{action}")


if __name__ == "__main__":
    main()
