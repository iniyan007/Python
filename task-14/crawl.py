import asyncio
import aiohttp
import time
import argparse
import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from collections import defaultdict, deque
import xml.etree.ElementTree as ET

visited = set()
graph = defaultdict(set)
inbound_links = defaultdict(set)
broken_links = []
redirects = []


def normalize_url(base, link):
    return urljoin(base, link.split('#')[0])


async def init_robot_parser(session, base_url):
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = RobotFileParser()
    try:
        async with session.get(robots_url) as resp:
            text = await resp.text()
            rp.parse(text.splitlines())
    except:
        pass
    return rp

async def fetch(session, url):
    try:
        start = time.time()
        async with session.get(url, allow_redirects=False) as resp:
            duration = time.time() - start
            status = resp.status

            if status in [301, 302]:
                location = resp.headers.get("Location", "")
                redirects.append((url, location))
                return None, status, duration

            if status == 404:
                broken_links.append(url)

            if status != 200:
                return None, status, duration

            text = await resp.text()
            return text, status, duration

    except Exception:
        return None, "ERR", 0


def extract_links(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    links = set()

    for tag in soup.find_all("a", href=True):
        href = tag['href']
        normalized = normalize_url(base_url, href)
        parsed = urlparse(normalized)

        if parsed.scheme in ["http", "https"]:
            links.add(normalized)

    return links


async def crawl(seed, max_depth, concurrency):
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:

        rp = await init_robot_parser(session, seed)

        queue = deque([(seed, 0)])
        visited.add(seed)

        start_time = time.time()

        while queue:
            url, depth = queue.popleft()

            if depth > max_depth:
                continue

            if not rp.can_fetch("*", url):
                continue

            html, status, duration = await fetch(session, url)

            print(f"[DEPTH {depth}] {url} {status} {round(duration,2)}s")

            if html is None:
                continue

            links = extract_links(html, url)

            for link in links:
                graph[url].add(link)
                inbound_links[link].add(url)

                if link not in visited:
                    visited.add(link)
                    queue.append((link, depth + 1))

        total_time = round(time.time() - start_time, 2)

        return total_time


def generate_sitemap(filename):
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for url in visited:
        url_tag = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url_tag, "loc")
        loc.text = url

    tree = ET.ElementTree(urlset)
    tree.write(filename)


def save_graph(filename):
    with open(filename, "w") as f:
        json.dump({k: list(v) for k, v in graph.items()}, f, indent=2)


def seo_report():
    print("\n=== SEO Audit Report ===")

    print("\nBroken Links (404):")
    for link in broken_links:
        print("-", link)

    print("\nRedirects:")
    for src, dest in redirects:
        print(f"- {src} -> {dest}")

    print("\nOrphan Pages:")
    for url in visited:
        if len(inbound_links[url]) == 0 and url != list(visited)[0]:
            print("-", url)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--concurrency", type=int, default=10)

    args = parser.parse_args()

    print("=== Crawl Started ===")
    print(f"[INFO] Seed: {args.seed}")
    print(f"[INFO] Max depth: {args.depth} | Concurrency: {args.concurrency}")

    total_time = asyncio.run(crawl(args.seed, args.depth, args.concurrency))

    print(f"\n=== Crawl Complete ({total_time}s) ===")
    print(f"Pages crawled: {len(graph)}")
    print(f"Unique URLs found: {len(visited)}")

    save_graph("crawl_graph.json")
    generate_sitemap("sitemap.xml")

    seo_report()

    print("\nSaved:")
    print("crawl_graph.json")
    print("sitemap.xml")


if __name__ == "__main__":
    main()