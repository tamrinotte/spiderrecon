# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import requests
import pathlib
import concurrent.futures
import os

##############################

# DOWNLOAD A FILE

##############################

def download_file(url, download_folder_path):
    try:
        file_name = url.split("/")[-1]
        destination_path = pathlib.Path(download_folder_path, file_name)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(destination_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        return url, True, f"{file_name} saved to {destination_path}"
    except Exception as e:
        return url, False, str(e)

##############################

# DOWNLOAD FILES

##############################

def download_all_files(
    urls,
    download_folder_path,
    max_workers,
):
    download_folder_path = pathlib.Path(download_folder_path)
    os.makedirs(download_folder_path, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for url in urls:
            futures.append(executor.submit(download_file, url=url, download_folder_path=download_folder_path))
        for future in concurrent.futures.as_completed(futures):
            url, success, msg = future.result()
            status = "[+]" if success else "[-]"
            print(f"{status} {msg}")

    print(f"\n[+] All files are saved to {download_folder_path.resolve()}")