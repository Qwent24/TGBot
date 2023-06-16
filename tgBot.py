import os
import logging
from pytube import YouTube
from moviepy.editor import VideoFileClip

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import Update

# Встановлення рівня журналювання
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Функція для початку роботи з ботом
def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привіт! Я готовий обробляти твої посилання на відео з YouTube.")

# Функція для обробки вхідних повідомлень
def handle_video_link(update: Update, context):
    video_link = update.message.text
    try:
        # Завантаження відео з YouTube
        youtube = YouTube(video_link)
        video = youtube.streams.first()
        video.download('./temp', filename='video.mp4')

        # Конвертація відео в MP3
        video_path = os.path.join('./temp', 'video.mp4')
        audio_path = os.path.join('./temp', 'audio.mp3')
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path)
        audio_clip.close()
        video_clip.close()

        # Відправлення аудіофайлу користувачу
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio_path, 'rb'))

        # Видалення тимчасових файлів
        os.remove(video_path)
        os.remove(audio_path)
    except Exception as e:
        logger.error(f"Error processing video link: {str(e)}")

# Головна функція
def main():
    # Ініціалізація токену та створення об'єктів Updater та Dispatcher
    updater = Updater(token='6225838049:AAFrqB1euLc-j4zvARZ8u3V2KqCphpLWeLk', use_context=True)
    dispatcher = updater.dispatcher

    # Додавання обробників команд та повідомлень
    start_handler = CommandHandler('start', start)
    video_link_handler = MessageHandler(None, handle_video_link)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(video_link_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
