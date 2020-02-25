from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from bs4 import BeautifulSoup

try:
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    # options.add_argument("--headless")
    options.add_argument("--kiosk")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(
        options=options, executable_path="c:/Users/javier.losada/Downloads/chromedriver/chromedriver.exe")
    driver.get('https://www.premierleague.com/')

    players_ele = driver.find_element_by_link_text("Players").click()

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "search-input")))

    search_ele = driver.find_element_by_id("search-input")
    search_ele.send_keys("Wayne Rooney")
    # time.sleep(1)
    # driver.find_element_by_css_selector("div[class*='searchIconContainer searchCommit']").click()
    driver.find_element_by_class_name("searchIconContainer").click()

    driver.implicitly_wait(2)
    click_wayne = driver.find_element_by_xpath(
        "//img[@data-player='p13017']").click()

    page_source_overview = driver.page_source

    soup = BeautifulSoup(page_source_overview, 'lxml')

    title_finder = soup.find_all('spam', class_='title')

    print(10*"-" + "These are the latest news headlines about Wayne Rooney" + 10*"-" + "\n")
    for title in title_finder:
        print(title.string)

    time.sleep(1)
    wayne_stats = driver.find_element_by_xpath("//a[@href='stats']").click()

    page_source_stats = driver.page_source

    soup = BeautifulSoup(page_source_stats, "lxml")

    stat_finder = soup.find_all("span", class_="allStatContainer")

    print(stat_finder)

    print(10*"-" + "Wayne Rooney Stats" + 10*"-" + "\n")
    for stat in stat_finder:
        print(stat["data-stat"] + " - " + stat.string)

    # for article in articles:
    #     print(type(article), articles.string)
    #     break
    # print(articles)
except Exception as ex:
    print("There has been an error!!:", ex)

finally:
    driver.quit()
