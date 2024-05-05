from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver. common. keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# 下載圖片時使用
import os
import wget
import pyautogui
from dotenv import load_dotenv, dotenv_values
import os
load_dotenv()

ig_account = os.getenv("IG_ACCOUNT")
ig_password = os.getenv("IG_PASSWORD")

options = webdriver.ChromeOptions()
#驱动过程结束后保持浏览器的打开状态
options.add_experimental_option("detach", True)
options.add_argument("--disable-notifications")
# mobile_emulation = {"deviceName":"Nexus 5"}
# options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(options=options)

def main():
  print("=" * 100)
  driver.get('https://www.instagram.com/')

  # 等待 name 為 username 的 input 顯示，並把標籤存放在 username 變數
  username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@name="username"]'))
  )

  # 等待 name 為 password 的 input 顯示，並把標籤存放在 password 變數
  password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@name="password"]'))
  )
  login = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
  # 使用前把它清空
  username.clear()
  password.clear()

  # 輸入 username 和 password 的值
  username.send_keys(ig_account)
  password.send_keys(ig_password)

  # 點擊 login 按鈕
  login.click()

  pre_post_btn = WebDriverWait(driver, 10).until(
    # 注意：此處用 svg 的aria-label 來找出點擊實體
    EC.presence_of_element_located((By.CSS_SELECTOR,'svg[aria-label="New post"]'))
  )
  pre_post_btn.click()

  post_btn = WebDriverWait(driver, 10).until(
    # 注意：此處用 svg 的aria-label 來找出點擊實體
    EC.presence_of_element_located((By.XPATH, f'//span[text()="Post"]'))
  )
  post_btn.click()

  select_photo = WebDriverWait(driver, 10).until(
    # 注意：此處用 svg 的aria-label 來找出點擊實體
    EC.presence_of_element_located((By.XPATH, f'//button[text()="Select from computer"]'))
  )
  select_photo.click()
  # Ctrl + Shift + G 直接輸入路徑
  pyautogui.hotkey('command', 'shift', 'G')
  time.sleep(5)

  # Photo path
  photo_path = "/Users/steven/Downloads/summertech-4.jpg"
  for word in photo_path:
    pyautogui.PAUSE=0.1
    pyautogui.typewrite(word)

  time.sleep(1)
  pyautogui.press('enter')
  time.sleep(1)
  pyautogui.press('enter')
  time.sleep(1)
  next_btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, f'//div[text()="Next"]'))
  )
  next_btn.click()
 
  next_btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, f'//div[text()="Next"]'))
  )
  next_btn.click()

  content = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Write a caption..."]'))
  )
  content.click()

  # Post content(用 \n 換行)
  content.send_keys("- \n hello world \n This is Steven.")

  share_btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, f'//div[text()="Share"]'))
  )
  share_btn.click()
  time.sleep(10)
  driver.quit()

if __name__ == "__main__":
  main()