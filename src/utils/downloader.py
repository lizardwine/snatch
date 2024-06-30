import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def downloader(url):
    destination_folder = f"downloads/{datetime.now().strftime('%Y%m%d')}/{urlparse(url).netloc}-{datetime.now().strftime('%H%M%S')}"
    # Get the content of the URL.
    response = requests.get(url)
    if response.status_code == 200:
        # Create the destination folder if it doesn"t exist.
        if not os.path.exists(destination_folder): os.makedirs(destination_folder)

        # Parse the HTML.
        soup = BeautifulSoup(response.text, "html.parser")

        # Download the HTML.
        with open(os.path.join(destination_folder, "index.html"), "w", encoding="utf-8") as html_file:
            html_file.write(str(soup))

        # Download images, CSS, and JS.
        for tag in soup.find_all(["img", "link", "script"]):
            if tag.has_attr("src") or tag.has_attr("href"):
                resource_url = tag["src" if "src" in tag.attrs else "href"]

                # Build the complete URL.
                complete_url = urljoin(url, resource_url)

                # Download the resource and save it in the destination folder.
                download_resource(complete_url, destination_folder)

    else:
        print(f"Failed to access the URL. Status code: {response.status_code}")

def download_resource(url, destination_folder):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Extract the filename from the URL
            filename = os.path.basename(urlparse(url).path)

            # Save the resource in the destination folder
            with open(os.path.join(destination_folder, filename), "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download the resource. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading the resource {url}: {str(e)}")