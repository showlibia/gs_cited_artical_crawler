import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def random_sleep(minimum, maximum):
    """生成随机延时以模仿用户行为"""
    time.sleep(random.uniform(minimum, maximum))


def access_article(driver, article_url):
    """访问指定的 Google Scholar 文章页面，并点击“被引用次数”"""
    driver.get(article_url)

    # 点击“被引用次数”
    cited_by = driver.find_element(By.XPATH,'//div[@class="gs_ri"]/div[@class="gs_fl gs_flb"]/a[contains(text(), "被引用次数")]')
    cited_by.click()

    # 等待页面加载
    random_sleep(2, 5)

def find_next_page_button(driver):
    """尝试找到并返回‘下一页’按钮的 WebElement"""
    try:
        return driver.find_element(By.XPATH, "//div[@id='gs_bdy']/div[@id='gs_bdy_ccl']/div[@id='gs_res_ccl']/div[@id='gs_res_ccl_bot']/div[@id='gs_n']/center/table/tbody/tr/td[@align='left']/a")
    except Exception as e:
        print(f"查找下一页按钮时发生错误: {e}")
        return None
    
def close_citation_modal(driver):
    """Close the citation modal by clicking outside the dialog area."""
    try:
        # Wait for the overlay to be clickable
        wait = WebDriverWait(driver, 10)
        overlay = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.gs_md_wnw.gs_md_ds.gs_md_wmw.gs_vis')))

        # JavaScript to find a clickable point that is not the dialog
        clickable_area = driver.execute_script("""
            var dialog = document.getElementById('gs_cit');
            var overlay = arguments[0];

            // Find the bounds of the dialog
            var dialogRect = dialog.getBoundingClientRect();
            var overlayRect = overlay.getBoundingClientRect();

            // Check for a clickable area not overlapping with dialog
            // Example: Click at the top center of the overlay, only if it's above the dialog
            if (dialogRect.top > overlayRect.top + 10) {
                return {x: overlayRect.width / 2, y: 10};
            } 
            return null;
        """, overlay)

        if clickable_area:
            # Use Selenium to click at the calculated coordinates
            driver.execute_script("arguments[0].click();", overlay)
            print("Clicked outside the dialog to close the modal.")
        else:
            print("No clickable area outside the dialog was found.")
        
    except Exception as e:
        print(f"Failed to close citation modal by clicking outside the dialog: {e}")