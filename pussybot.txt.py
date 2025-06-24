
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import time
import json
from pathlib import Path

BALANCE_FILE = Path("balance.json")
COOLDOWN_FILE = Path("cooldown.json")

def load_data(path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_data(path, data):
    with open(path, "w") as f:
        json.dump(data, f)

async def pussy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or update.effective_user.first_name

    balance = load_data(BALANCE_FILE)
    cooldowns = load_data(COOLDOWN_FILE)

    now = time.time()
    last_time = cooldowns.get(user_id, 0)

    if now - last_time < 3600:
        await update.message.reply_text("⏳ Подожди немного... пусси отдыхает (1 раз в час)")
        return

    change = random.randint(-10, 10)
    old_size = balance.get(user_id, 20)
    new_size = max(old_size + change, 0)

    balance[user_id] = new_size
    cooldowns[user_id] = now

    save_data(BALANCE_FILE, balance)
    save_data(COOLDOWN_FILE, cooldowns)

    if change >= 0:
        msg = f"🐱 Твоя пусси расширилась на +{change} см 💦\nТеперь она: {new_size} см"
    else:
        msg = f"🐱 Твоя пусси сжалась на {change} см 😿\nТеперь она: {new_size} см"

    await update.message.reply_text(msg)

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    balance = load_data(BALANCE_FILE)
    sorted_users = sorted(balance.items(), key=lambda x: x[1], reverse=True)[:5]

    if not sorted_users:
        await update.message.reply_text("Никто ещё не мерял свою пусси 😿")
        return

    leaderboard = "🏆 Лидерборд Pussy:\n"
    for i, (uid, size) in enumerate(sorted_users, 1):
        try:
            user = await context.bot.get_chat(uid)
            name = user.username or user.first_name or f"ID {uid}"
        except:
            name = f"ID {uid}"
        leaderboard += f"{i}. @{name} — {size} см\n"

    await update.message.reply_text(leaderboard)

app = ApplicationBuilder().token("8072641179:AAGo6JWW9Ivm9z6T2uppIxeWTGv7cHqMMyo").build()
app.add_handler(CommandHandler("pussy", pussy))
app.add_handler(CommandHandler("top", top))
app.run_polling()
