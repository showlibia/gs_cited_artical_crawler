import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_details(citation_text):
    """Extract the authors, publication platform, and year from the citation text."""
    try:

        author_pattern = r'^(.+?)(?:, et al\.|, and|\.)'
        title_pattern = r'\"(.+?)\"'
        platform_pattern = r'\"\.\s*(.+?)\s*\(\d{4}\)'
        year_pattern = r'\((\d{4})\)'
        
        authors_match = re.search(author_pattern, citation_text)
        title_match = re.search(title_pattern, citation_text)
        platform_match = re.search(platform_pattern, citation_text)
        year_match = re.search(year_pattern, citation_text)

        authors = authors_match.group(1) if authors_match else "Authors not found"
        title = title_match.group(1) if title_match else ""
        platform = platform_match.group(1) if platform_match else "Platform not found"
        year = year_match.group(1) if year_match else "Year not found"

        platform = platform.replace(f"\"{title}\"", "").strip()

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