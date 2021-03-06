import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from dateutil.parser import parse
from selenium import webdriver
import time
import csv
import json

from bs4 import BeautifulSoup

CHROMEDRIVER_EXE = "c:/Users/javier.losada/Downloads/chromedriver/chromedriver.exe"
CONCURRENCY_SIMPLE = True
CONCURRENCY_MULTIPLE = not CONCURRENCY_SIMPLE


def get_concurrency_method(concurrency_flag):
    if concurrency_flag == CONCURRENCY_SIMPLE:
        return "Simple Concurrency"
    else:
        return "Multiple Concurrency"


def parseArticle(outer_page):
    # print("Inner Page processed:", page_count)
    logging.info("Inner page title: %s", outer_page["title"])
    post_source = get_page_raw_source_from_url(outer_page["link"])

    # time.sleep(5)

    # inner_page = getArticle(post_source)

    return post_source


def get_page_raw_source_from_url(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument("--kiosk")
    options.add_argument("--disable-popup-blocking")

    # with webdriver.Chrome(
    #     options=options, executable_path="c:/Users/javier.losada/Downloads/chromedriver/chromedriver.exe") \
    #         as driver_aux:
    try:
        driver_aux = webdriver.Chrome(
            options=options, executable_path="c:/Users/javier.losada/Downloads/chromedriver/chromedriver.exe")
        print("Really getting driver for:", url)
        logging.info("Really getting driver for: %s", url)
        driver_aux.get(url)
        return driver_aux.page_source
    except Exception as ex:
        logging.error("Exception: %s", ex)
        raise
    finally:
        if driver_aux is not None:
            driver_aux.close()


def divWithClass(tag):
    return tag is not None and "the-post-content-meta" in tag.split()


def getArticle(source_page_xml_param):
    techeblog_page = BeautifulSoup(source_page_xml_param, "lxml")

    strippingPattern = "\n\t"

    article = techeblog_page.find("article")

    title = article.h1.text.strip(strippingPattern).replace("'", "'")
    datetime = parse(article.find('time')['datetime'])
    images = [img["src"] for img in article.find_all("img")
              if img.get("src") and img.get("alt") and not img.get("class")]
    videos = [iframe["src"] for iframe in article.find_all("iframe")
              if iframe.get("src") and iframe.get("allow")]
    texts = [p.text.strip(strippingPattern) for p in article.find_all("p")
             if p.br is not None and p.text.strip(strippingPattern) != ""]
    blockquote = [blockquote.text.strip(strippingPattern) for blockquote in article.find_all("blockquote")
                  if blockquote.p is not None and blockquote.text.strip(strippingPattern) != ""]
    print("Texts length:", len(texts))
    print("Images length:", len(images))
    print("Videos length:", len(videos))
    print("Blockquote length:", len(blockquote))
    page = {"title": title, "datetime": str(datetime), "link": article.a["href"],
            "img": images, "video": videos, "text": texts, "blockquote": blockquote}

    # print(page)
    logging.info("Processing article: %s", title)

    return page


def getArticles(source_page_xml_param):
    techeblog_page = BeautifulSoup(source_page_xml_param, "lxml")

    strippingPattern = "\n\t"

    articles = techeblog_page.find_all("article")

    pages = []
    for article in articles:
        page = {"title": article.h2.text.strip(strippingPattern).replace("'", "'"), "link": article.a["href"]}

        print(page)

        pages.append(page)

    return pages


def writeToCSV(pages, depth, fieldnames, mode='w'):
    with open('pages-scrapped-' + depth + '.csv', mode, newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for page in pages:
            writer.writerow(page)


def writeToJson(pages, depth, mode='w'):
    with open('pages-scrapped-' + depth + '.json', mode, encoding='utf-8') as file:
        json.dump(pages, file, indent=4, ensure_ascii=False)


def processSourceArticles(outer_pages_aux):
    post_sources_aux = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        start_post_articles = time.time()
        futures = [executor.submit(parseArticle, outer_page) for outer_page in outer_pages_aux]
        for post_source_post in as_completed(futures):
            if post_source_post.exception() is not None:
                logging.error("There has been an Exception: %s", post_source_post.exception())
            else:
                post_sources_aux.append(post_source_post.result())
        end_post_articles = time.time()
        logging.info("Time Taken SourceArticles: {:.6f}s".format(end_post_articles-start_post_articles))
    return post_sources_aux


def processInnerArticles(post_sources_aux):
    inner_page_aux = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        start_inner_articles = time.time()
        futures = [executor.submit(getArticle, post_source) for post_source in post_sources_aux]
        for post_inner_page in as_completed(futures):
            if post_inner_page.exception() is not None:
                logging.error("There has been an Exception: %s", post_inner_page.exception())
            else:
                inner_page_aux.append(post_inner_page.result())
        end_inner_articles = time.time()
        logging.info("Time Taken InnerArticles: {:.6f}s".format(end_inner_articles-start_inner_articles))
    return inner_page_aux


def parse_and_get_articles(outer_page):
    return getArticle(parseArticle(outer_page))


def processSourcesInnerArticles(outer_pages_aux):
    inner_page_aux = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        start_source_inner_articles = time.time()
        futures = [executor.submit(parse_and_get_articles, outer_page) for outer_page in outer_pages_aux]
        for post_inner_page in as_completed(futures):
            if post_inner_page.exception() is not None:
                logging.error("There has been an Exception: %s", post_inner_page.exception())
            else:
                inner_page_aux.append(post_inner_page.result())
        end_source_inner_articles = time.time()
        logging.info("Time Taken SourceInnerArticles: {:.6f}s".format(end_source_inner_articles - start_source_inner_articles))
    return inner_page_aux


# def processArticlesNestedConcurrencyArticles(outer_pages_aux):
#     post_sources_aux = []
#     with ProcessPoolExecutor(max_workers=10) as executor:
#         start_post_articles = time.time()
#         futures_parsed_articles = [executor.submit(parseArticle, outer_page) for outer_page in outer_pages_aux]
#         for post_source_post in as_completed(futures_parsed_articles):
#             if post_source_post.exception() is not None:
#                 logging.error("There has been an Exception: %s", post_source_post.exception())
#             else:
#                 post_sources_aux.append(post_source_post.result())
#                 futures_got_articles = [executor.submit(getArticle, post_source) for post_source in post_sources_aux]
#
#         end_post_articles = time.time()
#         logging.info("Time Taken SourceArticles: {:.6f}s".format(end_post_articles - start_post_articles))
#     return post_sources_aux


def process_blog(url='http://www.techeblog.com/', concurrency_method=CONCURRENCY_SIMPLE):
    try:
        start_general = time.time()
        print("Starting the application!!!!")

        source_page_xml = get_page_raw_source_from_url('%s' % url)

        outer_pages = getArticles(source_page_xml)

        if concurrency_method == CONCURRENCY_SIMPLE:
            post_sources = processSourceArticles(outer_pages)

            inner_pages = processInnerArticles(post_sources)
        else:
            inner_pages = processSourcesInnerArticles(outer_pages)

        writeToCSV(outer_pages, "outer", ["title", "link"], "a")
        writeToCSV(inner_pages, "inner", ["title", "datetime", "link", "img", "video", "text", "blockquote"], "a")

        writeToJson(inner_pages, "inner", "a")

        end_general = time.time()
        logging.info("Time Taken General: {:.6f}s".format(end_general - start_general))
        print("Scrapping has finished!!!!!")

    except Exception as ex:
        logging.error("There has been an error!!: %s", ex)
        logging.error("Exception instance: %s", type(ex))
        logging.error("Exception args: %s", type(ex.args))


if __name__ == "__main__":
    process_blog()
