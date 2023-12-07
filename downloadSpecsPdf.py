import requests
from bs4 import BeautifulSoup
import re
import os

def get_latest_version_url(base_url, path):
    # Construct URL for the initial directory
    url = f"{base_url}/{path}"

    # Get HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links
    links = soup.find_all('a', href=True)

    # Filter links that lead to version folders
    version_links = [link['href'] for link in links if re.match(r"/deliver/etsi_ts/\d+_\d+/\d+/\d+\.\d+\.\d+_\d+/$", link['href'])]

    # Sort versions based on their numerical value
    sorted_versions = sorted(version_links, key=lambda x: [int(num) for num in re.findall(r'\d+', x)])

    # Return the latest version link
    latest_version_relative_url = sorted_versions[-1] if sorted_versions else None

    # Construct the full URL for the latest version
    if latest_version_relative_url:
        latest_version_url = f"https://www.etsi.org{latest_version_relative_url}"
        return latest_version_url
    else:
        return None

def download_pdf_from_directory(url, local_dir):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all pdf links
    pdf_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('.pdf')]

    for pdf_link in pdf_links:
        # Extract just the PDF filename
        pdf_filename = os.path.basename(pdf_link)

        # Construct the full URL for the PDF
        full_pdf_url = url + pdf_link

        # Download the PDF
        pdf_response = requests.get(full_pdf_url)
        local_pdf_filepath = os.path.join(local_dir, pdf_filename)

        with open(local_pdf_filepath, 'wb') as file:
            file.write(pdf_response.content)

        print(f"Downloaded: {local_pdf_filepath}")

def construct_path_from_doc_number(doc_number):
    # Assuming the document number is always in the format 'XXXXXX'
    if not doc_number.isdigit() or len(doc_number) != 6:
        raise ValueError("Document number should be a 6-digit number.")

    # Extract the first three digits and the fourth digit to determine the subfolder
    first_three_digits = int(doc_number[:3])
    fourth_digit = int(doc_number[3])

    # The start of the range is the first three digits times 100
    start_range = first_three_digits

    # Adjust start range based on the fourth digit
 
    start_range = first_three_digits * 1000 + fourth_digit * 100

    # End range is always 49 more than start range
    end_range = start_range + 99

    # Construct the path with correct formatting for the folder range
    path = f"{start_range:05d}_{end_range:05d}/{doc_number}"
    return path

# Base URL of the website
base_url = "https://www.etsi.org/deliver/etsi_ts"
# List of document numbers

doc_numbers = ["138211", "138300"]

# Local directory to save PDFs
local_dir = "downloaded_pdfs"
os.makedirs(local_dir, exist_ok=True)

for doc_number in doc_numbers:
    path = construct_path_from_doc_number(doc_number)
    print(f"Processing document number: {doc_number}")
    print(f"Path: {path}")

    # Get the URL of the latest version
    latest_version_url = get_latest_version_url(base_url, path)

    if latest_version_url:
        print(f"Accessing latest version: {latest_version_url}")

        # Download all PDFs from the directory
        download_pdf_from_directory(latest_version_url, local_dir)
    else:
        print("No versions found for the specified path.")