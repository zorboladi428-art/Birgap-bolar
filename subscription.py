from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS

async def check_sub(bot, user_id):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

def sub_keyboard():
    kb = InlineKeyboardMarkup()
    for ch in CHANNELS:
        kb.add(
            InlineKeyboardButton(
                text="➕ Obuna bo‘lish",
                url=f"https://t.me/{ch[1:]}"
            )
        )
    kb.add(InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub"))
    return kb
