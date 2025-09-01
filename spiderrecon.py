# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import argparse
import sys
from modules.logging_config import error, debug
from modules.crawler import crawl_and_extract
from modules.resource_utils import load_resource_path
from modules.random_fake_user_agent import pick_a_random_user_agent

##############################

# SPIDER RECON

##############################

class SpiderRecon:
    def __init__(
        self,
        target,
        is_email_scan_on,
        is_phone_number_scan_on,
        is_social_media_scan_on,
        max_pages,
        output_file_path
    ):
        self.fake_user_agent_file = load_resource_path("data/fake_user_agents.txt")
        self.user_agent = pick_a_random_user_agent(user_agent_file=self.fake_user_agent_file)
        self.social_media_domains = []
        if is_social_media_scan_on:
            self.social_media_domains_file = load_resource_path("data/social_media_domains.txt")
            with open(self.social_media_domains_file, "r") as f:
                self.social_media_domains = [line.strip().lower() for line in f if line.strip()]
        self.target = target
        self.is_email_scan_on = is_email_scan_on
        self.is_phone_number_scan_on = is_phone_number_scan_on
        self.is_social_media_scan_on = is_social_media_scan_on
        self.max_pages = max_pages
        self.output_file_path = output_file_path
        self.results = {}

    def scan(self):
        return crawl_and_extract(
            start_url=self.target,
            user_agent=self.user_agent,
            is_email_scan_on=self.is_email_scan_on,
            is_phone_number_scan_on=self.is_phone_number_scan_on,
            is_social_media_scan_on=self.is_social_media_scan_on,
            social_media_domains=self.social_media_domains,
            max_pages=self.max_pages
        )

    def print_results(self):
        if self.results.get("emails") is not None:
            print("[+] Emails found:")
            if self.results["emails"]:
                for email in self.results["emails"]:
                    print(email)
            else:
                print("No emails found.")
            print()

        if self.results.get("phones") is not None:
            print("[+] Phone numbers found:")
            if self.results["phones"]:
                for phone in self.results["phones"]:
                    print(phone)
            else:
                print("No phone numbers found.")
            print()

        if self.results.get("social_links") is not None:
            print("[+] Social media links found:")
            if self.results["social_links"]:
                for link in self.results["social_links"]:
                    print(link)
            else:
                print("No social media links found.")

    def save_results(self):
        if not self.output_file_path:
            return
        try:
            with open(self.output_file_path, "w") as f:
                if self.results.get("emails") is not None:
                    f.write("[Emails]\n")
                    for email in self.results["emails"]:
                        f.write(email + "\n")
                if self.results.get("phones") is not None:
                    f.write("\n[Phones]\n")
                    for phone in self.results["phones"]:
                        f.write(phone + "\n")
                if self.results.get("social_links") is not None:
                    f.write("\n[Social Media Links]\n")
                    for link in self.results["social_links"]:
                        f.write(link + "\n")
            print(f"\n[+] Results saved to {self.output_file_path}")
        except Exception as e:
            error(f"Failed to save results: {e}")

    def start(self):
        emails, phones, social_links = set(), set(), set()
        try:
            emails, phones, social_links = self.scan()
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user (KeyboardInterrupt). Printing partial results:")
        finally:
            self.results["emails"] = emails if self.is_email_scan_on else []
            self.results["phones"] = phones if self.is_phone_number_scan_on else []
            self.results["social_links"] = social_links if self.is_social_media_scan_on else []
            self.print_results()
            self.save_results()
            sys.exit()

##############################

# MAIN

##############################

def main():
    parser = argparse.ArgumentParser(description="SpiderRecon - Scan Websites for Emails, Phone Numbers, and Social Media Links")
    parser.add_argument("target", help="Target URL (e.g. https://example.com).")
    parser.add_argument("-e", "--email_scan", action="store_true", help="Scan for email addresses.")
    parser.add_argument("-p", "--phone_number_scan", action="store_true", help="Scan for phone numbers.")
    parser.add_argument("-s", "--social_media_scan", action="store_true", help="Scan for social media accounts.")
    parser.add_argument("-m", "--max_pages", type=int, default=1000, help="Max number of pages to crawl (default: 1000).")
    parser.add_argument("-o", "--output", help="Save results to file.")
    args = parser.parse_args()

    if not args.target.startswith("http"):
        target = "https://" + args.target
    else:
        target = args.target

    try:
        spiderrecon = SpiderRecon(
            target=target,
            is_email_scan_on=args.email_scan,
            is_phone_number_scan_on=args.phone_number_scan,
            is_social_media_scan_on=args.social_media_scan,
            max_pages=args.max_pages,
            output_file_path=args.output,
        )
        spiderrecon.start()
    except FileNotFoundError as e:
        error(f"File not found error: {e}")
    except Exception as e:
        error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()