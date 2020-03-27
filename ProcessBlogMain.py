import getopt
import logging
import os
import sys
import time

from ScrapBlog import CONCURRENCY_MULTIPLE
from ScrapBlog import CONCURRENCY_SIMPLE
from ScrapBlog import get_concurrency_method
from ScrapBlog import process_blog

NUMBER_PAGES_PROCESS = 10

logging.basicConfig(handlers=[logging.FileHandler('ProcessBlogMain.log', 'a', 'utf-8')], level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main_with_arg(argv):
    try:
        opts, args = getopt.getopt(argv, "hrms", ["reset=", "multi", "simple"])
        print("opts:", opts)
        print("args:", args)
    except getopt.GetoptError:
        main()
    for opt, arg in opts:
        if opt in ('-r', '--reset'):
            os_listdir = [file for file in os.listdir('./') if file.endswith(tuple(['.csv', '.json']))]

            for f in os_listdir:
                os.remove(os.path.join('./', f))
        elif opt == '-h':
            print("Use -r/--reset to clean produced files")
        elif opt in ('-m', '--multi'):
            main(CONCURRENCY_MULTIPLE)
        else:
            # Default value is '-s' / '--simple'
            main(CONCURRENCY_SIMPLE)
    return


def main(concurrency_method=CONCURRENCY_MULTIPLE):
    start_general = time.time()
    print("Starting the application!!!!")
    print("Processing {} pages!!!!".format(NUMBER_PAGES_PROCESS))
    blog = 'http://www.techeblog.com/page/'
    logging.info("Processing the following blog:%s", blog)
    for i in range(1, NUMBER_PAGES_PROCESS):
        blog_current = blog + str(i) + '/'
        print("Processing the following blog:", blog_current)

        print("Performing a {} scraping".format(get_concurrency_method(concurrency_method)))
        logging.info("Performing a %s scraping", get_concurrency_method(concurrency_method))
        process_blog(blog_current, concurrency_method)

    end_general = time.time()
    logging.info("Time Taken Total: {:.6f}s".format(end_general - start_general))
    print("Scrapping has finished!!!!!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main_with_arg(sys.argv[1:])
    else:
        main()
