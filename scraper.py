# scraper.py
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
from selenium.common.exceptions import WebDriverException
# from screenshot import take_screenshot


IMAGE_NOT_DOWNLOAD = "https://images.ctfassets.net/1eftmbczj7w9/4lxJsZKPeDdqvWh9imZdNL/ac51d64ed9eab0cb6075423af8f2cc44/VPLOGO.jpg"
IMAGES_DIR = "images_download"
os.makedirs(IMAGES_DIR, exist_ok=True)


# 初始化 WebDriver
def init_driver(retries=3, delay=5):
    options = Options()
    # options.add_argument("--headless")  # 无头模式
    options.add_argument("--disable-gpu")  # 禁用 GPU 加速
    options.add_argument("--no-sandbox")  # 避免沙盒模式问题
    options.add_argument("--disable-dev-shm-usage")  # 避免 `/dev/shm` 内存不足
    options.add_argument("--disable-extensions")  # 禁用扩展
    options.add_argument("--disable-infobars")  # 禁用自动化提示
    options.add_argument("--disable-blink-features=AutomationControlled")  # 伪装成真实用户
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-javascript")
    options.add_argument("--start-maximized")
    options.add_argument("--js-flags=--max-old-space-size=512")

    driver = None
    service = None

    for attempt in range(retries):
        try:
            
            # service = Service(ChromeDriverManager(version="123.0.6312.59").install())
            service = Service(ChromeDriverManager().install())  # 启动 service
            driver = webdriver.Chrome(service=service, options=options)  # 初始化 driver
            driver.set_window_size(1920, 1080)
            # driver.set_window_size(2560, 1440)
            driver.set_page_load_timeout(15)
            driver.set_script_timeout(15)
            return driver, service  # 成功时返回 driver 实例
        except WebDriverException as e:
            driver = None
            service = None
            print(f"🚨 WebDriver 初始化失败，尝试重试 ({attempt + 1}/{retries})... 错误: {e}")
            time.sleep(delay)
    raise Exception("❌ WebDriver 初始化失败，已尝试多次。")

def release_driver(driver, service):
    try:
        if driver:
            driver.quit()
            driver = None
            print(f"✅ Driver quit")
    except Exception as quit_error:
        print(f"❌ Driver quit 失败: {quit_error}")
    try:
        if service:
            service.stop()
            service = None
            print(f"✅ Service close")
    except Exception as quit_error:
        print(f"❌ Service close 失败: {quit_error}")



