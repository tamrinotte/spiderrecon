# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import argparse
import sys
import os
import pathlib
from modules.logging_config import error, debug
from modules.crawler import crawl_and_extract
from modules.resource_utils import load_resource_path
from modules.random_fake_user_agent import pick_a_random_user_agent
from modules.file_download import download_all_files

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
        is_file_scan_on,
        is_download_on,
        download_folder_path,
        max_pages,
        workers,
        output_file_path
    ):
        self.max_workers = workers
        self.target = target
        self.is_email_scan_on = is_email_scan_on
        self.is_phone_number_scan_on = is_phone_number_scan_on
        self.is_social_media_scan_on = is_social_media_scan_on
        self.is_file_scan_on = is_file_scan_on
        self.is_download_on = is_download_on
        self.max_pages = max_pages
        self.output_file_path = output_file_path
        self.results = {}
        self.download_folder_path = download_folder_path
        self.fake_user_agent_file = load_resource_path("data/fake_user_agents.txt")
        self.user_agent = pick_a_random_user_agent(user_agent_file=self.fake_user_agent_file)
        self.downloadable_extensions = []
        if is_file_scan_on:
            self.downloadable_extensions_file = load_resource_path("data/downloadable_extensions.txt")
            with open(self.downloadable_extensions_file, "r", encoding="utf-8") as f:
                self.downloadable_extensions = [
                    line.strip().lower()
                    for line in f
                    if line.strip() and not line.strip().startswith("#")
                ]
        self.social_media_domains = []
        if is_social_media_scan_on:
            self.social_media_domains_file = load_resource_path("data/social_media_domains.txt")
            with open(self.social_media_domains_file, "r") as f:
                self.social_media_domains = [line.strip().lower() for line in f if line.strip()]

    def scan(self):
        return crawl_and_extract(
            max_workers=self.max_workers,
            start_url=self.target,
            user_agent=self.user_agent,
            is_email_scan_on=self.is_email_scan_on,
            is_phone_number_scan_on=self.is_phone_number_scan_on,
            is_social_media_scan_on=self.is_social_media_scan_on,
            is_file_scan_on=self.is_file_scan_on,
            downloadable_extensions=self.downloadable_extensions,
            social_media_domains=self.social_media_domains,
            max_pages=self.max_pages,
        )

    def print_results(self):
        if self.results.get("emails") is not None and self.is_email_scan_on:
            print("[+] Emails found:")
            if self.results["emails"]:
                for email in self.results["emails"]:
                    print(email)
            else:
                print("No emails found.")
            print()

        if self.results.get("phones") is not None and self.is_phone_number_scan_on:
            print("[+] Phone numbers found:")
            if self.results["phones"]:
                for phone in self.results["phones"]:
                    print(phone)
            else:
                print("No phone numbers found.")
            print()

        if self.results.get("social_links") is not None and self.is_social_media_scan_on:
            print("[+] Social media links found:")
            if self.results["social_links"]:
                for link in self.results["social_links"]:
                    print(link)
            else:
                print("No social media links found.")
            print()

        if self.results.get("file_urls") is not None and self.is_file_scan_on:
            print("[+] Files found:")
            if self.results["file_urls"]:
                for url in self.results["file_urls"]:
                    print(url)

    def download(self):
        if self.is_download_on:
            print()
            download_all_files(
                urls=self.results.get("file_urls"),
                download_folder_path=self.download_folder_path,
                max_workers=self.max_workers
            )

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
                if self.results.get("file_urls") is not None:
                    f.write("\n[Files]\n")
                    for url in self.results["file_urls"]:
                        f.write(url + "\n")
            print(f"\n[+] Results saved to {self.output_file_path}")
        except Exception as e:
            error(f"Failed to save results: {e}")

    def start(self):
        emails, phones, social_links, file_urls = set(), set(), set(), set()
        try:
            emails, phones, social_links, file_urls = self.scan()
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user (KeyboardInterrupt). Printing partial results:")
        finally:
            self.results["emails"] = emails if self.is_email_scan_on else []
            self.results["phones"] = phones if self.is_phone_number_scan_on else []
            self.results["social_links"] = social_links if self.is_social_media_scan_on else []
            self.results["file_urls"] = file_urls if self.is_file_scan_on else []
            self.print_results()
            self.save_results()
            self.download()
            sys.exit()

##############################

# MAIN

##############################

def main():
    parser = argparse.ArgumentParser(
        description=(
            "SpiderRecon - Scan Websites for Emails, "
            "Phone Numbers, and Social Media Links"
        )
    )
    parser.add_argument("target", help="Target URL (e.g. https://example.com).")
    parser.add_argument(
        "-e",
        "--email_scan",
        action="store_true",
        help="Scan for email addresses."
    )
    parser.add_argument(
        "-p",
        "--phone_number_scan",
        action="store_true",
        help="Scan for phone numbers."
    )
    parser.add_argument(
        "-s",
        "--social_media_scan",
        action="store_true",
        help="Scan for social media accounts."
    )
    parser.add_argument(
        "-f",
        "--file_scan",
        action="store_true",
        help="Scan for files."
    )
    parser.add_argument(
        "-d",
        "--download",
        help="Download files and specify a directory to store found files (requires -f)."
    )
    parser.add_argument(
        "-m",
        "--max_pages",
        type=int,
        default=1000,
        help="Max number of pages to crawl (default: 1000)."
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=10,
        help="Max number of workers."
    )
    parser.add_argument("-o", "--output", help="Save results to file.")
    args = parser.parse_args()

    if not args.target.startswith("http"):
        target = "https://" + args.target
    else:
        target = args.target

    is_download_on = bool(args.file_scan and args.download)

    try:
        spiderrecon = SpiderRecon(
            target=target,
            is_email_scan_on=args.email_scan,
            is_phone_number_scan_on=args.phone_number_scan,
            is_social_media_scan_on=args.social_media_scan,
            is_file_scan_on=args.file_scan,
            is_download_on=is_download_on,
            download_folder_path=args.download,
            max_pages=args.max_pages,
            workers=args.workers,
            output_file_path=args.output,
        )
        spiderrecon.start()
    except FileNotFoundError as e:
        error(f"File not found error: {e}")
    except Exception as e:
        error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()