import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_details(citation_text):
    """Extract the authors, publication platform, and year from the citation text."""
    try:
        # Regex to find the authors, platform, and the year
        # Assuming author names are followed by a period that precedes the title
        author_pattern = r'^(.+?)\.\s*'

        # List of regex patterns to try for extracting platform and year
        platform_year_pattern = [
            r'\]\.\s*([^,]+),\s*(\d{4}),',   # Matches "]. Platform, Year,"
            r'\[C\]//([^,]*?),\s*(\d{4})'    # Matches "[C]//Platform, Year"
        ]
        
        # Extract authors
        authors_match = re.search(author_pattern, citation_text)
        authors = authors_match.group(1) if authors_match else "Authors not found"
        
        # Try each pattern until a match is found
        platform, year = "Platform not found", "Year not found"
        for pattern in platform_year_pattern:
            match = re.search(pattern, citation_text)
            if match:
                platform = match.group(1).strip()
                year = match.group(2)
                break  # Exit the loop once a match is found

        return authors, platform, year
    except Exception as e:
        print(f"Error extracting details: {e}")
        return "Authors not found", "Platform not found", "Year not found"

def extract_citation_text(driver):
    """Wait for and extract GB/T 7714 citation text from the modal."""
    try:
        # Wait for the modal to become visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'gs_citd'))
        )

        # Navigate to the GB/T 7714 citation text within the modal
        citation_modal = driver.find_element(By.ID, 'gs_citd')
        gb_t_7714_row = citation_modal.find_element(By.XPATH, '//th[contains(text(), "GB/T 7714")]/following-sibling::td/div[@class="gs_citr"]')
        citation_text = gb_t_7714_row.text

        # Extract authors, platform, and year from the citation text
        authors, platform, year = extract_details(citation_text)
    except Exception as e:
        print(f"Failed to extract GB/T 7714 citation: {e}")
        return "Citation extraction failed.", None, None, None

    return citation_text, authors, platform, year