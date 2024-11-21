from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext
from multi import InstagramManager
from rich.console import Console

TOKEN = "7325149894:AAGTxEjEVB5pFuV-kGN_4dEOCdX5GRfsVzo"
console = Console()

manager = InstagramManager()
manager.preload_sessions()

async def start(update: Update, context: CallbackContext):
    welcome_message = (
        "[cyan]🚀 Welcome to the Instagram Bot![/cyan]\n"
        "[green]Commands:[/green] \n"
        "[yellow]➕ /add <username> <password>[/yellow] - Add a new user\n"
        "[yellow]🔄 /follow <target_username> <count>[/yellow] - Follow a user with multiple accounts\n"
        "[yellow]❌ /exit[/yellow] - Exit the bot\n"
    )
    await update.message.reply_text(welcome_message)

async def add_user(update: Update, context: CallbackContext):
    try:
        username, password = context.args
        manager.add_user(username, password)
        await update.message.reply_text(f"[green]✅ User {username} added successfully.[/green]")
    except ValueError:
        await update.message.reply_text("[red]❌ Invalid command. Use: /add <username> <password>[/red]")

async def follow(update: Update, context: CallbackContext):
    try:
        target_username, count = context.args
        manager.follow_all(target_username, int(count))
        await update.message.reply_text(f"[green]✅ Follow action completed for {target_username}.[/green]")
    except ValueError:
        await update.message.reply_text("[red]❌ Invalid command. Use: /follow <target_username> <count>[/red]")

async def like(update: Update, context: CallbackContext):
    try:
        post_url, count = context.args
        manager.like_all(post_url, int(count))
        await update.message.reply_text(f"[green]✅ Like action completed for {post_url}.[/green]")
    except ValueError:
        await update.message.reply_text("[red]❌ Invalid command. Use: /like <post_url> <count>[/red]")

async def exit(update: Update, context: CallbackContext):
    manager.close_all_sessions()
    await update.message.reply_text("[red]👋 Closing all sessions. Goodbye![/red]")

async def unknown(update: Update, context: CallbackContext):
    await update.message.reply_text("[red]❌ Unknown command. Use /add, /follow, /like, or /exit.[/red]")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_user))
    application.add_handler(CommandHandler("follow", follow))
    application.add_handler(CommandHandler("like", like))
    application.add_handler(CommandHandler("exit", exit))

    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    application.run_polling()

if __name__ == "__main__":
    console.print("[cyan]🔄 Initializing sessions...[/cyan]")
    # manager.preload_sessions()

    main()
