"""
Доп - вспомогательные главной функции main в файле bot.py
"""
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

user_states = {}


def is_about_command(message):
    return message.text == "⚙️\nО программе"


def is_view_questions_command(message):
    return message.text == "📜\nПосмотреть вопросы"


def is_ask_question_command(message):
    return message.text == "📝\nЗадать вопрос"


def is_sent_donat(message):
    """Проверяем является ли сообщение командой "Донат"""
    return message.text == "💷\nДонат"


def is_speaker_selected(call):
    return bool(call.data)


def is_speaker_selected_state(message):
    tg_id = str(message.chat.id)
    user_state = user_states.get(tg_id)
    return user_state and user_state.get('state') == 'speaker_selected'


def create_reply_keyboard(role):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("⚙️\nО программе")
    btn_donats = KeyboardButton("💷\nДонат")

    if role == 'speaker':
        btn2 = KeyboardButton("📜\nПосмотреть вопросы")
        keyboard.add(btn1, btn2)
    else:
        btn2 = KeyboardButton("📝\nЗадать вопрос")
        keyboard.add(btn1, btn2, btn_donats)
    return keyboard


def create_inline_keyboard(speakers):
    keyboard = InlineKeyboardMarkup()
    for speaker in speakers:
        keyboard.add(
            InlineKeyboardButton(
                text=speaker.name, callback_data=speaker.tg_id
            )
        )
    return keyboard
