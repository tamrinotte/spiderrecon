# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import re
import requests
import bs4
import collections
import concurrent.futures
import urllib.parse
import phonenumbers
from modules.random_fake_user_agent import pick_a_random_user_agent

##############################

# CONSTANTS

##############################

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

##############################

# HELPER FUNCTIONS

##############################

def extract_phone_numbers(text, region=None):
    numbers = set()
    for match in phonenumbers.PhoneNumberMatcher(text, region):
        number = phonenumbers.format_number(
            match.number,
            phonenumbers.PhoneNumberFormat.INTERNATIONAL,
        )
        numbers.add(number)
    return numbers

def normalize_url(url):
    return urllib.parse.urldefrag(url)[0].rstrip("/")

def fetch_url(session, url):
    try:
        response = session.get(url, timeout=10)
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            return None, None
        return url, response.text
    except requests.RequestException as e:
        print(f"[!] Failed to fetch {url}: {e}")
        return None, None

##############################

# CRAWL & EXTRACT

##############################

def crawl_and_extract(
    max_workers,
    start_url,
    user_agent,
    is_email_scan_on,
    is_phone_number_scan_on,
    is_social_media_scan_on,
    is_file_scan_on,
    downloadable_extensions,
    social_media_domains,
    max_pages
):
    visited = set()
    emails = set()
    phones = set()
    social_links = set()
    file_urls = set()

    queue = collections.deque([normalize_url(start_url)])
    domain = urllib.parse.urlparse(start_url).netloc
    pages_crawled = 0

    session = requests.Session()
    session.headers.update({"User-Agent": f"{user_agent}"})

    print(f"[+] Starting crawl at: {start_url}")
    print(f"[+] User agent: {user_agent}")
    print(f"[+] Max pages to crawl: {max_pages}")
    print(f"[+] Domain restriction: {domain}\n")

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            while queue and len(visited) < max_pages:
                futures = {}
                while queue and len(futures) < max_workers and len(visited) < max_pages:
                    url = normalize_url(queue.popleft())
                    if url in visited:
                        continue
                    visited.add(url)
                    futures[executor.submit(fetch_url, session, url)] = url

                for future in concurrent.futures.as_completed(futures):
                    url = futures[future]
                    result_url, html = future.result()

                    if not html:
                        continue

                    print(f"[>] Crawled ({pages_crawled}): {url}")
                    pages_crawled += 1

                    if is_email_scan_on:
                        found_emails = EMAIL_REGEX.findall(html)
                        normalized_emails = {email.lower().strip().strip(".") for email in found_emails}
                        emails.update(normalized_emails)

                    if is_phone_number_scan_on:
                        found_phones = extract_phone_numbers(html)
                        phones.update(found_phones)

                    # Internal links
                    soup = bs4.BeautifulSoup(html, "lxml")
                    
                    tag_attrs = {
                        "a": "href",
                        "img": "src",
                        "video": "src",
                        "source": "src",
                        "link": "href",
                    }

                    for tag, attr in tag_attrs.items():
                        for element in soup.find_all(tag):
                            raw = element.get(attr)
                            if not raw:
                                continue
                            candidate = normalize_url(urllib.parse.urljoin(url, raw))

                            if is_social_media_scan_on:
                                netloc = urllib.parse.urlparse(candidate).netloc.lower()
                                if any(d in netloc for d in social_media_domains):
                                    social_links.add(candidate)

                            if is_file_scan_on:
                                for ext in downloadable_extensions:
                                    if candidate.lower().endswith(ext):
                                        file_urls.add(candidate)

                            parsed = urllib.parse.urlparse(candidate)
                            if (
                                parsed.netloc == domain
                                and candidate not in visited
                                and len(visited) + len(queue) < max_pages
                            ):
                                queue.append(candidate)

    except KeyboardInterrupt:
        print("\n[!] Crawl interrupted. Returning partial results.\n")
    finally:
        print("\n[✓] Crawling complete.")
        print(f"Total pages crawled: {pages_crawled}")
        print(f"Total unique emails found: {len(emails)}")
        print(f"Total unique phone numbers found: {len(phones)}")
        print(f"Total unique social media accounts found: {len(social_links)}\n")
        return emails, phones, social_links, file_urls