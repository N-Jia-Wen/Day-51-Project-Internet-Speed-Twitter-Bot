from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os

# Your internet service provider's promised upload/download speeds (in MB):
PROMISED_DOWN = 1000
PROMISED_UP = 1000
# Replace this with "@(Twitter account username of your internet provider)":
INTERNET_PROVIDER = "Internet Provider"
TWITTER_EMAIL = os.environ["TWITTER_EMAIL"]
TWITTER_PASSWORD = os.environ["TWITTER_PASSWORD"]
TWITTER_USERNAME = os.environ["TWITTER_USERNAME"]


class InternetSpeedTwitterBot:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(chrome_options)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        go_button = self.driver.find_element(By.CSS_SELECTOR, ".start-button a")
        go_button.click()
        time.sleep(45)

        self.down = self.driver.find_element(By.CLASS_NAME, "download-speed").text
        self.up = self.driver.find_element(By.CLASS_NAME, "upload-speed").text

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/i/flow/login")
        time.sleep(4)

        email_input = self.driver.find_element(By.NAME, "text")
        email_input.send_keys(TWITTER_EMAIL, Keys.ENTER)
        time.sleep(1)

        try:
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(TWITTER_PASSWORD, Keys.ENTER)
            time.sleep(4)
        except NoSuchElementException:
            username_input = self.driver.find_element(By.NAME, "text")
            username_input.send_keys(TWITTER_USERNAME, Keys.ENTER)
            time.sleep(2)

            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(TWITTER_PASSWORD, Keys.ENTER)
            time.sleep(4)

        create_post_button = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div'
                                                                '/div/div/div[1]/div[3]/a')
        create_post_button.click()
        time.sleep(1)

        privacy_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]'
                                                            '/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div'
                                                            '/div[2]/div[1]/div/div/div/div')
        privacy_button.click()
        only_mentioned_acc = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[3]/div/div/div[2]/div'
                                                                '/div[2]/div/div/div/div/div/div[2]/div[4]')
        only_mentioned_acc.click()
        time.sleep(1)

        composed_tweet = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]'
                                                         '/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]'
                                                         '/div[2]/div/div/div/div/div/div/div/div/div/div/div/label'
                                                         '/div[1]/div/div/div/div/div/div[2]/div')
        composed_tweet.send_keys(f"Hey {INTERNET_PROVIDER}, why is my internet speed {self.down}down/{self.up}up "
                                 f"when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?")

        confirm_post_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div'
                                                                 '/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div'
                                                                 '/div/div/div[2]/div[2]/div/div/div/div[4]')
        confirm_post_button.click()


twitter_bot = InternetSpeedTwitterBot()
twitter_bot.get_internet_speed()
twitter_bot.tweet_at_provider()
