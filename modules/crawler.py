# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import re
import requests
import bs4
import collections
import concurrent.futures
import urllib.parse
import phonenumbers

##############################

# REGEX

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
    # Remove fragments like #section, strip trailing slashes
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

def crawl_and_extract(start_url, is_email_scan_on, is_phone_number_scan_on, max_pages):
    visited = set()
    emails = set()
    phones = set()
    queue = collections.deque([normalize_url(start_url)])

    domain = urllib.parse.urlparse(start_url).netloc
    pages_crawled = 0
    max_workers = 10  # Number of threads

    session = requests.Session()

    print(f"[+] Starting crawl at: {start_url}")
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

                    # Email extraction
                    if is_email_scan_on:
                        found_emails = EMAIL_REGEX.findall(html)
                        normalized_emails = {email.lower().strip().strip(".") for email in found_emails}
                        if normalized_emails:
                            print(f"[+] Found {len(normalized_emails)} email(s) at {url}")
                        emails.update(normalized_emails)

                    # Phone extraction
                    if is_phone_number_scan_on:
                        found_phones = extract_phone_numbers(html)
                        if found_phones:
                            print(f"[+] Found {len(found_phones)} phone number(s) at {url}")
                        phones.update(found_phones)

                    # Internal links
                    soup = bs4.BeautifulSoup(html, "lxml")
                    for link in soup.find_all("a", href=True):
                        next_url = normalize_url(urllib.parse.urljoin(url, link["href"]))
                        if (
                            urllib.parse.urlparse(next_url).netloc == domain
                            and next_url not in visited
                            and len(visited) + len(queue) < max_pages
                        ):
                            queue.append(next_url)

    except KeyboardInterrupt:
        print("\n[!] Crawl interrupted. Returning partial results.\n")
    finally:
        print("\n[✓] Crawling complete.")
        print(f"Total pages crawled: {pages_crawled}")
        print(f"Total unique emails found: {len(emails)}")
        print(f"Total unique phone numbers found: {len(phones)}\n")
        return emails, phones
