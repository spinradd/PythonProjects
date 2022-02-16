from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

PASSWORD = YOUR_PASSWORD
EMAIL = YOUR_EMAIL
ACCOUNT_YOU_WANT_TO_MASS_FOLLOW = ACCOUNT_HANDLE
DRIVER_PATH = YOUR_DRIVER_PATH

class InstaFollower():
    def __init__(self):
        service = Service(f"r{DRIVER_PATH}")
        self.driver = webdriver.Chrome(service=service)

    def login(self):
        """get to and log into site"""
        self.driver.get("https://www.instagram.com/accounts/login/")
        self.driver.maximize_window()
        username_box = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']").send_keys(EMAIL)
        password_box = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(PASSWORD)
        button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(10)

    def findfollowers(self):
        """go to the page of the account you want to follow, open up the 'followers' section"""
        account_page = self.driver.get(f"https://www.instagram.com/{ACCOUNT_YOU_WANT_TO_MASS_FOLLOW}/")
        time.sleep(5)
        followers_parent = self.driver.find_elements(By.CLASS_NAME, "Y8-fY")[1]
        followers_child = followers_parent.find_element(By.XPATH, './/*').click()
        time.sleep(5)

    def follow(self):
        """find all the loaded followers, select follow for each at random time intervals, then scroll down after 10"""
        follows_children = self.driver.find_elements(By.XPATH, "//div[text()='Follow']")
        follows = 0
        window_div = self.driver.find_element(By.CLASS_NAME, "isgrP")
        for people in follows_children:
            parent = people.find_element(By.XPATH, "..")
            people.click()
            time.sleep(random.randint(2, 7))
            follows += 1
            if follows % 10 == 0:
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', window_div)
                follows_children = self.driver.find_elements(By.XPATH, "//div[text()='Follow']")


if __name__=="__main__":
    bot = InstaFollower()
    bot.login()
    bot.findfollowers()
    bot.follow()





