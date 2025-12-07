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
    """Test that clicking the text toggles between 'hey' and 'what'.
    
    This test verifies:
    1. The page loads successfully
    2. There is clickable text
    3. Clicking toggles between 'hey' and 'what' states
    4. Both states are achievable through clicking
    """
    # Navigate to the home page
    page.goto("/")
    
    # Find the clickable text element (should initially show 'hey' or 'what')
    # Using a test-id or accessible role for reliable selection
    text_element = page.locator("#toggle-text")
    
    # Verify element exists and is visible
    expect(text_element).to_be_visible()
    
    # Get the initial text
    initial_text = text_element.inner_text()
    assert initial_text in ["hey", "what"], (
        f"Initial text should be 'hey' or 'what', got '{initial_text}'"
    )
    
    # Click to toggle
    text_element.click()
    
    # Verify text changed to the other state using Playwright's built-in waiting
    expected_text = "what" if initial_text == "hey" else "hey"
    expect(text_element).to_have_text(expected_text)
    
    # Click again to toggle back
    text_element.click()
    expect(text_element).to_have_text(initial_text)
