from playwright.sync_api import sync_playwright
from datetime import datetime
import random

print("Soubor se spustil.")

def generate_random_user():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=5)).capitalize()
    return {
        "first_name": "Testovaci",
        "last_name": f"Uzivatel{random_suffix}",
        "email": f"testuser{timestamp}@example.com",
        "password": f"Str0ngPass!{random.randint(100, 999)}",
        "birthdate": "01.01.1990"
    }

def test_register_user():
    print(">>> Spoustim test_register_user")
    user = generate_random_user()

    with sync_playwright() as p:
        print(">>> Spoustim Chromium...")
        browser = p.chromium.launch(headless=False, args=["--window-size=2560,1440"])
        context = browser.new_context(viewport={"width": 2560, "height": 1440})
        page = context.new_page()

        print(">>> Oteviram hlavni stranku...")
        page.goto("http://37.27.17.198:8084/cs/")

        print(">>> Klikam na 'Prihlasit se'...")
        page.click("text=Přihlásit se")

        print(">>> Klikám na 'Vytvorte si jej zde'...")
        page.click("text=Vytvořte si jej zde")

        print(">>> Vyplnuji formular...")
        page.check("input[name='id_gender'][value='1']")
        page.fill("input[name='firstname']", user["first_name"])
        page.fill("input[name='lastname']", user["last_name"])
        page.fill("input[name='email']", user["email"])
        page.fill("input[name='password']", user["password"])
        page.fill("input[name='birthday']", user["birthdate"])
        page.check("input[name='psgdpr']")
        page.check("input[name='customer_privacy']")

        page.wait_for_timeout(1500)

        print(">>> Odesilam formular...")
        page.click("button:has-text('ULOŽIT')")

        print(">>> Cekam na prihlaseni...")
        page.wait_for_selector("a.account", timeout=15000)

        print(">>> Kontroluji profil...")
        page.click("a.account")
        page.click("text=Informace")

        print(">>> Kontroluji vyplnene udaje...")
        firstname_val = page.get_attribute("input[name='firstname']", "value")
        lastname_val = page.get_attribute("input[name='lastname']", "value")
        email_val = page.get_attribute("input[name='email']", "value")
        birthday_val = page.get_attribute("input[name='birthday']", "value")

        assert firstname_val == user["first_name"], f"Jmeno nesouhlasi: {firstname_val} vs {user['first_name']}"
        assert lastname_val == user["last_name"], f"Prijmeni nesouhlasi: {lastname_val} vs {user['last_name']}"
        assert email_val == user["email"], f"Email nesouhlasi: {email_val} vs {user['email']}"
        assert birthday_val == user["birthdate"], f"Narozeni nesouhlasi: {birthday_val} vs {user['birthdate']}"

        page.wait_for_timeout(1500)

        print(">>> Udaje souhlasi. Test probehl uspesne.")

        print(">>> Odhlasuji uzivatele...")
        page.click("text=Odhlásit")

        print(">>> Hotovo, cekam 1,5 sekundy pred zavrenim...")
        page.wait_for_timeout(1500)
        browser.close()

if __name__ == "__main__":
    print(">>> Soubor byl spusten naprimo")
    test_register_user()
