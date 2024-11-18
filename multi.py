import threading
from main import InstagramLoginProcess, InstagramActions
from rich.console import Console
import os

console = Console()


class InstagramManager:
    def __init__(self):
        self.sessions = {}

    def preload_sessions(self):
        console.print("[cyan]:hourglass_flowing_sand: Preloading sessions...[/cyan]")
        cookies_dir = "cookies"
        if not os.path.exists(cookies_dir):
            os.makedirs(cookies_dir)

        cookie_files = os.listdir(cookies_dir)
        for cookie_file in cookie_files:
            username = cookie_file.replace("_cookies.pkl", "")
            console.print(f"[yellow]:key: Preparing session for {username}...[/yellow]")
            process = InstagramLoginProcess()
            process.open_instagram()
            if process.load_cookies(username):
                console.print(f"[green]:cookie: Logged in using cookies for {username}.[/green]")
                self.sessions[username] = process
            else:
                console.print(f"[red]:warning: Cookies not found for {username}. Login required.[/red]")
                process.quit()

        if not self.sessions:
            console.print("[red]:x: No valid sessions found. Add users manually using the CLI.[/red]")

    def add_user(self, username, password):
        if username in self.sessions:
            console.print(f"[yellow]:warning: User {username} already exists.[/yellow]")
            return
        process = InstagramLoginProcess()
        process.open_instagram()
        process.login(username, password)
        self.sessions[username] = process

    def follow_all(self, target_username, count):
        console.print(f"[cyan]:mag_right: Starting follow action for {target_username}...[/cyan]")
        threads = []
        active_sessions = list(self.sessions.values())[:count]
        for process in active_sessions:
            actions = InstagramActions(process.driver)
            thread = threading.Thread(target=actions.follow, args=(target_username,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        console.print(f"[green]:white_check_mark: Follow action completed for {target_username}.[/green]")

    def close_all_sessions(self):
        console.print("[red]:wave: Closing all sessions...[/red]")
        for username, process in self.sessions.items():
            console.print(f"[yellow]:wave: Closing session for {username}...[/yellow]")
            process.quit()
