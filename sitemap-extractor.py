import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from io import BytesIO
import time

# Custom headers to bypass restrictions
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
}

# Common sitemap URLs to check
SITEMAP_PATHS = ["/sitemap.xml", "/sitemap_index.xml", "/sitemap1.xml", "/sitemap-main.xml"]

def get_sitemap_url(website_url):
    if not website_url.startswith("http"):
        website_url = "https://" + website_url
    
    for path in SITEMAP_PATHS:
        sitemap_url = website_url.rstrip("/") + path
        response = requests.get(sitemap_url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return sitemap_url
    return None

def fetch_sitemap_urls(sitemap_url):
    try:
        response = requests.get(sitemap_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [elem.text for elem in root.findall('.//ns:loc', namespaces)]
        
        return urls
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching sitemap: {e}")
        return []
    except ET.ParseError:
        st.error("Error parsing the XML. Please check the sitemap URL.")
        return []

def fetch_all_sitemaps(main_sitemap_url):
    urls = fetch_sitemap_urls(main_sitemap_url)
    all_urls = []
    
    for url in urls:
        if url.endswith(".xml"):
            sub_urls = fetch_sitemap_urls(url)
            all_urls.extend(sub_urls)
        else:
            all_urls.append(url)
    
    return all_urls

def convert_to_csv(urls):
    df = pd.DataFrame({'URLs': urls})
    csv_data = BytesIO()
    df.to_csv(csv_data, index=False)
    csv_data.seek(0)
    return csv_data

def main():
    st.set_page_config(page_title="Sitemap URL Extractor", layout="wide")
    st.title("🔍 Sitemap URL Extractor & Downloader")
    
    website_url = st.text_input("Enter Website URL:", "https://example.com")
    
    if st.button("Fetch URLs"):
        if website_url:
            sitemap_url = get_sitemap_url(website_url)
            if sitemap_url:
                st.info(f"✅ Found Sitemap: {sitemap_url}")
                urls = fetch_all_sitemaps(sitemap_url)
                if urls:
                    st.success(f"✅ Found {len(urls)} URLs")
                    st.dataframe(urls, height=400)
                    csv_file = convert_to_csv(urls)
                    st.download_button(
                        label="📥 Download URLs as CSV",
                        data=csv_file,
                        file_name="sitemap_urls.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ No URLs found in the sitemap.")
            else:
                st.error("❌ This website does not have a sitemap.")
        else:
            st.warning("⚠️ Please enter a valid website URL")

if __name__ == "__main__":
    main()
