from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import bs4
import requests

APARTMENTS_URL = APARTMENTS_DOT_COM_SEARCH_URL
FORM_URL = YOUR_GOOGLE_DOC_FORM
DRIVER_PATH = YOUR_DRIVER_PATH

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}

# get html from website
response = requests.get(url=APARTMENTS_URL, headers=HEADERS)
response.raise_for_status()
html = response.text

# convert html to soup
soup = bs4.BeautifulSoup(html, "html.parser")

# find number of pages for your search
page_range = int(soup.find("span", class_="pageRange").text.split()[3])

# initialize data lists
addresses = []
rents = []
urls = []

# for all pages, mine listings and information and store in lists
for n in range(0, page_range-1):

    # if it isn't the first page, conform url to that extra page, then mine for data
    if n != 0:
        new_soup_url = f"{'first_half_of_url/'}{1+n}{'/second_half_of_url'}"

        # get html for new page
        new_response = requests.get(url=APARTMENTS_URL, headers=HEADERS)
        new_response.raise_for_status()
        new_html = response.text

        # convert to soup
        new_soup = bs4.BeautifulSoup(new_html, "html.parser")
        # mine for all listings
        listings = soup.find_all("li", class_="mortar-wrapper")

    # for each listing, find url, rent range, and address and place in lists
    for list in listings:
        url = list.find("article", class_="placard")
        url = url.get("data-url")
        urls.append(url)
        rent = list.find("p", class_="property-pricing")
        rent = rent.text
        rents.append(rent)
        address = list.find("div", class_="property-address")
        address = address.text
        addresses.append(address)


# initialize service
service = Service(f"r{DRIVER_PATH}")

# initialize driver
driver = webdriver.Chrome(service=service)

# maximize window for consistnent website layout
driver.maximize_window()

# go to google form, assumes access via link
driver.get(FORM_URL)
current_window = driver.current_window_handle
time.sleep(2)

# for each address, input address into "address" section of google form. Same with url and rent range
for n in range(0, len(addresses)-1):

    # find all input sections for google form
    inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")

    # address text boc
    inputs[0].send_keys(addresses[n])

    # rent text box
    inputs[1].send_keys(rents[n])

    # url text box
    inputs[2].send_keys(urls[n])
    time.sleep(3)

    # submit form
    submit = driver.find_element(By.CSS_SELECTOR, "div[role='button']").click()
    time.sleep(3)

    # select create another entry
    submit_another = driver.find_element(By.TAG_NAME, "a").click()
    time.sleep(2)

driver.quit()
