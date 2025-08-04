from playwright.sync_api import sync_playwright
import tempfile

def test_click_clothes():
    print(">>> Spoustim test test_click_clothes")

    with sync_playwright() as p:
        print(">>> Spoustim Chromium...")
        user_data_dir = tempfile.mkdtemp()
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={"width": 2560, "height": 1440},
            args=["--window-position=0,0", "--window-size=2560,1440"]
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        print(">>> Nacitam hlavni stranku...")
        page.goto("http://37.27.17.198:8084/cs/")

        print(">>> Zkousim fulltextove vyhledavani...")
        search_input = page.locator("input[name='s']")
        search_input.fill("Hummingbird Printed T-Shirt")
        search_input.press("Enter")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)

        print(">>> Kontroluji vysledek hledani...")
        if page.locator("div.search-results").count() > 0:
            no_results = page.locator("div.search-results").first.inner_text()
            print(">>> Vysledek hledani:", no_results)
        else:
            print(">>> Element s vysledkem hledani nenalezen – pokracuji...")

        print(">>> Oteviram stranku Clothes primo pres URL...")
        page.goto("http://37.27.17.198:8084/cs/3-clothes")
        page.wait_for_timeout(1000)

        print(">>> Cekam na text CLOTHES na strance...")
        page.wait_for_selector("text=CLOTHES", timeout=15000)

        print(">>> Kontroluji, ze jsme na strance CLOTHES...")
        assert page.locator("text=CLOTHES").first.is_visible(), "CLOTHES stranka se neotevrela."

        print(">>> Hledam produkt Hummingbird Printed T-Shirt...")
        product_card = page.locator("article:has-text('Hummingbird Printed T-Shirt')")
        assert product_card.is_visible(), "Produkt Hummingbird Printed T-Shirt neni viditelny."

        print(">>> Ukladam cenu pred kliknutim...")
        card_price = product_card.locator("span.price").first.inner_text().strip()
        print(">>> Cena z prehledu:", card_price)

        print(">>> Klikam na produkt podle nadpisu a cekam na URL detailu...")
        product_link = product_card.locator("h2.product-title a")
        with page.expect_navigation(wait_until="networkidle", timeout=15000):
            product_link.click()

        print(">>> Cekam na nacteni stranky s detailem produktu...")
        page.wait_for_load_state("networkidle")

        heading = page.get_by_role("heading", name="Hummingbird Printed T-Shirt")
        heading.wait_for(timeout=15000)
        assert heading.is_visible(), "Nazev produktu neni viditelny"
        print(">>> Detail produktu se nacetl.")

        print(">>> Hledam cenu na detailu produktu...")
        price_locator = page.locator("span.current-price-value").first
        price_locator.wait_for(state="visible", timeout=10000)
        detail_price = price_locator.inner_text().strip()
        print(">>> Cena z detailu:", detail_price)

        assert detail_price == card_price, f"Cena se neshoduje: prehled {card_price} vs detail {detail_price}"


        print(">>> Test byl uspesne dokonceny.")
        page.wait_for_timeout(1000)
        browser.close()

if __name__ == "__main__":
    test_click_clothes()
