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
import requests

# 配置 WebDriver
with open('config.json') as f:
    config = json.load(f)

if sys.platform == 'win32':
    chrome_driver_path = config['chromedriver']['path_win']
elif sys.platform == 'darwin':
    chrome_driver_path = config['chromedriver']['path_mac']
    
url_heads = config['url_head']
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

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
        print(f"No article name provided. Usage: {sys.argv[0]} '<Article Name>'")
        return
    
    article_name = sys.argv[1]
    # 转换文章名称为URL编码格式
    query = quote_plus(article_name)
    # 构建搜索URL

    for i in range(len(url_heads)):
        print(query)
        article_url = f"{url_heads[i]}{query}"
        accessible, message = check_url(article_url)
        if not accessible:
            print(message)
            continue

    accessible, message = access_article(driver, article_url)

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
