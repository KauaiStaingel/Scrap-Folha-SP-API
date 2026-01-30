import re
from html import unescape


class FolhaParser:
    def __init__(self, html: str):
        self.html = html

    def parse(self):
        items, seen = [], set()


        lis = re.findall(
            r'<li[^>]*class="[^"]*c-headline--newslist[^"]*"[^>]*>(.*?)</li>',
            self.html,
            flags=re.DOTALL,
        )


        clean = lambda s: re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", s))).strip()

        for li in lis:

            m = re.search(r'href="([^"]+)"', li)
            url = m.group(1) if m else ""


            m = re.search(r'<h2[^>]*class="[^"]*c-headline__title[^"]*"[^>]*>(.*?)</h2>', li, re.DOTALL)
            title = clean(m.group(1)) if m else ""


            m = re.search(r'<p[^>]*class="[^"]*c-headline__standfirst[^"]*"[^>]*>(.*?)</p>', li, re.DOTALL)
            description = clean(m.group(1)) if m else ""


            m = re.search(r'<time[^>]*class="[^"]*c-headline__dateline[^"]*"[^>]*>(.*?)</time>', li, re.DOTALL)
            date = clean(m.group(1)) if m else ""


            m = re.search(r'<img[^>]*src="([^"]+)"', li)
            image_url = m.group(1) if m else ""

            if not url or not title or url in seen:
                continue
            seen.add(url)

            items.append(
                {
                    "title": title,
                    "description": description,
                    "date": date,
                    "url": url,
                    "image_url": image_url,
                }
            )

        return items
