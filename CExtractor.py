from io import BytesIO
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import tkinter as tk
from PIL import Image, ImageTk

class CaptchaType:
	detect = "detect"
	hcaptcha = "hcaptcha"
	recaptcha = "recaptcha"
	cloudflare = "cloudflare"
	funcaptcha = "funcaptcha"

class CaptchaExtractorSelenium():
	def __init__(self,driver,captchaType=CaptchaType.detect,autoDisplay=True,timeout=10) -> None:
		# Check if driver is an actual selenium driver
		if not isinstance(driver,(webdriver.Chrome,webdriver.ChromiumEdge,webdriver.Edge,webdriver.Firefox,webdriver.Ie,webdriver.Safari)):
			raise TypeError("driver has to be a selenium webdriver")
		# Check if the language is set to english
		if _ := str(driver.execute_script("return navigator.language")).lower() in ["en","en,en_US","en_US"]:
			print("[WARNING] Default Browser Language is not english. Unexpected behaviour is likely to occur.")
			time.sleep(2) # give the user time to react
		self.driver = driver
		self.timeout = timeout
		self.autoDisplay = autoDisplay
		self.captcha = self.detectCaptcha() if captchaType == CaptchaType.detect else captchaType
		self.extract()

	def extract(self):
		match self.captcha:
			case CaptchaType.recaptcha:
				self.challengeElement = self.extract_reCAPTCHA()
			case CaptchaType.hcaptcha:
				# Prompt can be anything in text.
				# Grid can be 3x3
				# After Solving a solveCheck is needed to determine if its solved or not
				raise NotImplementedError("Captcha type 'hcaptcha' is not avialable yet")
			case CaptchaType.cloudflare:
				# Prompt does not exist.
				# Grid does not exist
				# After Solving a solveCheck is needed to determine if its solved or not
				raise NotImplementedError("Captcha type 'cloudflare' is not avialable yet")
			case CaptchaType.funcaptcha:
				# Prompt can be anything in text.
				# Grid is 3x2
				# After Solving a solveCheck is needed to determine if its solved or not
				raise NotImplementedError("Captcha type 'funcaptcha' is not avialable yet")
			case CaptchaType.detect:
				raise NotImplementedError("Captcha type 'detect' is not avialable yet")
			case _:
				raise NotImplementedError(f"Captcha of type {self.captcha} is unsupported")
		if self.autoDisplay:
			self.display()
			elSize = self.challengeElement.size
			ac = ActionChains(self.driver)
			for click in self.clicks:
				ac.move_to_element_with_offset(self.challengeElement,int(click[1][0] - (elSize["width"] / 2)),int(click[1][1] - (elSize["height"] / 2)))
				ac.click()
			ac.perform()
			input()
				
	def display(self):
		self.clicks = []
		def draw_circle(event):
			x, y = event.x, event.y
			radius = 15  # Adjust the circle radius as needed
			click = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red", outline="black")  # Draw a small red circle
			self.clicks.append((click,(x,y)))
		def clear_clicks():
			for click in self.clicks:
				canvas.delete(click[0])
			self.clicks = []
		# Create a tkinter window
		root = tk.Tk()
		root.title(f"CExtractor | {self.driver.current_url} | {self.captcha}")
		# Convert the BytesIO object to a PIL image
		element_image = Image.open(BytesIO(self.challengeElement.screenshot_as_png))
		# Adjust window size
		root.geometry(f"{element_image.size[0]}x{element_image.size[1] + int(element_image.size[0] / 10)}")
		root.resizable(width=False,height=False)
		# Create a Tkinter PhotoImage object from the PIL image
		photo = ImageTk.PhotoImage(element_image)
		# Create a canvas to display the image
		canvas = tk.Canvas(root, width=element_image.size[0], height=element_image.size[1])
		canvas.pack()
		# Display the image on the canvas
		canvas.create_image(0, 0, anchor=tk.NW, image=photo)
		# Click event listener
		canvas.bind("<Button-1>", draw_circle)
		frame = tk.Frame(root)
		reset_button = tk.Button(frame, command=clear_clicks, text="Reset Clicks", width=int(element_image.size[0] / 25))
		submit_button = tk.Button(frame, command=lambda: root.destroy(), text="Submit Clicks", width=int(element_image.size[0] / 25))
		reset_button.grid(row=0,column=0)
		submit_button.grid(row=0,column=1)
		frame.pack()
		# Run the Tkinter main loop
		root.mainloop()

	def extract_reCAPTCHA(self):
		WebDriverWait(self.driver, self.timeout).until(lambda driver: len([iframe for iframe in self.driver.find_elements(By.XPATH,"//iframe") if "recaptcha" in str(iframe.accessible_name).lower()]) > 0)
		iframeCount = len([iframe for iframe in self.driver.find_elements(By.XPATH,"//iframe")])
		clickThis = [iframe for iframe in self.driver.find_elements(By.XPATH,"//iframe") if "recaptcha" in str(iframe.accessible_name).lower()][0]
		time.sleep(2)
		clickThis.click()
		time.sleep(2)
		challengeFrame = [iframe for iframe in driver.find_elements(By.XPATH,"//iframe") if "challenge" in str(iframe.accessible_name).lower()][0]
		return challengeFrame

