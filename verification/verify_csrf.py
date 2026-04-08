from playwright.sync_api import Page, expect, sync_playwright
import os

def test_csrf_token_present(page: Page):
    # Go to the homepage
    page.goto("http://localhost:5000")

    # Wait for the form to be visible
    expect(page.locator("#searchForm")).to_be_visible()

    # Check if the CSRF token input exists
    csrf_token = page.locator('input[name="csrf_token"]')

    # Verify it has a non-empty value
    value = csrf_token.get_attribute("value")
    print(f"CSRF Token value: {value}")
    assert value and len(value) > 0

    # Take a screenshot of the page
    os.makedirs("verification", exist_ok=True)
    screenshot_path = os.path.join("verification", "csrf_token_present.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_csrf_token_present(page)
        finally:
            browser.close()
