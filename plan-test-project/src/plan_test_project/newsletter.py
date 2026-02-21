"""Utilities for building an anti-slop newsletter from curated feeds."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SLOP_PATTERNS = (
    r"\bai-generated\b",
    r"\bclickbait\b",
    r"\blow effort\b",
    r"\bviral thread\b",
)


@dataclass(slots=True, frozen=True)
class FeedEntry:
    title: str
    url: str
    summary: str
    source: str
    published: datetime


def load_feed_config(path: str | Path) -> list[dict[str, Any]]:
    """Load feed configuration JSON containing a `feeds` list."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    feeds = data.get("feeds", [])
    if not isinstance(feeds, list):
        raise ValueError("`feeds` must be a list")
    return feeds


def score_entry(entry: FeedEntry) -> int:
    """Compute quality score (higher is better, slop gets penalized)."""
    score = 100
    text = f"{entry.title} {entry.summary}".lower()
    for pattern in SLOP_PATTERNS:
        if re.search(pattern, text):
            score -= 30

    if len(entry.summary.strip()) < 80:
        score -= 10

    age_days = (datetime.now(UTC) - entry.published).days
    score -= min(age_days, 14)
    return max(score, 0)


def select_top_entries(entries: list[FeedEntry], *, limit: int = 10) -> list[FeedEntry]:
    """Sort by score and freshness, then return up to `limit` entries."""
    return sorted(
        entries,
        key=lambda entry: (score_entry(entry), entry.published.timestamp()),
        reverse=True,
    )[:limit]


def render_markdown(entries: list[FeedEntry], *, title: str) -> str:
    """Render newsletter markdown from ranked entries."""
    lines = [f"# {title}", "", "Curated low-slop links:", ""]
    for entry in entries:
        lines.extend(
            [
                f"- [{entry.title}]({entry.url})",
                f"  - Source: {entry.source}",
                f"  - Published: {entry.published.date().isoformat()}",
                f"  - Why it matters: {entry.summary.strip()}",
            ]
        )
    return "\n".join(lines) + "\n"
