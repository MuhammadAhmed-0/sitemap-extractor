# Sitemap URL Extractor

🔍 **Sitemap URL Extractor** is a simple yet powerful tool built using **Streamlit** and **Python**. It allows users to extract all URLs from a website's sitemap, download them in CSV format, and perform easy sitemap analysis.

## Features

- **Automatic Sitemap Detection**: Detects the sitemap automatically from common sitemap paths (`/sitemap.xml`, `/sitemap_index.xml`, etc.).
- **Extract URLs**: Fetches URLs from sitemaps and sub-sitemaps.
- **CSV Download**: Downloads the extracted URLs as a CSV file for further use.
- **Simple Interface**: User-friendly interface with **Streamlit**.

## Requirements

To run the tool, you need Python 3.x installed along with the following Python packages:

- **requests**: For making HTTP requests.
- **xml.etree.ElementTree**: For parsing XML data.
- **pandas**: For data manipulation and creating the CSV file.
- **streamlit**: For creating the web interface.

## Results
![image](https://github.com/user-attachments/assets/8bd0a201-a7ad-4c49-ae84-8432929f6dc0)


Install the dependencies using pip:

```bash
pip install requests pandas streamlit
