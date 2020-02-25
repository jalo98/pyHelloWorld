from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options, executable_path="c:/Users/javier.losada/Downloads/chromedriver/chromedriver.exe")
driver.get('http://www.pluralsight.com/')

ele = driver.find_element_by_name("q")
time.sleep(1)
ele.clear()
ele.send_keys("Pratheerth Padman")
ele.send_keys(Keys.RETURN)
time.sleep(1)

driver.quit()

