# Spider Recon

![SpiderRecon](https://raw.githubusercontent.com/tamrinotte/spiderrecon/main/app_images/spiderrecon_logo.png)

SpiderRecon is an advanced reconnaissance tool designed to crawl websites and extract publicly available email addresses, phone numbers, and social media accounts. It allows configurable crawling depth, ensures deduplicated results, and supports exporting findings to a file, making it suitable for OSINT research, security assessments, and contact discovery.

<br>

## Installation

1. Download the installer.

   * Kali

         curl -L https://github.com/tamrinotte/spiderrecon/releases/download/kali_v0.1.3/spiderrecon.deb -o spiderrecon.deb

2. Start the installer.

       sudo dpkg -i spiderrecon.deb

<br>

## Options

**-h, --help:** Show this help message and exit.

**target:** Target URL (e.g. https://example.com).

**-e, --email_scan:** Scan for email addresses.

**-p, --phone_number_scan:** Scan for phone numbers.

**-s, --social_media_scan:** Scan for social media accounts.

**-f, --file_scan:** Scan for files.

**-d DOWNLOAD, --download DOWNLOAD:** Download files and specify a directory to store found files (requires -f).

**-w WORKERS, --worker WORKERS:** Maximum number of workers.

**-m MAX_PAGES, --max_pages MAX_PAGES:** Max number of pages to crawl (default: 1000).

**-o OUTPUT, --output OUTPUT:** Save results to file.

<br>

## Examples

1. Scan for email addresses:

       spiderrecon -e example.com

2. Scan for phone numbers:

       spiderrecon -p example.com

3. Scan for social media accounts:

       spiderrecon -s example.com

4. Scan for both email addresses and phone numbers:

       spiderrecon -e -p example.com

5. Save results to a file:

       spiderrecon -e -p -s example.com -o results.txt

<br>

---

# Spider Recon

![SpiderRecon](https://raw.githubusercontent.com/tamrinotte/spiderrecon/main/app_images/spiderrecon_logo.png)

SpiderRecon, web sitelerini taramak ve herkese açık e-posta adresleri, telefon numaraları ve sosyal medya hesaplarını çıkarmak için tasarlanmış gelişmiş bir keşif aracıdır. Ayarlanabilir tarama derinliği sunar, yinelenen sonuçları engeller ve bulguların dosyaya aktarılmasını destekler. Bu özellikleri sayesinde OSINT araştırmaları, güvenlik değerlendirmeleri ve iletişim keşfi için uygundur.

<br>

## Kurulum

1. Yükleyiciyi indirin.

   * Kali

         curl -L https://github.com/tamrinotte/spiderrecon/releases/download/kali_v0.1.3/spiderrecon.deb -o spiderrecon.deb

2. Yükleyiciyi başlatın.

       sudo dpkg -i spiderrecon.deb

<br>

## Seçenekler

**-h, --help:** Bu yardım mesajını göster ve çık.

**target:** Hedef URL (ör. https://example.com).

**-e, --email_scan:** Eposta adresi taraması yap.

**-p, --phone_number_scan:** Telefon numarası taraması yap.

**-s, --social_media_scan:** Sosyal medya taraması yap.

**-f, --file_scan:** Dosya taraması yap.

**-d DOWNLOAD, --download DOWNLOAD:** Dosyaları indir ve bulunan dosyaları depolamak için bir klasör belirt (‑f gerektirir).

**-w WORKERS, --worker WORKERS:** Kullanılacak maksimum işçi sayısı.

**-m MAX_PAGES, --max_pages MAX_PAGES:** Taranacak maksimum sayfa sayısı (varsayılan: 1000).

**-o OUTPUT, --output OUTPUT:** Sonuçları dosyaya kaydedin.

<br>

## Örnekler

1. Eposta adresleri için tarama yap:

       spiderrecon -e example.com

2. Telefon numaraları için tarama yap:

       spiderrecon -p example.com

3. Sosyal medya hesapları için tarama yap:

       spiderrecon -s example.com

4. Hem eposta adresleri hem de telefon numaraları için tarama yap:

       spiderrecon -e -p example.com

5. Sonuçları bir dosyaya kaydedin:

       spiderrecon -e -p -s example.com -o results.txt