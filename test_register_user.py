from playwright.sync_api import sync_playwright
from datetime import datetime
import random

def generate_random_user():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return {
        "first_name": "Test",
        "last_name": f"User{timestamp}",
        "email": f"testuser{timestamp}@example.com",
        "password": f"Passw0rd!{random.randint(100, 999)}",
        "birthdate": "01.01.1990"
    }

def test_register_user():
    user = generate_random_user()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        # 1. Otevření hlavní stránky
        page.goto("http://37.27.17.198:8084/cs/")

        # 2. Kliknutí na "Přihlásit se"
        page.click("text=Přihlásit se")

        # 3. Najlezení a kliknutí na "Nemáte účet? Vytvořte si jej zde"
        page.click("text=Vytvořte si jej zde")

        # 4. Vyplnění registračního formulář
        page.check("input[name='id_gender'][value='1']")  # Pan
        page.fill("input[name='firstname']", user["first_name"])
        page.fill("input[name='lastname']", user["last_name"])
        page.fill("input[name='email']", user["email"])
        page.fill("input[name='password']", user["password"])
        page.fill("input[name='birthday']", user["birthdate"])
        page.check("input[name='psgdpr']")  # Ochrana osobních údajů

        # 5. Odeslání formuláře
        page.click("button:has-text('ULOŽIT')")

        # Nepovinně: počkáme na potvrzení / přesměrování
        page.wait_for_timeout(3000)

        browser.close()
