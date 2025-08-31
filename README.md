# Spider Recon

![SpiderRecon](https://raw.githubusercontent.com/tamrinotte/spiderrecon/main/app_images/spiderrecon_logo.png)

SpiderRecon is an advanced reconnaissance tool designed to crawl websites and extract publicly available email addresses and phone numbers. It allows configurable crawling depth, ensures deduplicated results, and supports exporting findings to a file, making it suitable for OSINT research, security assessments, and contact discovery.

<br>

## Installation

1. Download the installer.

   * Kali

         curl -L https://github.com/tamrinotte/spiderrecon/releases/download/kali_v0.1.1/spiderrecon.deb -o spiderrecon.deb

2. Start the installer.

       sudo dpkg -i spiderrecon.deb

<br>

## Options

**-h, --help:** Show this help message and exit.

**target:** Target URL (e.g. https://example.com).

**-e, --email_scan:** Scan for email addresses.

**-p, --phone_number_scan:** Scan for phone numbers.

**-m MAX_PAGES, --max_pages MAX_PAGES:** Max number of pages to crawl (default: 1000).

**-o OUTPUT, --output OUTPUT:** Save results to file.

<br>

## Examples

1. Scan for email addresses:

       spiderrecon -e example.com

2. Scan for phone numbers:

       spiderrecon -p example.com

3. Scan for both email addresses and phone numbers:

       spiderrecon -e -p example.com

4. Save results to a file:

       spiderrecon -e -p example.com -o results.txt

<br>

---

# Spider Recon

![SpiderRecon](https://raw.githubusercontent.com/tamrinotte/spiderrecon/main/app_images/spiderrecon_logo.png)

SpiderRecon, web sitelerini taramak ve herkese açık e-posta adresleri ile telefon numaralarını çıkarmak için tasarlanmış gelişmiş bir keşif aracıdır. Ayarlanabilir tarama derinliği sunar, yinelenen sonuçları engeller ve bulguların dosyaya aktarılmasını destekler. Bu özellikleri sayesinde OSINT araştırmaları, güvenlik değerlendirmeleri ve iletişim keşfi için uygundur.

<br>

## Kurulum

1. Yükleyiciyi indirin.

   * Kali

         curl -L https://github.com/tamrinotte/spiderrecon/releases/download/kali_v0.1.1/spiderrecon.deb -o spiderrecon.deb

2. Yükleyiciyi başlatın.

       sudo dpkg -i spiderrecon.deb

<br>

## Seçenekler

**-h, --help:** Bu yardım mesajını göster ve çık.

**target:** Hedef URL (ör. https://example.com).

**-e, --email_scan:** Eposta adreslerini tarayın.

**-p, --phone_number_scan:** Telefon numaralarını tarayın.

**-m MAX_PAGES, --max_pages MAX_PAGES:** Taranacak maksimum sayfa sayısı (varsayılan: 1000).

**-o OUTPUT, --output OUTPUT:** Sonuçları dosyaya kaydedin.

<br>

## Örnekler

1. Eposta adreslerini tarayın:

       spiderrecon -e example.com

2. Telefon numaralarını tarayın:

       spiderrecon -p example.com

3. Hem eposta adreslerini hem de telefon numaralarını tarayın:

       spiderrecon -e -p example.com

4. Sonuçları bir dosyaya kaydedin:

       spiderrecon -e -p example.com -o results.txt