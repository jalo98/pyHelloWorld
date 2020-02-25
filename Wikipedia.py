from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from bs4 import BeautifulSoup

file = open("busqueda.txt", "r")


def searchInPage(driver, searchWord):
    # players_ele = driver.find_element_by_link_text("Players").click()

    print("debug: Page loaded")

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "searchInput")))

    print("debug: Element search clickable")

    search_ele = driver.find_element_by_id("searchInput")

    print("debug: Element search by id")

    search_ele.send_keys(searchWord)

    print("debug: Send word to be search")

    time.sleep(2)
    # driver.find_element_by_css_selector("div[class*='searchIconContainer searchCommit']").click()
    driver.find_element_by_class_name("searchButton").click()

    print("debug: Search Button clicked")

    driver.implicitly_wait(5)
    # click_wayne = driver.find_element_by_xpath(
    #     "//img[@data-player='p13017']").click()

    # page_source_overview = driver.page_source

    # soup = BeautifulSoup(page_source_overview, 'lxml')

    # title_finder = soup.find_all('spam', class_='title')

    # print(10*"-" + "These are the latest news headlines about Wayne Rooney" + 10*"-" + "\n")
    # for title in title_finder:
    #     print(title.string)

    # time.sleep(1)
    # wayne_stats = driver.find_element_by_xpath("//a[@href='stats']").click()

    print("debug: Search result")

    time.sleep(5)
    driver.implicitly_wait(5)

    print("debug: Analysing the Header of the page")

    firstHeading = driver.find_element_by_id("firstHeading")

    firstHeadingElement = BeautifulSoup(firstHeading.page_source, "lxml")

    print(firstHeadingElement)
    print("Header of the page " + firstHeadingElement.getText)

    if (firstHeading.string != "Search results"):

        page_source_stats = driver.page_source

        soup = BeautifulSoup(page_source_stats, "lxml")

        # stat_finder = soup.find_all("span", class_="nowrap")

        # print(stat_finder)

        # print(10*"-" + "Bill Clinton Stats" + 10*"-" + "\n")
        # for stat in stat_finder:
        #     # print(stat["data-stat"] + " - " + stat.string)
        #     print(stat.string)

        # tables information

        print("debug: finging tables")

        table = soup.find("table", class_="infobox vcard")
        table_body = table.find("tbody")

        rows = table_body.find_all("tr")

        print("debug: rows found")

        for row in rows:
            cols = row.find_all(["th", "td"])
            cols = [ele.text.strip() for ele in cols]
            line = ""
            for col in cols:
                line += col + " "
            print(line)

        # for article in articles:
        #     print(type(article), articles.string)
        #     break
        # print(articles)
    else:
        print("We did not find the page we were looking for")


try:
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    # options.add_argument("--headless")
    # options.add_argument("--kiosk")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(
        options=options, executable_path="c:/Users/javier.losada/Downloads/chromedriver/chromedriver.exe")
    driver.get('https://en.wikipedia.org/')

    # players_ele = driver.find_element_by_link_text("Players").click()

    # for line in file:
    #     print(line)
    searchInPage(driver, "Bill Clinton")

    # for article in articles:
    #     print(type(article), articles.string)
    #     break
    # print(articles)
except Exception as ex:
    print("There has been an error!!:", ex)

finally:
    driver.quit()
