from playwright.sync_api import sync_playwright

EMAIL = "testovaci@uzivatel.cz"
PASSWORD = "TestovaciHeslo123!"

def test_order_product():
    print(">>> Spoustim test objednavky produktu")
    with sync_playwright() as p:
        print(">>> Spoustim Chromium...")
        browser = p.chromium.launch(headless=False, args=["--window-size=2560,1440"])
        context = browser.new_context(viewport={"width": 2560, "height": 1440})
        page = context.new_page()

        print(">>> Nacitam hlavni stranku...")
        page.goto("http://37.27.17.198:8084/cs/")

        print(">>> Prihlasuji se jako existujici uzivatel...")
        page.click("text=Přihlásit se")
        page.fill("input[name='email']", EMAIL)
        page.fill("input[name='password']", PASSWORD)
        page.click("button:has-text('Přihlásit se')")

        print(">>> Prechazim do kategorie Clothes...")
        page.goto("http://37.27.17.198:8084/cs/3-obleceni")

        print(">>> Oteviram detail produktu...")
        page.click("text=Hummingbird Printed T-Shirt")

        print(">>> Pridavam produkt do kosiku z detailu...")
        page.click("button:has-text('Přidat do košíku')")

        print(">>> Cekam na potvrzeni o pridani do kosiku...")
        page.wait_for_selector("text=Produkt byl úspěšně přidán do nákupního košíku", timeout=10000)

        print(">>> Pokracuji do pokladny (1/2)...")
        page.click("a:has-text('Pokračovat do pokladny')")

        print(">>> Pokracuji do pokladny (2/2)...")
        page.click("a:has-text('Pokračovat do pokladny')")

        print(">>> Vyplnuji adresu...")
        page.wait_for_selector("input[name='address1']")
        page.fill("input[name='address1']", "Testovaci 123")
        page.wait_for_selector("input[name='city']")
        page.fill("input[name='city']", "Brno")
        page.wait_for_selector("input[name='postcode']")
        page.fill("input[name='postcode']", "602 00")
        page.wait_for_selector("select[name='id_country']")
        page.select_option("select[name='id_country']", label="Česko")

        print(">>> Odesilam formular s adresou...")
        page.click("button[name='confirm-addresses']")

        print(">>> Vybiram zpusob dopravy...")
        page.wait_for_selector("input[id='delivery_option_2']")
        page.check("input[id='delivery_option_2']")

        print(">>> Potvrzuji dopravu...")
        confirm_button = page.locator("button[name='confirmDeliveryOption']")
        confirm_button.wait_for(state="visible", timeout=10000)

        # Čekáme, dokud tlačítko není disabled
        page.wait_for_function("() => !document.querySelector('button[name=\"confirmDeliveryOption\"]').disabled")
        confirm_button.click()

        print(">>> Zaskrtavam souhlas s obchodnimi podminkami...")
        page.wait_for_selector("input#conditions_to_approve\\[terms-and-conditions\\]")
        page.check("input#conditions_to_approve\\[terms-and-conditions\\]")

        print(">>> Kontroluji informaci o platebni metode...")
        locator = page.locator("div.payment-options p.alert.alert-danger")
        locator.wait_for(state="visible", timeout=5000)
        text = locator.inner_text()
        assert "Bohužel není k dispozici žádná platební metoda." in text, \
        f"Neocekavany text: {text}"
        print(">>> Hlaseni o nedostupnosti platebni metody bylo nalezeno.")

        print(">>> Hotovo, cekam 10 sekund pred zavrenim...")
        page.wait_for_timeout(10000)
        browser.close()

if __name__ == "__main__":
    test_order_product()
