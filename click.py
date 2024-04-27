import time
import random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def random_sleep(minimum, maximum):
    """生成随机延时以模仿用户行为"""
    time.sleep(random.uniform(minimum, maximum))


def access_article(driver, article_url):
    """访问指定的 Google Scholar 文章页面，并点击“Cited by”"""
    # driver.get(article_url)
    random_sleep(1, 2)
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
        else:
            print("No clickable area outside the dialog was found.")
        
    except Exception as e:
        print(f"Failed to close citation modal by clicking outside the dialog: {e}")

def check_captcha(driver):
    """Check for the presence of a CAPTCHA and wait for the user to complete it."""
    try:
        # Check for the presence of a CAPTCHA element on the page
        captcha_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'gs_captcha_f')))

        if captcha_element:
            print("CAPTCHA detected. Please complete the CAPTCHA within 10 minutes.")
            # Wait for up to 10 minutes for the CAPTCHA to be completed
            WebDriverWait(driver, 600).until(EC.staleness_of(captcha_element))
            print("CAPTCHA completed.")

            
    except TimeoutException:
        print("CAPTCHA was not completed within 10 minutes.")

def attempt_citation_click(driver, cite_button):
    while True:
        try:
            # Check if the system error message is visible
            alert_message = WebDriverWait(driver, 0.5).until(
                EC.visibility_of_element_located((By.ID, "gs_alrt_m"))
            )
            if "系统目前无法执行此操作，请稍后再试。" in alert_message.text:
                print("System error detected. Waiting for 2 minutes before retrying.")
                time.sleep(120)  
                # driver.refresh()  # Refresh the page
                cite_button.click()
                check_captcha(driver)
            else:
                break  # If no error, break the loop

        except TimeoutException:
            print("Failed to perform the operation within the expected time.")
            break