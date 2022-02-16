from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException
import time

# locate and activate service
PATH_TO_DRIVER = YOUR_ABSOLUTE_PATH_TO_SELNIUM_DRIVER
PASSWORD = YOUR_LINKED_PASSWORD
USERNAME = YOUR_LINKED_USERNAME
PHONE_NUM = YOUR_PHONE_NUMBER
service = Service(f"r{PATH_TO_DRIVER}")

# go to linked in website job forum, type in parameters for job, copy and paste LinkedIn URL here
LINKEDIN_URL = YOUR_SEARCH_URL

# initialize driver
driver = webdriver.Chrome(service=service)

driver.get(LINKEDIN_URL)
driver.maximize_window()

# locate sign in button on page
sign_in = driver.find_element(By.CLASS_NAME, "nav__button-secondary")
sign_in.click()

# find user detaiils on pop up, enter in user details, and click log in ("submit")
user = driver.find_element(By.ID, "username")
user.send_keys(USERNAME)
pass_ = driver.find_element(By.ID, "password")
pass_.send_keys(PASSWORD)
submit = driver.find_element(By.CLASS_NAME, "btn__primary--large")
submit.click()

# wait for page to load
time.sleep(5)

# scan LinkedIn job list, mine all jobs
all_jobs = driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")

# for all jobs on page...
for jobs in all_jobs:

    # click job, wait for load
    jobs.click()
    time.sleep(1)

    # try clicking an instant apply button
    try:
        job_button = driver.find_element(By.CSS_SELECTOR, ".jobs-apply-button")

    # if unsuccessful, there is no "Easy Apply" skip job
    except NoSuchElementException:
        continue

    # once clicked "Easy Apply", find boxes for relevant information
    job_button.click()
    phone = driver.find_elements(By.CSS_SELECTOR, ".fb-single-line-text__input")

    # if phone number has already been loaded (from cache)
    if len(phone) > 1:

        # if phone number is already filled in, find submit button and submit
        try:
            submit = driver.find_element(By.CSS_SELECTOR, "footer button")
            print(f"submit: {submit}")

        # if submit button does not exist, then there is no "Easy Apply", pass the error and locate the "x" button
        except:
            pass

        else:
            x_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-modal__dismiss")
            x_button.click()

            # after clicking accept / close, find and select to close the proceeding pop-up window
            discard = driver.find_element(By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")
            discard.click()

    # if phone number hasn't been entered, enter in phone number, and then submit
    else:
        if phone[0].text == "":
            phone[0].send_keys(PHONE_NUM)
        try:
            submit = driver.find_element(By.CSS_SELECTOR, "footer button")
            print(f"submit: {submit}")

        # if submit button does not exist, then there is no "Easy Apply", pass the error and locate the "x" button
        except:
            pass
        else:
            x_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-modal__dismiss")
            x_button.click()
            discard = driver.find_element(By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")
            discard.click()
