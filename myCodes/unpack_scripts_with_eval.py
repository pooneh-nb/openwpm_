import itertools
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from myCodes import utilities
import multiprocessing
from multiprocessing import Pool as ThreadPool



def read_file_newline_stripped(file_path):
    with open(file_path) as f:
        content = [word.strip() for word in f if word.strip() != '']
    return content


def append_file(file_name, content):
    with open(file_name, "a") as myfile:
        myfile.write(content + '\n')


def multiprocess_crawl(url_to_open, driver_path, binary_path):
    page_load_timeout = 10
    file_write_timeout = 4
    log_extraction_script = "document.createCDATASection('NOTVERYUNIQUESTRING');"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--chrome-binary=' + binary_path)
    chrome_options.binary_location = binary_path

    driver = webdriver.Chrome(driver_path, options=chrome_options)
    driver.set_page_load_timeout(page_load_timeout)

    url_to_open = url_to_open.split('/')[-1]
    try:
        print('Opening URL: ' + url_to_open)

        # driver.get('http://127.0.0.1:8000/' + url_to_open)
        # The driver.get method will navigate to a page given by the URL.
        driver.get("http://0.0.0.0:8000/" + url_to_open)
        time.sleep(file_write_timeout)
        try:
            driver.execute_script(log_extraction_script)
            append_file('crawl.log', url_to_open)

        except BaseException as ex:
            print('[Main Frame] Something went wrong: ' + str(ex))
            time.sleep(4)
            pass

        #driver.quit()
        #driver.close()

    except BaseException as ex:
        print('Something went wrong: ' + str(ex))
        print(url_to_open)
        time.sleep(4)
        #time.sleep(4)
        #driver.quit()
        #driver.close()
        pass
    finally:
        driver.quit()
        #driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
        #driver.set_page_load_timeout(page_load_timeout)


def crawl(driver_path, binary_path, log_extraction_script, websites_to_crawl, page_load_timeout=10, file_write_timeout=4):
    pass


    """for url_to_open in websites_to_crawl:
        url_to_open = url_to_open.split('/')[-1]
        try:
            print('Opening URL: ' + url_to_open)
            append_file('crawl.log', url_to_open)
            #driver.get('http://127.0.0.1:8000/' + url_to_open)
            # The driver.get method will navigate to a page given by the URL.
            driver.get("http://0.0.0.0:8000/" + url_to_open)
            time.sleep(file_write_timeout)
            try:
                driver.execute_script(log_extraction_script)
            except BaseException as ex:
                print('[Main Frame] Something went wrong: ' + str(ex))
                pass
            time.sleep(1)

        except BaseException as ex:
            print('Something went wrong: ' + str(ex))
            pass
        finally:
            driver.quit()
            driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
            driver.set_page_load_timeout(page_load_timeout)"""


def main():
    driver_path = '/home/c6/Downloads/chromedriver'  # ~/data/input/selenium/drive/chromedriver
    binary_path = '/home/c6/Documents/dockdockgo/AdGraph/chrome' # ~/data/input/selenium/adgraph/chrome
    websites_to_crawl_dir = '/home/c6/Documents/OpenWPM2/datadir/inline_js/unpacking/packed_html_files'
    # ~/data/input/unpacking/2020/unpacking/packed_html_files/
    #driver_path = sys.argv[1]
    #binary_path = sys.argv[2]
    #websites_to_crawl_dir = sys.argv[3]
    raw_websites_to_crawl = utilities.get_files_in_a_directory(websites_to_crawl_dir)
    visited_websites = utilities.read_file_newline_stripped("crawl.log")
    websites_to_crawl = []
    for site in raw_websites_to_crawl:
        if site.split('/')[-1] not in visited_websites:
            websites_to_crawl.append(site)
    print(len(websites_to_crawl))
    #websites_to_crawl = ["https://google.com"]
    #log_extraction_script = "document.createCDATASection('NOTVERYUNIQUESTRING');"
    #crawl(driver_path, binary_path, log_extraction_script, websites_to_crawl)

    for site in websites_to_crawl:
        multiprocess_crawl(site, driver_path, binary_path)
    """cpu_to_relax = 1
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    #pool = ThreadPool(processes=1)
    results = pool.starmap(multiprocess_crawl,
                           zip(websites_to_crawl, itertools.repeat(driver_path), itertools.repeat(binary_path)))
    pool.close()
    pool.join()"""

    crawl_log = read_file_newline_stripped('crawl.log')
    if websites_to_crawl[-1] == crawl_log[-1]:
        print('All files crawled. Exiting now.')
    else:
        print(len(websites_to_crawl_dir), len(crawl_log))


if __name__ == '__main__':
    main()