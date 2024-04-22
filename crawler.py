from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup
import requests
import json
import time
import random

# 配置 WebDriver
chrome_driver_path = "D:\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

def random_sleep(minimum, maximum):
    """生成随机延时以模仿用户行为"""
    time.sleep(random.uniform(minimum, maximum))

def access_article(article_url):
    """访问指定的 Google Scholar 文章页面，并点击“被引用次数”"""
    driver.get(article_url)

    if check_for_captcha():
        manual_verification_needed()

    # 点击“被引用次数”
    cited_by = driver.find_element(By.XPATH,'//div[@class="gs_ri"]/div[@class="gs_fl gs_flb"]/a[contains(text(), "被引用次数")]')
    cited_by.click()

    # 等待页面加载
    random_sleep(2, 5)

def parse_articles():
    """解析文章数据并保存"""
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select('#gs_res_ccl_mid .gs_ri')
    results = []

    for article in articles:
        title = article.select_one('.gs_rt').text
        author_info = article.select_one('.gs_a').text
        results.append({
            'title': title,
            'author_info': author_info
        })

    # 保存结果到 txt 文件
    with open('cited_articles.txt', 'a') as f:
        json.dump(results, f, indent=4)

    # 查找并点击下一页
    
    next_page_button = find_next_page_button()
    if next_page_button:
        next_page_button.click()
        random_sleep(2, 5)  # 随机延时，模仿用户行为
        parse_articles()
    else:
        print("已达到最后一页或未找到下一页按钮。")

def find_next_page_button():
    """尝试找到并返回‘下一页’按钮的 WebElement"""
    try:
        return driver.find_element(By.XPATH, "//div[@id='gs_bdy']/div[@id='gs_bdy_ccl']/div[@id='gs_res_ccl']/div[@id='gs_res_ccl_bot']/div[@id='gs_n']/center/table/tbody/tr/td[@align='left']/a")
    except Exception as e:
        print(f"查找下一页按钮时发生错误: {e}")
        return None

def check_for_captcha():
    """检查页面是否有验证码"""
    try:
        captcha = driver.find_element(By.ID, "captcha")
        return captcha is not None
    except:
        return False

def manual_verification_needed():
    """需要人工介入时的操作"""
    print("检测到验证码，请进行人工验证，并在完成后按回车键继续。")
    input()  # 等待用户按回车键

def main():
    article_url = "https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0%2C5&q=Defeating+hidden+audio+channel+attacks+on+voice+assistants+via+audio-induced+surface+vibrations&btnG="
    access_article(article_url)
    parse_articles()
    driver.quit()

if __name__ == "__main__":
    main()
