from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from rich import print
from rich.console import Console
import time
import os
import pickle
import imapclient
import pyzmail

console = Console()

class InstagramLoginProcess:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def open_instagram(self):
        console.print(":globe_with_meridians: [bold cyan]Opening Instagram...[/bold cyan]")
        self.driver.get("https://www.instagram.com")
        time.sleep(5)
        self.check_and_accept_cookies()

    def check_and_accept_cookies(self):
        console.print(":cookie: [bold yellow]Checking for 'Allow All Cookies' button...[/bold yellow]")
        if self.check_for_text('Allow the use'):
            cookies_button = self.driver.find_element(By.XPATH, "//button[contains(@class, '_a9-- _ap36 _a9_0')]")
            cookies_button.click()
            console.print("[green]:white_check_mark: Accepted cookies.[/green]")
            time.sleep(2)
        else:
            console.print("[yellow]:warning: 'Allow All Cookies' button not found.[/yellow]")

    def load_cookies(self, username):
        cookie_file = f"{username}_cookies.pkl"
        console.print(f":cookie: [bold yellow]Loading cookies for {username}...[/bold yellow]")
        if os.path.exists(cookie_file):
            with open(cookie_file, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            console.print("[green]:white_check_mark: Cookies loaded from file.[/green]")
            self.driver.refresh()
            time.sleep(5)
            return True
        console.print("[yellow]:warning: No cookie file found; proceeding with login.[/yellow]")
        return False

    def login(self, username, password):
        if not self.load_cookies(username):
            console.print(f":key: [bold cyan]Attempting login for {username}...[/bold cyan]")
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            username_field.send_keys(username)
            password_field.send_keys(password)
            username_field.send_keys(Keys.RETURN)
            console.print(":hourglass_flowing_sand: [bold cyan]Waiting for the home page to load...[/bold cyan]")
            self.wait_for_home_page()
            self.save_cookies(username)

    def wait_for_home_page(self):
        while not self.check_text("home"):
            time.sleep(1)
        console.print("[green]:house: Logged in successfully![/green]")

    def check_text(self, text):
        return text in self.driver.page_source

    def check_for_text(self, text):
        page_source = self.driver.page_source
        return text in page_source

    def save_cookies(self, username):
        with open(f"{username}_cookies.pkl", "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)
        console.print(f"[green]:floppy_disk: Cookies saved as {username}_cookies.pkl[/green]")

    def quit(self):
        self.driver.quit()
        console.print(":wave: [bold blue]Closed browser and ended session.[/bold blue]")

class InstagramActions:
    def __init__(self, driver):
        self.driver = driver

    def follow(self, target_username):
        console.print(f":mag_right: [bold cyan]Navigating to {target_username}'s profile to follow...[/bold cyan]")
        self.driver.get(f"https://www.instagram.com/{target_username}/")
        time.sleep(5)
        
        try:
            follow_button = self.driver.find_element(By.XPATH, "//button[.//div[contains(text(), 'Follow')]]")
            follow_button.click()
            console.print(f"[green]:white_check_mark: Clicked 'Follow' button for {target_username}.[/green]")
            WebDriverWait(self.driver, 20).until(
                EC.text_to_be_present_in_element((By.XPATH, "//button"), "Following")
            )
            console.print(f"[green]:white_check_mark: Now following {target_username} successfully.[/green]")
        except TimeoutException:
            console.print(f"[yellow]:warning: Timeout waiting for follow confirmation for {target_username}.")
        except Exception as e:
            console.print(f"[yellow]:warning: Could not follow {target_username}. Error: {e}[/yellow]")

if __name__ == "__main__":
    login_process = InstagramLoginProcess()
    login_process.open_instagram()
    
    username = "Canyildiz1386"
    password = "Rahyab1357"
    login_process.login(username, password)
    
    if login_process.check_text("home"):
        console.print("[green]:cookie: Logged in with cookies.[/green]")
    else:
        console.print("[red]:x: Login failed or cookies not found.[/red]")
    
    actions = InstagramActions(login_process.driver)
    target_username = "cristiano"
    actions.follow(target_username)
    
    # login_process.quit()
