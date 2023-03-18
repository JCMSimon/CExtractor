import shutil
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchFrameException
import requests
import random
import pathlib

CurrentDir = pathlib.Path(__file__).parent.absolute()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("log-level=3")
chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
while True:
	driver.get("https://www.google.com/recaptcha/api2/demo")
	# driver.get("https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox-explicit.php")
	# driver.get("https://www.nulled.to/index.php?app=core&module=global&section=register")
	# click captcha box (its in a frame idk)
	driver.switch_to.frame(0)
	try:
		captcha = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".recaptcha-checkbox-border")))
	except TimeoutException:
		input("ITS THE CAPTCHA BUTTON")
	captcha.click()
	# switch back
	driver.switch_to.parent_frame()
	# go into captcha frame
	iframes = driver.find_elements(By.XPATH,"//iframe")
	# for iframe in iframes:
	# 	print(iframe.accessible_name)
	print(f"iframe name:{iframes[len(iframes) - 1].accessible_name}")
	driver.switch_to.frame(iframes[len(iframes) - 1]) # instead switch to the iframe with reCAPTCHA as .accessible_name
	# get image
	try:
		prompt = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".rc-imageselect-desc-no-canonical")))
	except TimeoutException:
		try:
			prompt = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".rc-imageselect-desc")))
		except TimeoutException:
			input("wtf")
	print("Prompt:", str(prompt.text).replace("\n"," "))
	# if "once there are none left" in prompt.text:
	# 	input("THIS SHOULD BE AN ANNOYING ONE (Images fade out and new ones appear)")
	try:
		image = driver.find_elements(By.TAG_NAME,"img")[0]
		url = image.get_attribute("src")
	except Exception as e:
		input(f"IMAGE ({e})")
	try:
		grid = image.get_attribute("class").split("-")[-1]
	except Exception as e:
		input(f"GRID ({e})")
	print(f"Grid:{grid[0]}x{grid[1]}")
	with requests.get(url,stream=True) as url:
			with open(f"{CurrentDir}/{random.randint(0,55555)}output.png", "wb") as file:
				shutil.copyfileobj(url.raw, file)
	# except (TimeoutException,NoSuchElementException,NoSuchFrameException,Exception) as e:
	# 	print("##########################")

