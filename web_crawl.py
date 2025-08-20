from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json

# 设置WebDriver路径
webdriver_path = 'C:/Program Files/Google/chromedriver-win64/chromedriver.exe'
# 初始化浏览器
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service)
# 读取jsonl文件得到每个网页后缀的代码
input_file_path = 'cma_yidu_disease_diagnosis_test_v2_wo_answer.jsonl'
output_file_path = 'webcrawl_class.jsonl'


def crawl_page(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # 查找所有具有'class='title'的元素
        title_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'title')))

        # 存储诊断结果
        diagnostic_results = []

        # 遍历所有标题元素，检查是否包含“诊断”这个词
        for title in title_elements:
            if "诊断" in title.text:
                # 获取标题元素的下一个兄弟元素
                sibling = title.find_element(By.XPATH, './following-sibling::*')
                if sibling:
                    diagnostic_results.append(sibling.text)

        # 如果找到了诊断结果，返回结果
        if diagnostic_results:
            return {
                'id': 0,
                'Diagnostic_results': '\n'.join(diagnostic_results)
            }
        else:
            print(f"No diagnostic results found for URL: {url}")
            return None
    except TimeoutException:
        print(f"Timeout occurred for URL: {url}")
        return None


# 读取输入文件路径和输出文件路径
with open(input_file_path, 'r', encoding='utf-8') as input_file, \
        open(output_file_path, 'w', encoding='utf-8') as output_file:
    for line in input_file:
        content = json.loads(line)
        id = content['id']
        base_url = "https://rs.yiigle.com/cmaid/"
        url = f"{base_url}{id}"
        result = crawl_page(driver, url)
        if result:
            result.update({"id": id})
            output_file.write(json.dumps(result, ensure_ascii=False) + '\n')
        else:
            print(f"Error occurred while crawling ID: {id}")