from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import random
import os
from time import sleep

cur_path = os.path.dirname(os.path.realpath(__file__))


def enable_headless_download(browser, download_path):
    # Add missing support for chrome "send_command" to selenium webdriver
    browser.command_executor._commands["send_command"] = \
        ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': download_path}}
    browser.execute("send_command", params)

def find_element_by_xpath(driver, xpath):
    driver.find_element_by_xpath(xpath)
    sleep(10)


def crawl():
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

    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--window-size=1920x1080')

    # Startexi up browser
    browser = webdriver.Chrome(executable_path=webdriver_path,
                               chrome_options=chrome_options)

    enable_headless_download(browser, download_path)

    # Load webpage
    browser.get(url)
    time.sleep(10)

    get = browser.find_element_by_xpath("//input[@aria-label = 'Enter a search term or a topic']")
    sleep(10)
    get.send_keys("Samsung Galaxy S9")
    sleep(5)
    get.send_keys(Keys.ENTER)
    sleep(5)

    choose_drop_down_range = browser.find_element_by_xpath("//div[contains(text(), 'Past 12 months')]")
    sleep(5)
    choose_drop_down_range.click()
    sleep(5)
    print('good')

    choose_range = browser.find_element_by_xpath("//div[contains(text(), 'Past 90 days')]")
    sleep(5)
    choose_range.click()
    sleep(5)
    print('good')



    # button = browser.find_element_by_css_selector('.widget-actions-item.export')
    # sleep(10)
    # button.send_keys("Samsung Galaxy X9")
    # sleep(5)
    # browser.quit()


if __name__ == "__main__":
    crawl()