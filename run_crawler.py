import sys
import subprocess

def run_spider(article_name, total_cited_number, pages_per_batch=15):
    """
    运行爬虫程序，按照指定的每次处理的页数来分批处理。

    Args:
    - article_name: 文章名称
    - total_cited_number: 总的被引用次数
    - pages_per_batch: 每批次处理的最大页数，默认为15
    """

    total_pages = total_cited_number // 10

    start_page = 1
    while start_page <= total_pages:
        end_page = min(start_page + pages_per_batch - 1, total_pages)
        print(f"Processing from page {start_page} to {end_page}...")
        
        # 构建命令行参数
        command = ['python', 'crawler.py', article_name, str(start_page), str(end_page)]
        
        # 调用主程序
        result = subprocess.run(command, capture_output=True, text=True)
        
        # 打印输出结果
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        start_page = end_page + 1

        input("Please change your IP and press Enter to continue...")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_spider.py '<Article Name>' <total_cited_number>")
        sys.exit(1)
    
    article_name = sys.argv[1]
    total_cited_number = int(sys.argv[2])
    run_spider(article_name, total_cited_number)
