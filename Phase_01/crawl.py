import json
import re
import time
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


BASE_URL = "https://chiaki.vn/"
OUTPUT_FILE = "chiaki_documents.json"


def clean_text(text):
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_between(pattern, html):
    result = re.search(pattern, html, flags=re.S)
    if result:
        return clean_text(result.group(1))
    return ""


def fetch_html(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    request = Request(url, headers=headers)
    response = urlopen(request, timeout=15)
    html = response.read().decode("utf-8", errors="ignore")
    response.close()
    return html


def get_links(url, html):
    links = re.findall(r'<a[^>]+href=["\'](.*?)["\']', html)
    good_links = []

    for link in links:
        full_link = urljoin(url, link.split("#")[0])
        domain = urlparse(full_link).netloc

        if domain in ["chiaki.vn", "www.chiaki.vn"] and full_link not in good_links:
            good_links.append(full_link)

    return good_links


def parse_document(url, html):
    title = get_between(r"<title>(.*?)</title>", html)
    description = get_between(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
        html,
    )
    body_text = clean_text(html)

    return {
        "url": url,
        "title": title,
        "description": description,
        "content": body_text[:2000],
    }


def crawl_chiaki(max_pages=20):
    queue = [BASE_URL]
    visited = []
    documents = []

    while len(queue) > 0 and len(documents) < max_pages:
        url = queue.pop(0)

        if url in visited:
            continue

        try:
            print("Dang crawl:", url)
            html = fetch_html(url)
            visited.append(url)

            document = parse_document(url, html)
            if document["title"] != "":
                documents.append(document)

            links = get_links(url, html)
            for link in links:
                if link not in visited and link not in queue:
                    queue.append(link)

            time.sleep(0.5)
        except Exception as error:
            print("Loi:", error)

    return documents


def save_documents(documents, output_file=OUTPUT_FILE):
    file = open(output_file, "w", encoding="utf-8")
    json.dump(documents, file, ensure_ascii=False, indent=2)
    file.close()


if __name__ == "__main__":
    data = crawl_chiaki()
    save_documents(data)
    print("Da luu", len(data), "documents vao", OUTPUT_FILE)
