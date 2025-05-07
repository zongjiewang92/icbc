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


TM = time.strftime("%Y%m%d-%H%M%S")
# 创建截图目录
SCREENSHOT_DIR_ERROR = os.path.join("screenshots_error", TM)
os.makedirs(SCREENSHOT_DIR_ERROR, exist_ok=True)

# 创建截图目录
SCREENSHOT_DIR_Q = os.path.join("screenshots_question", TM)
os.makedirs(SCREENSHOT_DIR_Q, exist_ok=True)

def take_screenshot(driver, name="screenshot", path_falg=1):
    pass

    # try:
    #     if path_falg==1:
    #         SCREENSHOT_DIR = SCREENSHOT_DIR_ERROR
    #     else:
    #         SCREENSHOT_DIR = SCREENSHOT_DIR_Q
    #     """截图并保存"""
    #     timestamp = time.strftime("%Y%m%d-%H%M%S")
    #     filename = os.path.join(SCREENSHOT_DIR, f"{name}_{timestamp}.png")
    #     driver.save_screenshot(filename)
    #     print(f"📸 截图已保存: {filename}")
    # except Exception as screenshot_error:
    #     print(f"❌ 截图失败: {screenshot_error}")
