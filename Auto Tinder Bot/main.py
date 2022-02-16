from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

swipe_count = 0
DRIVER_PATH = YOUR_DRIVER_PATH
PASSWORD = YOUR_PASSWORD
EMAIL = YOUR_EMAIL

swipe_count = 0

# activate service
service = Service(f"r{DRIVER_PATH}")

# initialize driver
driver = webdriver.Chrome(service=service)

# get website
driver.get("https://tinder.com/")

# maximize window to ensure desktop formatting
driver.maximize_window()

# wait for site to load
time.sleep(2)

# locate and click sign in button
sign_in = driver.find_element(By.XPATH, "//span[text()='Log in']")
sign_in.click()
time.sleep(2)
sign_in_fb = driver.find_element(By.XPATH, "//span[text()='Log in with Facebook']")
sign_in_fb.click()

# get current browser windows, assign variable to main window, assign variable to sign in popup
base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]

# switch to popup
driver.switch_to.window(fb_login_window)

# enter in log in information, log in
enter_email = driver.find_element(By.ID, "email")
enter_email.send_keys(EMAIL)
passwrd = driver.find_element(By.ID, "pass")
passwrd.send_keys(PASSWORD)
next_btn = driver.find_element(By.ID, "loginbutton")
next_btn.click()

# switch to base window
driver.switch_to.window(base_window)

# wait for window to load
time.sleep(5)

# select inevitable pop up button, click button
allow = driver.find_element(By.XPATH, "//span[text()='Allow']")
allow.click()

# wait for next popup
time.sleep(2)

# select inevitable pop up button, click button
not_interested = driver.find_element(By.XPATH, "//span[text()='Not interested']")
not_interested.click()

# wait for next popup
time.sleep(2)

# select inevitable pop up button, click button
cookies = driver.find_element(By.XPATH, "//span[text()='I Accept']")
cookies.click()

# select inevitable pop up button, click button
pop1 = driver.find_element(By.XPATH, "//span[text()='Maybe Later']")
pop1.click()

# wait for screen to load
time.sleep(3)

# until we reach our max swipes, swipe right or left
while swipe_count <= 100:
    try:
        # find inner span of button
        filter_out_span = driver.find_element(By.XPATH, "//span[text()='Like']")

        # zoom out to find clickable button
        filter_out = filter_out_span.find_element(By.XPATH, "..")
        filter_out.click()

        time.sleep(1)
        swipe_count += 1
    except:
        driver.quit()
driver.quit()




