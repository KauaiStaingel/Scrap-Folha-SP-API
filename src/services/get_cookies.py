from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class SeleniumSessionCookieFetcher:
    def __init__(self, url: str, headless: bool = True):
        self.url = url
        self.headless = headless

    def fetch_cookie_header(self) -> str:
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)

        try:
            driver.get(self.url)

            # aguarda JS / trackers setarem cookies
            time.sleep(5)

            cookies = driver.get_cookies()

            # monta no formato: name=value; name=value
            cookie_header = "; ".join(
                f"{c['name']}={c['value']}" for c in cookies
            )

            return cookie_header

        finally:
            driver.quit()