# **抓取 ICBC 题目**
def scrape_questions(step3, question_set, max_questions=25):
    # 使用示例
    try:
        driver, service = init_driver()
        print("✅ WebDriver 启动成功！")
    except Exception as e:
        print(e)
        return

    wait = WebDriverWait(driver, 10)
    question_data = []  # 存储所有题目

    # **访问 ICBC 练习考试页面**
    url = "https://practicetest.icbc.com/"
    driver.get(url)
    time.sleep(2)
        
    # **Step 1: 选择“简体中文”并确认**
    try:
        simplified_chinese = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), '简体中文')]"))
        )
        simplified_chinese.click()
        print("✅ Step1.1:语言已选择：简体中文")
        time.sleep(1)
    except Exception as e:
        print("❌ Step1.1:语言选择失败:", e)
        # take_screenshot(driver, "step1_error")  # 发生异常时截图
        release_driver(driver, service)
        return question_data
    
    try:
        confirm_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '确认')]"))
            )
        confirm_button.click()
        print("✅ Step1.2:语言已选择：简体中文; 并点击 确认")
        time.sleep(1)  # 进入下一个页面
    except Exception as e:
        print("❌ Step1.2:语言已选择：简体中文; 点击 确认 失败", e)
        # take_screenshot(driver, "step1_error")  # 发生异常时截图
        release_driver(driver, service)
        return question_data

    # **Step 2: 点击 "笔试练习"**
    try:
        practice_test_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '笔试练习')]"))
        )
        practice_test_button.click()
        print("✅ Step2:进入页面2：笔试练习")
        time.sleep(1)
    except Exception as e:
        print("❌ Step2:进入笔试练习失败:", e)
        # take_screenshot(driver, "step2_error")  # 发生异常时截图
        release_driver(driver, service)
        return question_data

    # **Step 3: 点击 "完整测试"**
    if step3:
        try:
            full_test_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '完整测试')]"))
            )
            full_test_button.click()
            print("✅ Step3:进入页面3：完整测试")
            time.sleep(1)
        except Exception as e:
            print("❌ Step3:进入完整测试失败:", e)
            # take_screenshot(driver, "step3_error")  # 发生异常时截图
            release_driver(driver, service)
            return question_data
    else:
        try:
            full_test_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '标志测试')]"))
            )
            full_test_button.click()
            print("✅ Step3:进入页面3：标志测试")
            time.sleep(1)
        except Exception as e:
            print("❌ Step3:进入标志测试失败:", e)
            # take_screenshot(driver, "step3_error")  # 发生异常时截图
            release_driver(driver, service)
            return question_data

    time.sleep(1)

    # **Step 4: 开始抓取测试题**
    question_data = []  # 存储所有题目信息

    for _ in range(max_questions):

        now_question = None

        question_text = ""
        try:
            # **抓取题目文本**
            question_text = wait.until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'mb-2') and contains(@class, 'font-headings') and contains(@class, 'text-[18px]') and contains(@class, 'font-bold')]"))
            ).text
            print(f"✅ 题目: {question_text}")
        except:
            print(f"❌ 题目 抓取失敗: {question_text}")
            break

        if not question_text:
            print(f"❌ 题目 抓取失敗 跳出: {question_text}")
            break


        # **抓取图片**
        image_url = ""
        try:
            # 定位图片
            image_element = driver.find_element(By.CSS_SELECTOR, "img.max-w-60")  # 使用 class 精准定位
            image_url = image_element.get_attribute("src")

            if IMAGE_NOT_DOWNLOAD == image_url:
                image_url = ""
                print("⚠️ 图片 不下载")
            else:
                # 确保 URL 有效
                if image_url.startswith("http") :
                    image_filename = os.path.basename(image_url).split("?")[0]  # 去掉 URL 参数，获取文件名
                    image_download_filename = os.path.join(IMAGES_DIR, image_filename)
                    img_data = requests.get(image_url).content

                    # 保存图片
                    with open(image_download_filename, "wb") as f:
                        f.write(img_data)
                    print(f"✅ 图片已下载: {image_download_filename}")
                    image_url = image_download_filename
                else:
                    image_url = ""
                    print("⚠️ 图片 URL 无效")
        except Exception as e:
            image_url = ""
            print(f"❌ 该题目无图片, 或者图片加载失败: {e}")
            # take_screenshot(driver, "image_error")  # 发生异常时截图
            break


        # **抓取选项**
        options_data = []
        try:
            option_buttons = driver.find_elements(By.TAG_NAME, "button")  # 找到所有按钮
            for button in option_buttons:
                divs = button.find_elements(By.TAG_NAME, "div")  # 找到按钮下所有 div
                
                if len(divs) >= 3:  # 确保有足够的 div
                    option_letter = divs[1].text.strip()  # 选项字母（位于第二个 div）
                    option_text = divs[2].text.strip()  # 选项内容（位于第三个 div）
                    options_data.append({"letter": option_letter, "text": option_text})

            for button in option_buttons:
                divs = button.find_elements(By.TAG_NAME, "div")  # 找到按钮下所有 div
                
                if len(divs) >= 3:  # 确保有足够的 div
                    option_letter = divs[1].text.strip()  # 选项字母（位于第二个 div）
                    if option_letter.startswith("A"):
                        time.sleep(0.1)
                        button.click()
                        button.click()
                        print("✅ 选择 A")
                        break

                    
            print(f"✅ 选项: {options_data}")

            # **点击 A 选项**
            # for button in option_buttons:
                    # break
                

        except:
            print(f"❌ 选项 抓取失敗: {options_data}")
            break
        if not options_data:
            print(f"❌ 选项 抓取失敗 跳出: {options_data}")
            break

        
        try:
            # **点击 "提交答案"**
            submit_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].bg-purple"))
            )
            submit_button.click()
            print("✅ 点击 提交答案")
            time.sleep(1)  
        except:
            print(f"❌ 点击 提交答案 失敗")
            break

        
        try:
            now_question = question_text + "_" + image_url
            if now_question in question_set:
                print(f"✅ 题目已经存在，不抓取答案， 跳过题目：{now_question}")
            else:
                print(f"✅ 题目不存在，取答案")
                # take_screenshot(driver, "question", 2)
                # **获取正确答案**
                try:
                    # **查找 "正确" 标志，判断 A 是否正确**
                    driver.find_element(By.XPATH, "//button[@value='A']//img[contains(@src, 'icon-checkmark.svg')]")
                    correct_answer = "A"
                except:
                    try:
                        # **如果 A 错误，查找正确答案的选项字母**
                        correct_answer = driver.find_element(By.XPATH, "//button[contains(@class, 'border-[#3adda2]')]//div[contains(@class, 'h-7') and contains(@class, 'w-7')]").text.strip()
                    except Exception as e:
                        print("❌ A 错误，同时没找到正确答案:", e)
                        # take_screenshot(driver, "question_error")  # 发生异常时截图
                        break

                print(f"✅ 正确答案: {correct_answer}")

                question = {
                    "question": question_text,
                    "options": options_data,
                    "image": image_url,
                    "correct_answer": correct_answer
                }

                print(f"✅ 抓取到的題目: \n{question}")
                # **存储题目、图片、答案**
                question_data.append(question)

        except:
            print(f"❌ 抓取正確答案以及保存完整題目 失敗")
            break


        # **点击 "下一个问题"**
        try:
            next_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '下一个问题')]"))
            )
            next_button.click()
            time.sleep(1)
            print(f"✅ 下一个问题 ===============================")
        except:
            print("✅ 测试结束，无 '下一个问题' 按钮***************************")
            break

            # try:
            #     print("✅ 测试结束，无 '下一个问题' 按钮")
                

            #     release_driver(driver, service)



            #     # 尝试查找 "完成" 按钮

            #     buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '完成')]")
            #     if buttons:
            #         buttons[0].click()
            #         print("✅ 点击 完成")
            #     else:
            #         print("❌ 没有找到 完成 按钮")
            #     break


            #     # buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '完成')]")
            #     # if buttons:
            #     #     buttons[0].click()  # 找到按钮则点击
            #     #     time.sleep(1)
            #     #     print(f"✅ 点击 完成")
            #     # break
            # except Exception as e:
            #     print(f"❌ 没有找到  完成 按钮:", e)
            #     release_driver(driver, service)
            #     # screenshot_name = "question_next_error"
            #     # if now_question:
            #     #     screenshot_name = now_question
            #     # take_screenshot(driver, screenshot_name)
            #     break

    
    wait = None
    release_driver(driver, service)

    # print(f"✅ 问题内容: {question_data}")
    return question_data  # 返回抓取的数据




