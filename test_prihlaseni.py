from playwright.sync_api import sync_playwright

def test_homepage_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        page.goto("http://37.27.17.198:8084/cs/")
        assert "Přihlášení" in page.title()
        browser.close()
