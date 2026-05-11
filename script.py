
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin

URL = "https://www.assemblee-nationale.fr/dyn/17/questions/recherche?rechercheTextuelle=recherche+and+université&limit=10&order=numero&sort=desc"
BASE_URL = "https://www.assemblee-nationale.fr"

response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

fg = FeedGenerator()
fg.title("Questions AN - Université")
fg.link(href=URL)
fg.description("Suivi automatique")

links = soup.select("a[href*='/questions/']")

seen = set()

for link in links:
    href = link.get("href")
    title = link.get_text(strip=True)

    if not href or not title:
        continue

    full_link = urljoin(BASE_URL, href)

    if full_link in seen:
        continue
    seen.add(full_link)

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=full_link)

fg.rss_file("feed.xml")

print("✅ feed.xml mis à jour")
