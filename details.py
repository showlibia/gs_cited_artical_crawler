import re
import requests
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_url(url):
    try:
        response = requests.get(url, timeout=5)  # 设置5秒超时
        # 如果状态码在200到299之间，URL被认为是可访问的
        if 200 <= response.status_code < 300:
            return True, "URL is accessible."
        else:
            return False, f"URL returned a status code of {response.status_code}.\n"
    
    except requests.RequestException as e:
        # 处理请求相关的错误
        return False, f"An error occurred: {e}.\n"
    
def update_json_file(results: dict, article_name: str):
    existing_data = {}
    try:
        with open(f'{article_name}.json', 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        print("File not found. Creating a new one.")
    except json.JSONDecodeError:
        print("JSON decode error. Creating a new file.")

    # 合并数据
    existing_data.update(results)

    return existing_data

def extract_details(citation_text: str):
    """Extract the authors, publication platform, and year from the citation text."""
    try:
        title = re.search(r'\"(.+?)\"', citation_text)
        year_pattern = r'(\d{4})'
            
        # Extracting authors
        authors = ""
        author_match = re.search(r'^([^"]+)\.', citation_text)
        if author_match:
            authors = author_match.group(1).strip()
            # 如果存在 "et al."，则截断之前的部分
            if "et al" in authors:
                authors = authors[:authors.index(", et al")]
                authors = authors.replace(", et al", "")

        # Extracting year
        year = ""
        year_match = re.search(year_pattern, citation_text)
        if year_match:
            year = year_match.group(1)
            
        # Extracting platform
        platform = ""
        platform = citation_text.replace(f"{author_match.group()} {title.group()}", "").strip()
        platform = platform.replace(f"{title.group()}", "").strip()

        return authors, platform, year
    except Exception as e:
        print(f"Error extracting details: {e}")
        return "Authors not found", "Platform not found", "Year not found"

def extract_citation_text(driver):
    """Wait for and extract MLA citation text from the modal."""
    try:
        # Wait for the modal to become visible
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, 'gs_citd'))
        )

        # Navigate to the MLA citation text within the modal
        citation_modal = driver.find_element(By.ID, 'gs_citd')
        mla_row = citation_modal.find_element(By.XPATH, '//th[contains(text(), "MLA")]/following-sibling::td/div[@class="gs_citr"]')
        citation_text = mla_row.text

        # Extract authors, platform, and year from the citation text
        authors, platform, year = extract_details(citation_text)
    except Exception as e:
        print(f"Failed to extract MLA citation: {e}")
        return "Citation extraction failed.", None, None, None

    return citation_text, authors, platform, year

