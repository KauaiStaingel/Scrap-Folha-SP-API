from services.search_query import SearchQueryBuilder
from services.excel import CsvNewsSaver
from services.get_cookies import SeleniumSessionCookieFetcher
from services.get_news import HtmlFetcher
from services.html_parser import FolhaParser
import time


def orchestrator_main():
    max_retries = 3
    attempt = 0

    query_builder = SearchQueryBuilder()
    encoded_query = query_builder.ask()

    search_url = f"https://search.folha.uol.com.br/?q={encoded_query}&site=todos"

    while attempt < max_retries:
        driver = None
        try:
            attempt += 1
            print(f"Tentativa {attempt} de {max_retries}")


            url = "https://search.folha.uol.com.br/"

            fetcher = SeleniumSessionCookieFetcher(url)
            session_cookies = fetcher.fetch_cookie_header()


            fetcher = HtmlFetcher(
                url=search_url,
                cookie_header=session_cookies
            )

            html = fetcher.fetch_html()

            parser = FolhaParser(html)
            noticias = parser.parse()



            saver = CsvNewsSaver(noticias)
            saver.save("noticias.csv")

            return 

        except Exception as e:
            print(f"Erro na tentativa {attempt}: {e}")

            if attempt >= max_retries:
                print("Número máximo de tentativas atingido")
                raise

            time.sleep(2)

        finally:
            if driver:
                driver.quit()
