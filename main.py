from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException , NoSuchElementException
from rich import print
from rich.console import Console
import time
import os
import pickle
import threading

console = Console()

class InstagramLoginProcess:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service('./chromedriver'), options=options)
        self.cookies_dir = "cookies"
        self.create_cookies_folder()

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

    def create_cookies_folder(self):
        if not os.path.exists(self.cookies_dir):
            os.makedirs(self.cookies_dir)
            console.print(f"[green]:file_folder: Created folder '{self.cookies_dir}' for storing cookies.[/green]")

    def load_cookies(self, username):
        cookie_file = os.path.join(self.cookies_dir, f"{username}_cookies.pkl")
        if os.path.exists(cookie_file):
            with open(cookie_file, "rb") as file:
                for cookie in pickle.load(file):
                    self.driver.add_cookie(cookie)
            console.print("[green]:white_check_mark: Cookies loaded from file.[/green]")
            time.sleep(5)
            self.driver.refresh()
            return True
        console.print("[yellow]:warning: No cookie file found; proceeding with login.[/yellow]")
        return False

    def save_cookies(self, username):
        cookie_file = os.path.join(self.cookies_dir, f"{username}_cookies.pkl")
        with open(cookie_file, "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)
        console.print(f"[green]:floppy_disk: Cookies saved as {cookie_file}[/green]")

    def login(self, username, password):
        if not self.load_cookies(username):
            console.print(f":key: [bold cyan]Attempting login for {username}...[/bold cyan]")
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            username_field.send_keys(username)
            password_field.send_keys(password)
            username_field.send_keys(Keys.RETURN)
            console.print(":hourglass_flowing_sand: [bold cyan]Waiting for the verification prompt or home page to load...[/bold cyan]")
            self.handle_two_factor_auth()
            self.wait_for_home_page()
            self.save_cookies(username)

    def handle_two_factor_auth(self):
        try:
            
            WebDriverWait(self.driver, 40).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Enter the code we sent to")
            )
            console.print("[yellow]:mailbox: Code sent to your email. Please enter the code below.[/yellow]")
            code = input("Enter the code received by email: ")
            code_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "email"))  
            )
            code_field.send_keys(code)
            code_field.send_keys(Keys.RETURN)
            time.sleep(30)
            console.print("[green]:white_check_mark: Code entered, attempting login...[/green]")
        except TimeoutException:
            console.print("[yellow]:warning: No two-factor authentication prompt appeared; proceeding without it.[/yellow]")


    def wait_for_home_page(self):
        while not self.check_text("home"):
            time.sleep(20)
        console.print("[green]:house: Logged in successfully![/green]")

    def check_text(self, text):
        return text in self.driver.page_source

    def check_for_text(self, text):
        page_source = self.driver.page_source
        return text in page_source

    def check_all_cookies(self):
        if not os.path.exists(self.cookies_dir):
            console.print("[red]:x: Cookies folder does not exist.[/red]")
            return
        
        cookie_files = os.listdir(self.cookies_dir)
        if not cookie_files:
            console.print("[yellow]:warning: No cookies found in the folder.[/yellow]")
            return

        for cookie_file in cookie_files:
            username = cookie_file.replace('_cookies.pkl', '')
            console.print(f":file_folder: [bold cyan]Checking cookies for user: {username}[/bold cyan]")
            
            self.driver.get("https://www.instagram.com")
            self.load_cookies(username)
            self.driver.refresh()
            time.sleep(5)
            
            if self.check_text("home"):
                console.print(f"[green]:white_check_mark: Cookies for {username} are valid and logged in successfully.[/green]")
            else:
                console.print(f"[red]:x: Cookies for {username} are invalid or expired; login failed.[/red]")

            self.driver.delete_all_cookies()

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
                lambda driver: "Following" in driver.page_source
            )
            console.print(f"[green]:white_check_mark: Now following {target_username} successfully.[/green]")
        except TimeoutException:
            console.print(f"[yellow]:warning: Timeout waiting for follow confirmation for {target_username}.")
        except NoSuchElementException:
            console.print(f"[yellow]:warning: Could not follow {target_username}. ⚠ HandleIt: No follow button found on profile page.[/yellow]")
        except Exception as e:
            console.print(f"[yellow]:warning: Could not follow {target_username}. Error: {e}[/yellow]")



def open_and_follow(username, cookie_file, target_username):
    process = InstagramLoginProcess()
    process.open_instagram()
    if process.load_cookies(username):
        actions = InstagramActions(process.driver)
        actions.follow(target_username)
    process.quit()

def open_all_accounts_with_cookies_and_follow(target_username):
    cookies_dir = "cookies"
    threads = []

    if not os.path.exists(cookies_dir):
        console.print("[red]:x: Cookies folder does not exist.[/red]")
        return

    cookie_files = os.listdir(cookies_dir)
    
    for cookie_file in cookie_files:
        username = cookie_file.replace('_cookies.pkl', '')
        thread = threading.Thread(target=open_and_follow, args=(username, cookie_file, target_username))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    login_process = InstagramLoginProcess()
    login_process.open_instagram()
    # login_process.check_all_cookies()
    
    username = "delniya_khavaran78"
    password = "bahar1378##"
    login_process.login(username, password)
    
    # if login_process.check_text("home"):
    #     console.print("[green]:cookie: Logged in with cookies.[/green]")
    # else:
    #     console.print("[red]:x: Login failed or cookies not found.[/red]")
    
    # actions = InstagramActions(login_process.driver)
    # target_username = "Canyildiz1386"
    # actions.follow(target_username)

    # target_username = "Canyildiz1386"
    # open_all_accounts_with_cookies_and_follow(target_username)
    

    
    
