import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin


class Crawler:

    def __init__(self, url, method="bfs", max_depth=2, max_pages=20):

        self.url = url
        self.method = method.lower()
        self.max_depth = max_depth
        self.max_pages = max_pages

        self.visited = set()
        self.count = 0

        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def get_links(self, url):
        try:
            soup = BeautifulSoup(
                requests.get(
                    url,
                    headers=self.headers,
                    timeout=5
                ).text,
                "html.parser"
            )
            return [
                urljoin(url, link.get("href"))
                for link in soup.find_all("a")
                if link.get("href")
            ]
        except:
            return []
        
    def bfs(self):
        dq = deque([(self.url, 0)])
        while dq:
            url, depth = dq.popleft()
            if (url in self.visited or depth > self.max_depth or self.count >= self.max_pages):
                continue
            
            self.visited.add(url)
            self.count += 1
            print(f"[BFS] {depth}: {url}")

            for href in self.get_links(url):
                print("  " * depth + f"-> {href}")
                dq.append((href, depth + 1))

    def dfs(self, url, depth=0):

        if (url in self.visited or depth > self.max_depth or self.count >= self.max_pages):
            return

        self.visited.add(url)
        self.count += 1
        print(f"[DFS] {depth}: {url}")
        
        for href in self.get_links(url):
            print("  " * depth + f"-> {href}")
            self.dfs(href, depth + 1)

    def crawl(self):
        if self.method == "bfs":
            self.bfs()
        else:
            self.dfs(self.url)

crawler = Crawler(
    url="https://chiaki.vn",
    method="bfs",   # bfs hoặc dfs
    max_depth=2,
    max_pages=10
)
crawler.crawl()
