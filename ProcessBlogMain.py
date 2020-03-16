import logging

from ScrapBlog import process_blog

logging.basicConfig(filename='ProcessBlogMain.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main():
    blog = 'http://www.techeblog.com/'
    print("Processing the following blog:", blog)
    logging.info("Processing the following blog:%s", blog)
    process_blog(blog)


if __name__ == "__main__":
    main()


