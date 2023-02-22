import shutil
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchFrameException
import time
import requests
import pathlib
import sqlite3

CurrentDir = pathlib.Path(__file__).parent.absolute()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("log-level=3")
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
while True:
	try:
		driver.get("https://www.google.com/recaptcha/api2/demo")
		# click captcha box (its in a frame idk)
		driver.switch_to.frame(0)
		captcha = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".recaptcha-checkbox-border")))
		captcha.click()
		# switch back
		driver.switch_to.parent_frame()
		# go into captcha frame
		iframes = driver.find_elements(By.XPATH,"//iframe")
		driver.switch_to.frame(iframes[len(iframes) - 1])
		time.sleep(5)
		# get image
		prompt = driver.find_element(By.CSS_SELECTOR, ".rc-imageselect-desc-no-canonical")
		print("Prompt:", str(prompt.text).replace("\n"," "))
		image = driver.find_elements(By.TAG_NAME,"img")[0]
		url = image.get_attribute("src")
		grid = image.get_attribute("class").split("-")[-1]
		print(f"Grid:{grid[0]}x{grid[1]}")
		with requests.get(url,stream=True) as url:
				with open(f"{CurrentDir}/output.png", "wb") as file:
					shutil.copyfileobj(url.raw, file)
	except (TimeoutException,NoSuchElementException,NoSuchFrameException,Exception) as e:
		print(e)
		continue
# 	#Click verify button
# 	# captchaButton = driver.find_element(By.ID, "recaptcha-verify-button")
# 	# captchaButton.click()

# if __name__ == "__main__":
# 	conn = sqlite3.connect('recaptcha.db')
# 	c = conn.cursor()
# 	c.execute("SELECT prompt FROM mytable")
# 	results = c.fetchall()
# 	prompt_list = [result[0] for result in results]
# 	prompt_set = set(prompt_list)
# 	for prompt in prompt_set:
# 		print(prompt)