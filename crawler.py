import sys
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import quote_plus
from details import extract_citation_text
from click import access_article, random_sleep, find_next_page_button, close_citation_modal, check_captcha, attempt_citation_click
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 配置 WebDriver
import json

with open('config.json') as f:
    config = json.load(f)

chrome_driver_path = config['chromedriver']['path']

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

def parse_articles(driver, results, article_count):
    """解析文章数据并保存"""
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select('#gs_res_ccl_mid .gs_r.gs_or.gs_scl')


    for index, article in enumerate(articles, start=1):
        article = article.select_one('.gs_ri')
        title = article.select_one('.gs_rt').text
        
        article_element = driver.find_elements(By.CSS_SELECTOR, '#gs_res_ccl_mid .gs_ri')[index - 1]
        cite_button = article_element.find_element(By.CSS_SELECTOR, 'a.gs_or_cit.gs_or_btn.gs_nph')
        
        # Execute JavaScript click
        driver.execute_script("arguments[0].scrollIntoView();", cite_button)
        cite_button.click()

        attempt_citation_click(driver, cite_button)

        # Extract citation in MLA format
        try:
            # Ensure the citation modal is fully loaded
            citation_text, authors, platform, year = extract_citation_text(driver)
        except Exception as e:
            print(f"Failed to extract citation: {e}")
            citation_text = "Citation extraction failed."

        random_sleep(0.5,1)
        # Close the citation modal if needed
        close_citation_modal(driver)

         # Compile results using a unique key
        results[f'article_{article_count}'] = {
            'title': title,
            'citation': citation_text,
            'authors': authors,
            'platform': platform,
            'year': year
        }
        article_count += 1  # Increment the counter for the next entry

    # 查找并点击下一页
    next_page_button = find_next_page_button(driver)
    if next_page_button:
        next_page_button.click()
        random_sleep(1.5, 3)  # 随机延时，模仿用户行为
        parse_articles(driver, results, article_count)
    else:
        print("Reached the last page or no next page button found.")

def main():
    if len(sys.argv) < 2:
        print("No article name provided. Usage: script.py '<Article Name>'")
        return
    
    article_name = sys.argv[1]
    # 转换文章名称为URL编码格式
    query = quote_plus(article_name)
    # 构建搜索URL
    article_url = f"https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0%2C5&q={query}"    
    driver.get(article_url)
    # 检查是否有人机验证
    # check_captcha(driver)
    # check_captcha(driver)

    access_article(driver, article_url)
    # 检查是否有人机验证
    # check_captcha(driver)
    # maximze the window
    driver.maximize_window()
    # 解析文章数据
    results = {}
    article_count = 1
    parse_articles(driver, results, article_count)
    with open('cited_articles.json', 'w') as f:
        json.dump(results, f, indent=4)
    driver.quit()

if __name__ == "__main__":
    main()
