from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, ADMIN_ID
from ai import ask_ai
from premium import is_premium, check_limit, give_premium
from subscription import check_sub, sub_keyboard

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if not await check_sub(bot, message.from_user.id):
        await message.answer(
            "Botdan foydalanish uchun obuna bo‘ling:",
            reply_markup=sub_keyboard()
        )
        return

    await message.answer("🤖 AI botga xush kelibsiz!\nSavol yozing.")

@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def check_subscription(callback: types.CallbackQuery):
    if await check_sub(bot, callback.from_user.id):
        await callback.message.edit_text("✅ Obuna tasdiqlandi. Savol yozing.")
    else:
        await callback.answer("❌ Obuna topilmadi", show_alert=True)

@dp.message_handler(commands=["premium"])
async def premium_info(message: types.Message):
    text = (
        "💎 PREMIUM\n\n"
        "30 kun — 50 000 so‘m\n\n"
        "To‘lov:\n"
        "8600 **** **** ****\n\n"
        "Chekni yuboring.\n"
        "Admin captionga USER ID yozadi."
    )
    await message.answer(text)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def confirm_payment(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    if not message.caption or not message.caption.isdigit():
        await message.answer("Captionga user_id yoz.")
        return

    user_id = int(message.caption)
    give_premium(user_id)
    await bot.send_message(user_id, "✅ Premium 30 kunga faollashtirildi")

@dp.message_handler()
async def chat(message: types.Message):
    user_id = message.from_user.id

    if not await check_sub(bot, user_id):
        await start(message)
        return

    if not is_premium(user_id):
        if not check_limit(user_id):
            await message.answer("❌ Limit tugadi. /premium")
            return

    answer = ask_ai(message.text)
    await message.answer(answer)

if __name__ == "__main__":
    executor.start_polling(dp)
