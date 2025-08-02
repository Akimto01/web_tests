from playwright.sync_api import sync_playwright
from datetime import datetime
import random
import tempfile

print("Soubor se spustil.")

def generate_random_user():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return {
        "first_name": "Test",
        "last_name": "Tester",  # bez čísel, povoleny pouze písmena
        "email": f"testuser{timestamp}@example.com",
        "password": f"Str0ngPass!{random.randint(100, 999)}",  # silné heslo
        "birthdate": "1990-01-01"
    }

def test_register_user():
    print(">>> Spouštím test_register_user")
    user = generate_random_user()

    with sync_playwright() as p:
        print(">>> Spouštím Chromium...")

        user_data_dir = tempfile.mkdtemp()
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={"width": 2560, "height": 1440},
            args=["--window-position=0,0", "--window-size=2560,1440"]
        )

        page = context.pages[0] if context.pages else context.new_page()

        print(">>> Otevírám hlavní stránku...")
        page.goto("http://37.27.17.198:8084/cs/")

        print(">>> Klikám na 'Přihlásit se'...")
        page.click("text=Přihlásit se")

        print(">>> Klikám na 'Vytvořte si jej zde'...")
        page.click("text=Vytvořte si jej zde")

        print(">>> Vyplňuji formulář...")
        page.check("input[name='id_gender'][value='1']")  # Pan
        page.fill("input[name='firstname']", user["first_name"])
        page.fill("input[name='lastname']", user["last_name"])
        page.fill("input[name='email']", user["email"])
        page.fill("input[name='password']", user["password"])
        page.fill("input[name='birthday']", user["birthdate"])
        page.check("input[name='psgdpr']")  # Ochrana osobních údajů
        page.check("input[name='customer_privacy']")  # Ochrana osobních údajů

        print(">>> Odesílám formulář...")
        page.click("button:has-text('ULOŽIT')")

        print(">>> Čekám na přesměrování / potvrzení...")
        page.wait_for_timeout(3000)

        print(">>> Kontroluji přihlášení...")

        # Ověření jména uživatele
        assert page.get_by_text("Test Tester").is_visible(), "Uživatelské jméno se nezobrazilo."

        # Ověření přítomnosti tlačítka Odhlásit – přesné zacílení
        assert page.get_by_role("link", name="Odhlásit", exact=True).is_visible(), "Tlačítko 'Odhlásit' se nezobrazilo."

        print(">>> Přihlášení potvrzeno.")

        # Testovací prodleva pro vizuální ověření
        page.wait_for_timeout(10000)

        print(">>> Hotovo.")

        # Nepovinně zavřít browser (během vývoje můžeš zakomentovat)
        # context.close()

if __name__ == "__main__":
    print(">>> Soubor byl spuštěn napřímo")
    test_register_user()
