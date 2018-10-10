from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import time
import random
import os
from time import sleep


cur_path = os.path.dirname(os.path.realpath(__file__))

def enable_headless_download(browser, download_path):
    """
    In here, we want to make function to enable download in headless mode

    :param browser:
    :param download_path:
    :return:
    """
    browser.command_executor._commands["send_command"] = \
        ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': download_path}}
    browser.execute("send_command", params)


def crawl():
    """
    In here we will crawl data from the website
    :return:
    """

    webdriver_path = cur_path + '/chromedriver'
    url = 'https://trends.google.com/trends/'
    user_agent =  [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7"
    ]

    download_path = cur_path

    # Add arguments telling Selenium to not actually open a window
    chrome_options = Options()
    download_prefs = {'download.default_directory': download_path,
                      'download.prompt_for_download': False,
                      'profile.default_content_settings.popups': 0}

    chrome_options.add_experimental_option('prefs', download_prefs)
    chrome_options.add_argument(
        '--user-agent={}'.format(random.choice(user_agent)))

    ## This script if we want to running in headless mode
    # chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(executable_path=webdriver_path, chrome_options=chrome_options)
    enable_headless_download(browser, download_path)

    # Load webpage
    browser.get(url)
    time.sleep(20)

    try:

        get_topic = browser.find_element_by_xpath("//input[@aria-label = 'Enter a search term or a topic']")
        sleep(10)
        get_topic.send_keys("Samsung Galaxy S9")
        sleep(5)
        get_topic.send_keys(Keys.ENTER)
        sleep(5)

    except (NoSuchElementException, ElementNotVisibleException):
        exit("Crawling is failed")

    try:

        choose_drop_down_range = browser.find_element_by_xpath("//div[contains(text(), 'Past 12 months')]")
        sleep(5)
        choose_drop_down_range.click()
        sleep(5)

    except (NoSuchElementException, ElementNotVisibleException):
        exit("Crawling is failed")

    try:
        choose_range_date = browser.find_element_by_xpath("//div[contains(text(), 'Past 90 days')]")
        sleep(5)
        choose_range_date.click()
        sleep(5)

    except (NoSuchElementException, ElementNotVisibleException):
        exit("Crawling is failed")

    try:

        get_csv = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/md-content/div/div/div[1]/"
                                                "trends-widget/ng-include/widget/div/div/div/widget-actions/"
                                                "div/button[1][@class = 'widget-actions-item export']")
        sleep(5)
        get_csv.click()
        sleep(20)

    except (NoSuchElementException, ElementNotVisibleException):
        exit("Crawling is failed")


if __name__ == "__main__":
    crawl()