import requests
import zipfile
from io import BytesIO
import os

def download_and_unzip(url, filenames, extract_folder):
    # Create the folder if it doesn't exist
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)

    for filename in filenames:
        # Append '.zip' to the filename
        zip_filename = f"{filename}.zip"

        # Construct the full URL
        full_url = f"{url}/{zip_filename}"

        # Send a GET request to the URL
        response = requests.get(full_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Unzip the file in memory
            with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(extract_folder)
            print(f"Downloaded: {zip_filename}")
            # Optionally delete the zip file after extraction
            # os.remove(os.path.normpath(os.path.join(extract_folder, zip_filename)))
        else:
            print(f"Failed to download: {zip_filename}")

# Example usage
base_url = "https://www.3gpp.org/ftp/TSG_RAN/TSG_RAN/TSGR_102/Docs"
filenames = ['RP-232966', 'RP-233539', 'RP-233712', 'RP-232873', 'RP-233128', 'RP-233272', 'RP-233424', 'RP-233474', 'RP-233616']  # Replace with actual file names without '.zip'
download_and_unzip(base_url, filenames, './docs')
