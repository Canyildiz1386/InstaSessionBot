import asyncio
import time
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sqlite3
from concurrent.futures import ThreadPoolExecutor

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        
        # Ensure the cookies directory exists
        if not os.path.exists("cookies"):
            os.makedirs("cookies")

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        try:
            with open(f"cookies/{self.username}_cookies.pkl", "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            self.driver.refresh()
        except FileNotFoundError:
            self.driver.find_element(By.NAME, "username").send_keys(self.username)
            self.driver.find_element(By.NAME, "password").send_keys(self.password)
            self.driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
            time.sleep(5)
            cookies = self.driver.get_cookies()
            with open(f"cookies/{self.username}_cookies.pkl", "wb") as file:
                pickle.dump(cookies, file)

    def follow_user(self, user_to_follow):
        self.driver.get(f"https://www.instagram.com/{user_to_follow}/")
        time.sleep(2)
        follow_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Follow')]")
        follow_button.click()

    def close(self):
        self.driver.quit()

def get_accounts_and_target():
    connection = sqlite3.connect('accounts.db')
    cursor = connection.cursor()
    cursor.execute("SELECT username, password FROM accounts")
    accounts = cursor.fetchall()
    cursor.execute("SELECT username FROM target LIMIT 1")
    target_username = cursor.fetchone()[0]
    connection.close()
    return accounts, target_username

def run_bot(username, password, user_to_follow):
    bot = InstagramBot(username, password)
    bot.login()
    bot.follow_user(user_to_follow)
    bot.close()

async def main():
    accounts, user_to_follow = get_accounts_and_target()
    
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=len(accounts)) as executor:
        tasks = [
            loop.run_in_executor(executor, run_bot, username, password, user_to_follow)
            for username, password in accounts
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
