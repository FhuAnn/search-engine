import requests
from bs4 import BeautifulSoup
import sqlite3
import urllib.parse

def crawler(start_url, max_pages=100):
    conn = sqlite3.connect("crawled_pages.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS pages (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              url TEXT UNIQUE,
              content TEXT
        )
    ''')
    conn.commit()

    url_frontier = [start_url]
    visited_pages = set()

    while url_frontier and len(visited_pages) < max_pages:
        url = url_frontier.pop(0)

        if url in visited_pages:
            continue

        visited_pages.add(url)  # Đánh dấu đã thăm trước khi request

        print(f"Crawling {url}")
        
        try:
            response = requests.get(url, timeout=10)  # Thêm timeout để tránh treo
            response.raise_for_status()  # Báo lỗi nếu request không thành công
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        c.execute("INSERT OR IGNORE INTO pages (url, content) VALUES(?, ?)", (url, str(soup)))
        conn.commit()

        links = soup.find_all("a", href=True)  # Tránh lỗi NoneType
        for link in links:
            href = link.get("href")
            absolute_url = urllib.parse.urljoin(url, href)  # Chuyển sang URL tuyệt đối

            if absolute_url.startswith("http") and absolute_url not in visited_pages:
                url_frontier.append(absolute_url)

    conn.close()
    print("Crawling Complete")

seed_urls = ["https://www.bbc.co.uk/news/topics/c4y26wwj72zt"]
for url in seed_urls:
    crawler(url, 50)
