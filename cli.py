from multi import InstagramManager
from rich.console import Console

console = Console()


def start_cli(manager):
    console.print("[cyan]:keyboard: CLI Started. Type commands below.[/cyan]")
    console.print("[green]Commands:[/green] [yellow]add <username> <password>[/yellow], [yellow]follow <target_username> <count>[/yellow], [yellow]exit[/yellow]")
    while True:
        command = input("> ").strip()
        if command.lower() == "exit":
            break
        if command.startswith("add"):
            try:
                _, username, password = command.split()
                manager.add_user(username, password)
            except ValueError:
                console.print("[red]:x: Invalid command. Use: add <username> <password>[/red]")
        elif command.startswith("follow"):
            try:
                _, target_username, count = command.split()
                manager.follow_all(target_username, int(count))
            except ValueError:
                console.print("[red]:x: Invalid command. Use: follow <target_username> <count>[/red]")
        else:
            console.print("[red]:x: Unknown command. Use add, follow, or exit.[/red]")


if __name__ == "__main__":
    manager = InstagramManager()

    console.print("[cyan]:hourglass_flowing_sand: Initializing sessions...[/cyan]")
    manager.preload_sessions()

    try:
        start_cli(manager)
    finally:
        manager.close_all_sessions()
