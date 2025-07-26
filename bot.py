import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import logging
import os

# إعداد تسجيل الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# مفاتيح API - يُفضل استخدام متغيرات البيئة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8466485634:AAEaDpYw_ESPIfeuxDy3beJxM99Itwdj9hs")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDDb5mK-NT7djxwk93SXVEwTsVp6nWnDyk")

# تهيئة Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ذاكرة بسيطة للمستخدمين
user_memory = {}

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "هلا! 🙌\n"
        "أنـا چات عالسريع، بوت أجاوبك على أسئلتك ونسولف سوا إذا تحب.\n"
        "جرب تسألني أي شي بخاطرك، وأنا حاضر!\n\n"
        "🤖 من برمجة وتطوير: *Mohamed Ali*\n"
        "📬 للتواصل: [@R8d1k](https://t.me/R8d1k)"
    )
    await update.message.reply_markdown(welcome_message)

# رد شبابي باللهجة العراقية مع ذاكرة
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_input = update.message.text

    # استدعاء ذاكرة المستخدم
    history = user_memory.get(user_id, [])
    history.append({"role": "user", "parts": [user_input]})

    try:
        response = model.generate_content(history)
        reply = response.text.strip()

        # تحديث الذاكرة
        history.append({"role": "model", "parts": [reply]})
        user_memory[user_id] = history[-10:]  # نحفظ آخر 10 رسائل فقط

        # رد شبابي باللهجة العراقية
        if reply:
            final_reply = f"💬 {reply}"
        else:
            final_reply = "ماعرفت شجاوبك بصراحة، جرب تسألني شي ثاني؟ 😅"

    except Exception as e:
        final_reply = f"صار خلل بسيط: {e}"

    await update.message.reply_text(final_reply)

# تشغيل البوت
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ البوت شغال ويا ذاكرة وترحيب... سولف وياه على التلي.")
    app.run_polling()

if name == "main":
    main()
