"""Test web interface toggle behavior."""
from typing import Any

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict[str, Any]) -> dict[str, Any]:
    """Configure browser context for testing."""
    return {
        **browser_context_args,
        "base_url": "http://localhost:5000",
    }


def test_toggle_behavior_exists(page: Page) -> None:
    """Test that clicking the text toggles between 'hey' and 'what'."""
    page.goto("/")
    text_element = page.locator("#toggle-text")
    expect(text_element).to_be_visible()

    initial_text = text_element.inner_text()
    assert initial_text in ["hey", "what"]

    text_element.click()
    expected_text = "what" if initial_text == "hey" else "hey"
    expect(text_element).to_have_text(expected_text)

    text_element.click()
    expect(text_element).to_have_text(initial_text)
