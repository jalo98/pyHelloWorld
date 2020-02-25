from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
# options.add_argument("--headless")
# options.add_argument("--kiosk")
options.add_argument("--disable-popup-blocking")

driver = webdriver.Chrome(
    options=options, executable_path="c:/Users/javier.losada/Downloads/chromedriver/chromedriver.exe")
driver.get('https://www.techeblog.com/')

# /html/body/div[1]/div[2]/div/div/div/div/article[2]/header/div[2]/h2/a
# //*[@id="post-80279"]/header/div[2]/h2
# //*[@id="post-80279"]/header/div[2]/h2/a

source_page_xml = driver.page_source

techeblog_page = BeautifulSoup(source_page_xml, "lxml")

articles = techeblog_page.find_all("article")

# print(articles[0].find_element_by_class_name("post-meta post-meta-b"))

pages = []
for article in articles:
    print("Title:", article.h2.text)
    print("Link:", article.a["href"])
    print("Img:", article.img["src"])
    print("Text:", article.p.text)

    page = {}
    page["title"] = article.h2.text
    page["link"] = article.a["href"]
    page["Img:"] = article.img["src"]
    page["Text:"] = article.p.text

    pages.append(page)

    print(page)

print(pages)


driver.get(pages[0]["link"])
