import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace this string with your actual BotFather token
TOKEN = "80-6xcgvw"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a link and I'll process it for you!")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if not (url.startswith("http://") or url.startswith("https://")):
        await update.message.reply_text("Please send a valid link starting with http:// or https://")
        return

    await update.message.reply_text("⏳ Processing link...")

    try:
        # Example web task: Fetching page title and headings
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No title"
            
            # Grabbing top headings from the page
            headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2'])[:3]]
            headings_list = "\n".join([f"• {h}" for h in headings]) if headings else "None found"

            reply = f"✅ **Task Done!**\n\n**Page Title:** {title}\n\n**Key Headings:**\n{headings_list}"
            await update.message.reply_text(reply, parse_mode="Markdown")
        else:
            await update.message.reply_text(f"Could not open site. Status code: {response.status_code}")

    except Exception as e:
        await update.message.reply_text(f"Error executing task: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_link))
    app.run_polling()
  
