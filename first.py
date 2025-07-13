import os
import datetime
import pytz
import threading
from playsound import playsound
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# === [ 사용자 설정 영역 ] ===
BOT_TOKEN = "7236566081:AAEqFrpt71pOr8SyTo_JRhXjCZGnOk3m0BY"
GROUP_CHAT_ID = -4977264361
TIMEZONE = pytz.timezone("Asia/Seoul")
LOG_DIR = "logs"
SOUND_FILE = "alert.mp3"  # 사운드 파일 (없으면 무음)
# ============================

received_message_ids = set()

def write_log(user, text):
    try:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        now = datetime.datetime.now(TIMEZONE)
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        log_path = os.path.join(LOG_DIR, f"log_{date_str}.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{time_str}] 메시지 수신 by {user}:\n{text}\n\n")
    except Exception as e:
        print("[오류] 로그 기록 실패:", e)

def play_sound():
    if SOUND_FILE and os.path.exists(SOUND_FILE):
        try:
            playsound(SOUND_FILE)
        except Exception as e:
            print("[경고] 사운드 재생 실패:", e)

async def handle_message(update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.effective_chat.id != GROUP_CHAT_ID:
            return

        msg_id = update.message.message_id
        if msg_id in received_message_ids:
            return
        received_message_ids.add(msg_id)

        sender = update.message.from_user.full_name
        text = update.message.text
        if not text:
            return

        # 콘솔 출력
        print(f"[수신] {sender} → {text}")

        # 사운드 알림 (비동기)
        threading.Thread(target=play_sound, daemon=True).start()

        # 로그 저장
        write_log(sender, text)

    except Exception as e:
        print("[오류] 메시지 처리 중 오류:", e)

if __name__ == "__main__":
    print("🚨 수신기 실행 중... 텔레그램 그룹 메시지를 대기합니다.")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.Chat(GROUP_CHAT_ID), handle_message))
    app.run_polling()
