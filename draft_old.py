import requests
from selenium import webdriver
import time
import csv
import json

from bs4 import BeautifulSoup


def divWithClass(tag):
    return tag is not None and "the-post-content-meta" in tag.split()


def getArticle(source_page_xml_param):
    techeblog_page = BeautifulSoup(source_page_xml_param, "lxml")

    strippingPattern = "\n\t"

    article = techeblog_page.find("article")

    # print(articles[0].find_element_by_class_name("post-meta post-meta-b"))

    pages = []
    # print("Title:", article.h2.text.strip(strippingPattern))
    # print("Link:", article.a["href"])
    # print("Img:", article.img["src"])
    images = [img["src"] for img in article.find_all("img")
              if img.get("src") and img.get("alt") and not img.get("class")]
    videos = [iframe["src"] for iframe in article.find_all("iframe")
              if iframe.get("src") and iframe.get("allow")]
    texts = [p.text.strip(strippingPattern) for p in article.find_all(
        "p") if p.br is not None and p.text.strip(strippingPattern) != ""]
    blockquote = [blockquote.text.strip(strippingPattern) for blockquote in article.find_all("blockquote")
                  if blockquote.p is not None and blockquote.text.strip(strippingPattern) != ""]
    # if article.iframe is not None:
    #     # print("Video:", article.iframe["src"])
    #     videos.append(article.iframe["src"])
    # print("Text:", article.p.text.strip(strippingPattern))
    print("Texts length:", len(texts))
    print("Images length:", len(images))
    print("Videos length:", len(videos))
    print("Blockquote length:", len(blockquote))
    page = {"title": article.h1.text.strip(strippingPattern).replace("'", "'"), "link": article.a["href"],
            "img": images, "video": videos, "text": texts, "blockquote": blockquote}

    print(page)

    return page


def getArticles(source_page_xml_param):
    techeblog_page = BeautifulSoup(source_page_xml_param, "lxml")

    strippingPattern = "\n\t"

    articles = techeblog_page.find_all("article")

    # print(articles[0].find_element_by_class_name("post-meta post-meta-b"))

    pages = []
    for article in articles:
        page = {"title": article.h2.text.strip(strippingPattern).replace(
            "'", "'"), "link": article.a["href"]}

        print(page)

        pages.append(page)

    # print(pages)
    return pages


def writeToCSV(pages, depth, fieldnames, mode='w'):
    with open('pages-scrapped-' + depth + '.csv', mode, newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # writer.writerow(["title", "link", "img", "video", "text"])
        writer.writeheader()
        for page in pages:
            writer.writerow(page)


def writeToJson(pages, depth, mode='w'):
    with open('pages-scrapped-' + depth + '.json', mode, encoding='utf-8') as file:
        json.dump(pages, file, indent=4, ensure_ascii=False)


options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
options.add_argument("--headless")
options.add_argument("--kiosk")
options.add_argument("--disable-popup-blocking")

# with webdriver.Chrome(
#         options=options, executable_path="c:/Users/javier.losada/Downloads/chromedriver/chromedriver.exe") as driver:
try:

    print("Starting the application!!!!")
    start = time.time()

    driver = webdriver.Chrome(
        options=options, executable_path="c:/Users/javier.losada/Downloads/chromedriver/chromedriver.exe")
    driver.get('http://www.techeblog.com/')

    # /html/body/div[1]/div[2]/div/div/div/div/article[2]/header/div[2]/h2/a
    # //*[@id="post-80279"]/header/div[2]/h2
    # //*[@id="post-80279"]/header/div[2]/h2/a

    source_page_xml = driver.page_source

    outer_pages = getArticles(source_page_xml)

    inner_pages = []

    for page_count, outer_page in enumerate(outer_pages, start=1):
        print("Inner Page processed:", page_count)
        print("Inner page title:", outer_page["title"])
        driver.get(outer_page["link"])

        post_source = driver.page_source

        post_page = BeautifulSoup(post_source, "lxml")

        # time.sleep(5)

        inner_pages.append(getArticle(post_source))

    end = time.time()

    writeToCSV(outer_pages, "outer", ["title", "link"], "w")
    writeToCSV(inner_pages, "inner", [
               "title", "link", "img", "video", "text", "blockquote"], "w")

    writeToJson(inner_pages, "inner", "w")

    print("Time Taken: {:.6f}s".format(end - start))
    print("Scrapping has finished!!!!!")

except Exception as ex:
    print("There has been an error!!:", ex)
    print("Exception instance:", type(ex))
    print("Exception args:", type(ex.args))
finally:
    if driver is not None:
        driver.close()
