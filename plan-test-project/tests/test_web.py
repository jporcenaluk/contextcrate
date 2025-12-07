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
    
    # Wait for text to change
    page.wait_for_timeout(100)  # Small delay for any animations
    
    # Get the new text after clicking
    toggled_text = text_element.inner_text()
    
    # Verify the text changed to the other state
    if initial_text == "hey":
        assert toggled_text == "what", (
            f"Expected 'what' after clicking 'hey', got '{toggled_text}'"
        )
    else:
        assert toggled_text == "hey", (
            f"Expected 'hey' after clicking 'what', got '{toggled_text}'"
        )
    
    # Click again to toggle back
    text_element.click()
    page.wait_for_timeout(100)
    
    # Verify it toggles back to the original state
    final_text = text_element.inner_text()
    assert final_text == initial_text, (
        f"Expected to toggle back to '{initial_text}', got '{final_text}'"
    )
