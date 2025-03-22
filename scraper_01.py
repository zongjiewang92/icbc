import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException

IMAGE_NOT_DOWNLOAD = "https://images.ctfassets.net/1eftmbczj7w9/4lxJsZKPeDdqvWh9imZdNL/ac51d64ed9eab0cb6075423af8f2cc44/VPLOGO.jpg"
IMAGES_DIR = "images_download"
os.makedirs(IMAGES_DIR, exist_ok=True)

def init_driver(retries=3, delay=5):
    """ 初始化 WebDriver，确保失败时重试 """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-background-networking")
    
    for attempt in range(retries):
        try:
            # 启动 WebDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            return driver   # 如果成功，返回 driver 实例
        except WebDriverException as e:
            print(f"🚨 WebDriver 初始化失败，尝试重试 ({attempt + 1}/{retries})... 错误: {e}")
            time.sleep(delay)
    raise Exception("❌ WebDriver 初始化失败，已尝试多次。")


# **抓取 ICBC 题目**
def scrape_questions(step3, max_questions=25):
    """ 抓取 ICBC 练习题目 """
    driver = None
    try:
        driver = init_driver()
        wait = WebDriverWait(driver, 5)  # 降低等待时间
        question_data = []
        
        driver.get("https://practicetest.icbc.com/")
        time.sleep(2)
        
        # **Step 1: 选择“简体中文”**
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), '简体中文')]"))).click()
            driver.find_element(By.XPATH, "//button[contains(text(), '确认')]").click()
            time.sleep(1)
        except TimeoutException:
            print("❌ Step1: 语言选择超时，跳过")
            return
        
        # **Step 2: 点击 "笔试练习"**
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '笔试练习')]"))).click()
            time.sleep(1)
        except TimeoutException:
            print("❌ Step2: 进入笔试练习超时")
            return
        
        # **Step 3: 选择测试模式**
        step3_xpath = "//button[contains(text(), '完整测试')]" if step3 else "//button[contains(text(), '标志测试')]"

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, step3_xpath))).click()
            time.sleep(2)
        except TimeoutException:
            print("❌ Step3: 进入测试失败")
            return
        
        # **Step 4: 开始抓取题目**
        for _ in range(max_questions):
            try:
                question_text = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//p[contains(@class, 'mb-2') and contains(@class, 'font-headings')]"))
                ).text
                print(f"📌 题目: {question_text}")

                # **获取图片**
                image_url = ""
                try:
                    img_elem = driver.find_element(By.CSS_SELECTOR, "img.max-w-60")
                    image_url = img_elem.get_attribute("src")
                    if image_url == IMAGE_NOT_DOWNLOAD or not image_url.startswith("http"):
                        image_url = ""
                    else:
                        img_path = os.path.join(IMAGES_DIR, os.path.basename(image_url).split("?")[0])
                        with open(img_path, "wb") as f:
                            f.write(requests.get(image_url).content)
                        image_url = img_path
                except Exception:
                    image_url = ""

                # **获取选项**
                options_data = []
                option_buttons = driver.find_elements(By.TAG_NAME, "button")
                for button in option_buttons:
                    divs = button.find_elements(By.TAG_NAME, "div")
                    if len(divs) >= 3:
                        options_data.append({"letter": divs[1].text.strip(), "text": divs[2].text.strip()})

                # **点击 A 选项**
                for btn in option_buttons:
                    if btn.text.startswith("A"):
                        btn.click()
                        break

                # **提交答案**
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].bg-purple"))).click()
                except TimeoutException:
                    print("❌ 提交失败，跳过此题")
                    continue

                time.sleep(0.5)

                # **获取正确答案**
                try:
                    driver.find_element(By.XPATH, "//button[@value='A']//img[contains(@src, 'icon-checkmark.svg')]")
                    correct_answer = "A"
                except:
                    correct_answer = driver.find_element(
                        By.XPATH, "//button[contains(@class, 'border-[#3adda2]')]//div[contains(@class, 'h-7')]"
                    ).text.strip()

                print(f"✅ 正确答案: {correct_answer}")

                # **存储数据**
                question_data.append({
                    "question": question_text,
                    "options": options_data,
                    "image": image_url,
                    "correct_answer": correct_answer
                })

                # **进入下一个问题**
                try:
                    next_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '下一个问题')]"))
                    )
                    next_button.click()
                except TimeoutException:
                    print("✅ 测试结束")
                    break

                time.sleep(0.5)

            except Exception as e:
                print("❌ 题目抓取失败:", e)
                break

        return question_data

    finally:
        if driver:
            driver.quit()
            print("✅ WebDriver 关闭成功")

