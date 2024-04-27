import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        WebDriverWait(driver, 10).until(
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

if __name__ == "__main__":
    import json
    with open("cited_articles.json", "r") as f:
        data = json.load(f)
        
    for article in data:
        # print(data[article]["citation"])
        authors, platform, year = extract_details(data[article]["citation"])
        print(authors)
        print(platform)
        print(year)
        print()