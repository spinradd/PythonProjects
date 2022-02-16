from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException
import time
CHROME_PATH = r"C:\Users\spinr\PycharmProjects\Chrome Tools\chromedriver"

password = "dN$?xrmr4pYQ8#84"
username = "ComcastHostag3"
PROMISED_UP = 5
PROMISED_DOWN = 70

class InternetSpeedTwitterBot():
    def __init__(self):
        service = Service(CHROME_PATH)
        self.driver = webdriver.Chrome(service=service)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        self.driver.maximize_window()
        go = self.driver.find_element(By.XPATH, "//span[text()='Go']")
        go.click()
        time.sleep(60)
        try:
            download = self.driver.find_element(By.CLASS_NAME, "download-speed")
            upload = self.driver.find_element(By.CLASS_NAME, "upload-speed")
            download_speed = float(download.text)
            upload_speed = float(upload.text)
        except ValueError:
            print("More time was needed to complete the speed test")

        self.down = download_speed
        self.up = upload_speed


    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/?lang=en")
        time.sleep(2)
        try:
            login = self.driver.find_element(By.LINK_TEXT, "Sign in").click()
        except NoSuchElementException:
            login = self.driver.find_element(By.LINK_TEXT, "Log in").click()
        time.sleep(2)
        user_name = self.driver.find_element(By.TAG_NAME, "input")
        user_name.send_keys(username)
        user_name.send_keys(Keys.ENTER)
        time.sleep(2)
        pass_word = self.driver.find_element(By.CSS_SELECTOR, "input[name=password")
        pass_word.send_keys(password)
        pass_word.send_keys(Keys.ENTER)
        time.sleep(2)
        tweet_prompt = self.driver.find_element(By.CSS_SELECTOR, "a[data-testid=SideNav_NewTweet_Button]").click()
        time.sleep(2)
        tweet_prompt = self.driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block")
        message = (f"Comcast, my internet speeds are currently down:{self.down}"
                f"and up:{self.up} when I should be getting down:{PROMISED_DOWN}"        
                f"and up:{PROMISED_UP}")
        tweet_prompt.send_keys(message)
        send_tweet = self.driver.find_element(By.CSS_SELECTOR, "div[data-testid=tweetButton]").click()

if __name__=="__main__":
    bot = InternetSpeedTwitterBot()
    bot.get_internet_speed()
    if bot.up < PROMISED_UP and bot.down < PROMISED_DOWN:
        bot.tweet_at_provider()



