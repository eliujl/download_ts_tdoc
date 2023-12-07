import requests
import zipfile
import os

def download_zip_file(url, local_filename):
    try:
        response = requests.get(url)
        with open(local_filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {local_filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def unzip_file(local_filename, extract_to_folder):
    try:
        with zipfile.ZipFile(local_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_to_folder)
        print(f"Unzipped {local_filename} to {extract_to_folder}")
    except zipfile.BadZipFile:
        print(f"Error: The file {local_filename} is not a zip file or it is corrupted.")
    except Exception as e:
        print(f"Error unzipping {local_filename}: {e}")

def delete_file(local_filename):
    try:
        os.remove(local_filename)
        print(f"Deleted {local_filename}")
    except Exception as e:
        print(f"Error deleting {local_filename}: {e}")

def get_latest_version(base_url, number):
    response = requests.get(base_url + str(number))
    html = response.content.decode('utf-8')

    latest_version = None
    for line in html.splitlines():
        if 'href' in line and '38' + str(number) in line:
            parts = line.split('"')
            for part in parts:
                if part.startswith('38' + str(number)):
                    latest_version = part.split('-')[-1].split('.')[0]  # Extract version
                    break
            if latest_version:
                break

    return latest_version

def download_unzip_and_delete(base_url, number, version):
    url = base_url + str(number) + '/38' + str(number) + '-' + version + '.zip'
    local_filename = '38' + str(number) + '-' + version + '.zip'  # Local filename for saving the zip
    extract_to_folder = '.' #'38' + str(number) + '-' + version  # Folder to extract contents

    download_zip_file(url, local_filename)
    unzip_file(local_filename, extract_to_folder)
    delete_file(local_filename)

base_urls = ['https://www.3gpp.org/ftp/Specs/archive/38_series/38.']
numbers = [864]  # Example numbers
versions = ['i10']  # Example versions

for number in numbers:
    latest_version = get_latest_version(base_urls[0], number)
    if latest_version in versions:
        download_unzip_and_delete(base_urls[0], number, latest_version)
    else:
        print(f"No newer version found for number {number}. Downloading and unzipping the oldest version.")
        download_unzip_and_delete(base_urls[0], number, versions[0])