if __name__ == "__main__":
		from selenium import webdriver
		from selenium.webdriver.chrome.options import Options
		from selenium.webdriver.chrome.service import Service
		from webdriver_manager.chrome import ChromeDriverManager
		chrome_options = Options()
		# chrome_options.add_argument("--headless")
		chrome_options.add_argument("log-level=3")
		chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
		driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
		driver.get("https://www.google.com/recaptcha/api2/demo")
		Test = CaptchaExtractorSelenium(driver,captchaType=CaptchaType.recaptcha)
		# time.sleep(1)
		# driver.get("https://www.nulled.to/index.php?app=core&module=global&section=register")
		# Test = CaptchaExtractorSelenium(driver,captchaType=CaptchaType.recaptcha)
		# time.sleep(1)
		# driver.get("https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox-explicit.php")
		# Test = CaptchaExtractorSelenium(driver,captchaType=CaptchaType.recaptcha)
		# time.sleep(1)
		# driver.get("https://forums.lenovo.com/login")
		# Test = CaptchaExtractorSelenium(driver,captchaType=CaptchaType.recaptcha)
		# time.sleep(1)
		# driver.get("https://linustechtips.com/register")
		# Test = CaptchaExtractorSelenium(driver,captchaType=CaptchaType.recaptcha)
		# time.sleep(1)





# import shutil
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchFrameException
# import requests
# import random
# import pathlib

# CurrentDir = pathlib.Path(__file__).parent.absolute()

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("log-level=3")
# chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
# driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
# while True:
# 	driver.get("https://www.google.com/recaptcha/api2/demo")
# 	# driver.get("https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox-explicit.php")
# 	# driver.get("https://www.nulled.to/index.php?app=core&module=global&section=register")
# 	# click captcha box (its in a frame idk)
# 	driver.switch_to.frame(0)
# 	try:
# 		captcha = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".recaptcha-checkbox-border")))
# 	except TimeoutException:
# 		input("ITS THE CAPTCHA BUTTON")
# 	captcha.click()
# 	# switch back
# 	driver.switch_to.parent_frame()
# 	# go into captcha frame
# 	iframes = driver.find_elements(By.XPATH,"//iframe")
# 	# for iframe in iframes:
# 	# 	print(iframe.accessible_name)
# 	print(f"iframe name:{iframes[len(iframes) - 1].accessible_name}")
# 	driver.switch_to.frame(iframes[len(iframes) - 1]) # instead switch to the iframe with reCAPTCHA as .accessible_name
# 	# get image
# 	try:
# 		prompt = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".rc-imageselect-desc-no-canonical")))
# 	except TimeoutException:
# 		try:
# 			prompt = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".rc-imageselect-desc")))
# 		except TimeoutException:
# 			input("wtf")
# 	print("Prompt:", str(prompt.text).replace("\n"," "))
# 	# if "once there are none left" in prompt.text:
# 	# 	input("THIS SHOULD BE AN ANNOYING ONE (Images fade out and new ones appear)")
# 	try:
# 		image = driver.find_elements(By.TAG_NAME,"img")[0]
# 		url = image.get_attribute("src")
# 	except Exception as e:
# 		input(f"IMAGE ({e})")
# 	try:
# 		grid = image.get_attribute("class").split("-")[-1]
# 	except Exception as e:
# 		input(f"GRID ({e})")
# 	print(f"Grid:{grid[0]}x{grid[1]}")
# 	with requests.get(url,stream=True) as url:
# 			with open(f"{CurrentDir}/{random.randint(0,55555)}output.png", "wb") as file:
# 				shutil.copyfileobj(url.raw, file)
# 	# except (TimeoutException,NoSuchElementException,NoSuchFrameException,Exception) as e:
# 	# 	print("##########################")

