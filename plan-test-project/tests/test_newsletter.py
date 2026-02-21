from datetime import UTC, datetime, timedelta

from plan_test_project.newsletter import (
    FeedEntry,
    render_markdown,
    score_entry,
    select_top_entries,
)


def _entry(*, title: str, summary: str, days_old: int) -> FeedEntry:
    return FeedEntry(
        title=title,
        url=f"https://example.com/{title.replace(' ', '-').lower()}",
        summary=summary,
        source="Example",
        published=datetime.now(UTC) - timedelta(days=days_old),
    )


def test_score_penalizes_slop() -> None:
    high = _entry(
        title="Technical writeup",
        summary=(
            "A deeply detailed implementation and tradeoffs analysis "
            "for production systems."
        ),
        days_old=1,
    )
    low = _entry(
        title="Viral thread recap",
        summary="Low effort AI-generated clickbait about trends.",
        days_old=1,
    )
    assert score_entry(high) > score_entry(low)


def test_select_top_entries_orders_best_first() -> None:
    long_summary = "High quality analysis with details and references." * 2
    entries = [
        _entry(title="Older", summary=long_summary, days_old=7),
        _entry(title="Fresh", summary=long_summary, days_old=0),
    ]
    top = select_top_entries(entries, limit=1)
    assert len(top) == 1
    assert top[0].title == "Fresh"


def test_render_markdown_contains_expected_sections() -> None:
    entries = [_entry(title="Entry A", summary="S" * 100, days_old=0)]
    output = render_markdown(entries, title="Anti-Slop Drop")
    assert "# Anti-Slop Drop" in output
    assert "[Entry A](https://example.com/entry-a)" in output
