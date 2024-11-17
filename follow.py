from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import time
import pickle
import threading
from webdriver_manager.chrome import ChromeDriverManager
from rich import print

def open_and_follow_with_cookies(username, cookie_file, target_username):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service('./chromedriver'), options=options)
    driver.get("https://www.instagram.com")

    with open(os.path.join("cookies", cookie_file), "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(5)

    if "home" in driver.page_source:
        driver.get(f"https://www.instagram.com/{target_username}/")
        time.sleep(5)
        try:
            follow_button = driver.find_element(By.XPATH, "//button[.//div[contains(text(), 'Follow')]]")
            follow_button.click()
            print(f"[green]Followed {target_username} successfully with {username}[/green]")
        except Exception as e:
            print(f"[yellow]:warning: Could not follow {target_username} with {username}. Error: {e}[/yellow]")
    else:
        print(f"[red]:x: Failed to log in with cookies for {username}[/red]")
    driver.quit()

def open_all_accounts_with_cookies_and_follow(target_username):
    cookies_dir = "cookies"
    threads = []

    if not os.path.exists(cookies_dir):
        print("[red]:x: Cookies folder does not exist.[/red]")
        return

    cookie_files = os.listdir(cookies_dir)
    
    for cookie_file in cookie_files:
        username = cookie_file.replace('_cookies.pkl', '')
        thread = threading.Thread(target=open_and_follow_with_cookies, args=(username, cookie_file, target_username))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

target_username = "Canyildiz1386"
open_all_accounts_with_cookies_and_follow(target_username)
