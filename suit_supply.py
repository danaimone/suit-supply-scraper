import json
import re
import time

import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from Product import Product
import argparse
from apscheduler.schedulers.blocking import BlockingScheduler
from webdrivermanager import GeckoDriverManager

sched = BlockingScheduler()
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.headless = True
driver = webdriver.Firefox(options=options, executable_path="geckodriver.exe")


def get_suits_page(web_driver: selenium.webdriver, size, color):
    web_driver.get("https://outlet-us.suitsupply.com/en_US/home")
    form = web_driver.find_element_by_id("dwfrm_clearancelanding_code")
    form.send_keys("2020")
    button = web_driver.find_element_by_id("sendBtn")
    button.click()
    web_driver.get(
        f"https://outlet-us.suitsupply.com/en_US/c_suits?prefn1=colorID&prefv1={color}&prefn2=size&prefv2={size}")


def scroll_to_end(web_driver: selenium.webdriver, scroll_pause_time=2):
    # Get scroll height
    last_height = web_driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = web_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


def list_to_string(list):
    temp = ""
    return temp.join(list)


def add_to_product_list(product_list, text):
    list_of_words = text.split()
    identity = list_to_string(list_of_words[0:10])
    color = list_to_string(list_of_words[0:2])
    type = list_to_string(list_of_words[2:4])
    material = list_to_string(list_of_words[4:6])
    original_price = list_to_string(list_of_words[6:8])
    sale_price = list_to_string(list_of_words[8:10])
    product_to_add = Product(identity, color, type, material, sale_price, original_price)
    product_list.append(product_to_add)


def in_stock(web_driver: selenium.webdriver, filter):
    """
    Checks if a given web page has filter text on page and returns
    the list of products, or None if there are none.
    :rtype: List[] Products in Stock, or None if not found
    """
    product_list = []
    HTML = web_driver.page_source
    doc = BeautifulSoup(HTML, "html.parser")
    page_text = doc.get_text().strip()
    formatted_text = page_text.replace("\n", " ").strip()
    formatted_text = re.sub(r'\s+', ' ', formatted_text)

    find_all_indexes = list(find_all(formatted_text, filter))
    if find_all_indexes != 0:
        for index in find_all_indexes:
            product_text = formatted_text[index:]
            add_to_product_list(product_list, product_text)

    return product_list


def update_json(file_name, product_list):
    with open(file_name, 'w') as json_write:
        json.dump([product.__dict__ for product in product_list], json_write)


def notify_through_ITT(message, key, event="product_list_updated"):
    print("Notifying a new deal...")
    report = {}
    report["value1"] = message
    print(requests.post(f"https://maker.ifttt.com/trigger/{event}/with/key/{key}",
                        data=report).content)


def find_suit_deals(filter, color, size, event, IFTTT_key):
    start_time = time.time()
    item_in_stock = []
    while True:
        product_count = len(item_in_stock)
        get_suits_page(driver, size, color)
        scroll_to_end(driver)
        item_in_stock = list(in_stock(driver, filter))
        current_product_count = len(item_in_stock)
        if current_product_count > product_count:
            print("Found a new item!")
            for product in item_in_stock:
                notify_through_ITT(product.identity, IFTTT_key, event, )
        print("Searching...")
        time.sleep(3600 - ((time.time() - start_time) % 3600))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create an IFTTT trigger for stock on Suit Supply Outlet")
    parser.add_argument('key',
                                    help="Webhook key that can be found under the IFTTT Webhook documentation page.")
    parser.add_argument('filter',
                        help="The words you want to filter for. Example: 'Dark Grey Sienna'")
    parser.add_argument('color',
                        help="The color of the item you are searching for. Example: 'Grey'")
    parser.add_argument('size',
                        help="The size of the item you're trying to find. Example: 38")
    parser.add_argument('--event',
                        help="Event webhook name, defaults to 'product_list_updated'")
    parser.add_argument('--install', type=bool,
                        help="Installs the correct Gecko Driver if one is not already installed.")
    return parser.parse_args()


def install_gecko_driver():
    gdd = GeckoDriverManager()
    gdd.download_and_install()


if __name__ == "__main__":
    args = parse_args()
    if args.install:
        install_gecko_driver()

    IFTTT_key = args.key
    filter = args.filter
    color = args.color
    size = args.size
    event = args.event
    find_suit_deals(filter, color, size, event, IFTTT_key)
