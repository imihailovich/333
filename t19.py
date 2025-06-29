import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from openai import OpenAI

API_TOKEN = '8036865757:AAF3hKAkpj_kExmlEktg4G2P09QTtShNvsc'  # <-- ВСТАВЬТЕ СВОЙ ТОКЕН
OPENAI_KEY = ""# <-- ВСТАВЬТЕ СВОЙ OpenAI API KEY

client = OpenAI(api_key=OPENAI_KEY)

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher()

user_gender_dictionary = {}
user_topic_dictionary = {}
user_post_number_dictionary = {}
user_post_length_dictionary = {}
user_state_dictionary = {}
user_tone_dictionary = {}
user_new_prompt_desc_dictionary = {}
user_topic1_dictionary = {}
user_cp_period_dictionary = {}
user_cp_frequency_dictionary = {}
user_cp_audience_dictionary = {}
user_cp_themes_dictionary = {}
user_cp_social_network_dictionary = {}
user_emoji_count_dictionary = {}

topic_list = [
    "Здоровое питание и диеты", "Психология и ментальное здоровье",
    "Личностный рост и саморазвитие", "Мода и стиль", "Красота и уход за собой",
    "Путешествия и тревел-блоги", "Финансовая грамотность и инвестиции",
    "Бизнес и предпринимательство", "Маркетинг и продвижение", "Образование и обучение",
    "Родительство и семейная жизнь", "Отношения и сексология", "Дом и уют, интерьер",
    "Кулинария и рецепты", "Искусство и креатив (фотография, живопись, музыка)",
    "Карьера и продуктивность", "Технологии и гаджеты", 
    "Развлечения: кино, сериалы, книги, юмор", "Другое"
]

post_types_list = [
    "Прямой продающий пост", "Продающий пост через полезный контент", "Продающий пост через историю",
    "Продающий пост через кейс", "Продающий пост через боль", "Продающий пост До и После",
    "Продающий пост через ограничение", "Контентный пост с логическим подходом",
    "Контентный пост с эмоциональным подходом", "Контентный пост через личную историю",
    "Экспертный разбор", "Пост-руководство", "Пост с приглашением на вебинар",
    "Пост, привязанный к определенному событию", "Пост-рекомендация", "Жизненный пост",
    "Пост-опрос для вовлечения аудитории", "Пост-вызов для аудитории", "Пост Мифы и реальность",
    "Пост Выбор правильного пути", "Пост-трансформация", "Интегрированный пост Ценность-Предложение",
    "Пост Вопрос-Ответ с продажей"
]

post_types_text = (
    "Выберите номер поста (вид):\n\n" +
    "\n".join([f"{str(i+1).zfill(2)}. {name}" for i, name in enumerate(post_types_list)])
)

topic_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=str(i)) for i in range(1, 7)],
        [KeyboardButton(text=str(i)) for i in range(7, 13)],
        [KeyboardButton(text=str(i)) for i in range(13, 19)],
        [KeyboardButton(text='19')],
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

post_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=str(i)) for i in range(1, 9)],
        [KeyboardButton(text=str(i)) for i in range(9, 17)],
        [KeyboardButton(text=str(i)) for i in range(17, 24)],
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

post_length_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Короткий (≈800 символов)")],
        [KeyboardButton(text="Обычный (≈2100)")],
        [KeyboardButton(text="Длинный (≈3200)")],
        [KeyboardButton(text="Своя длина")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

tone_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Обычно")],
        [KeyboardButton(text="Воодушевляюще")],
        [KeyboardButton(text="По-деловому")],
        [KeyboardButton(text="Иронично")],
        [KeyboardButton(text="Юмористически")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

emoji_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Без эмодзи")],
        [KeyboardButton(text="Оптимально")],
        [KeyboardButton(text="Много")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

workshop_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Генератор тем')],
        [KeyboardButton(text='Создание поста')],
        [KeyboardButton(text='Контент-план')],
        [KeyboardButton(text='Генерация изображения для поста')],
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True
)

period_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="неделя"), KeyboardButton(text="две недели")],
        [KeyboardButton(text="месяц"), KeyboardButton(text="квартал")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

frequency_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="часто"), KeyboardButton(text="оптимально"), KeyboardButton(text="редко")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

social_network_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Instagram"), KeyboardButton(text="ВКонтакте")],
        [KeyboardButton(text="Telegram"), KeyboardButton(text="Facebook")],
        [KeyboardButton(text="Другое")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

post_structures = {
    1: "Структура поста №1 ...",
    2: "Структура поста №2 ...",
    # ... остальные структуры ...
}

payment_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Оплата",
                url="https://yoomoney.ru/transfer/quickpay?requestId=353538383535313937345f36323564336264323063626561366164373762316662653636646430313239666561633163656433"
            )
        ]
    ]
)

# --- Клавиатура для диалога "Подробно"/"Назад" после генерации тем
details_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Подробно")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# ====== ФУНКЦИЯ ДЛЯ ОТПРАВКИ ДЛИННЫХ СООБЩЕНИЙ ======
async def send_long_message(message, text, reply_markup=None, max_length=4000):
    for i in range(0, len(text), max_length):
        part = text[i:i+max_length]
        if reply_markup and i + max_length >= len(text):
            await message.answer(part, parse_mode="HTML", reply_markup=reply_markup)
        else:
            await message.answer(part, parse_mode="HTML")
        await asyncio.sleep(0.1)

@dispatcher.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_gender_dictionary:
        await message.answer(
            "Пожалуйста, выберите ваш пол:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text='Мужчина'), KeyboardButton(text='Женщина')]],
                resize_keyboard=True
            )
        )
    else:
        await show_main_menu(message)

@dispatcher.message(lambda message: message.text in ["Мужчина", "Женщина"])
async def set_gender(message: types.Message):
    user_id = message.from_user.id
    user_gender_dictionary[user_id] = message.text.lower()
    user_state_dictionary[user_id] = "main_menu"
    await message.answer(
        "Спасибо! Пол сохранён.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await show_main_menu(message)

async def show_main_menu(message: types.Message):
    await message.answer(
        "Привет! Это наш бот. Тут дофига чего есть.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Мастерская')],
                [KeyboardButton(text='Поддержка'), KeyboardButton(text='Баланс')]
            ],
            resize_keyboard=True
        )
    )

@dispatcher.message(lambda message: message.text == "Мастерская")
async def workshop(message: types.Message):
    user_state_dictionary[message.from_user.id] = "workshop"
    await message.answer(
        "Мастерская — выберите действие:",
        reply_markup=workshop_keyboard
    )

# ====== Генератор тем ======
@dispatcher.message(lambda message: message.text == "Генератор тем")
async def topic_generator_start(message: types.Message):
    user_id = message.from_user.id
    user_state_dictionary[user_id] = "wait_new_prompt_desc"
    await message.answer(
        "Пожалуйста, опишите вашу аудиторию и задачу (это единственный обязательный параметр).\n\n"
        "<b>Описание аудитории и задачи</b>:",
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_new_prompt_desc")
async def topic_generator_desc(message: types.Message):
    user_id = message.from_user.id
    desc = message.text.strip()
    user_new_prompt_desc_dictionary[user_id] = desc
    user_state_dictionary[user_id] = "wait_topic1"
    topic_text = (
        "Выберите основную тему (topic1) для генерации идей:\n\n" +
        "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(topic_list)]) +
        "\n\nПожалуйста, выберите номер темы:"
    )
    await message.answer(topic_text, reply_markup=topic_keyboard)

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_topic1" and message.text in [str(i) for i in range(1, 19)])
async def topic1_chosen(message: types.Message):
    user_id = message.from_user.id
    topic_index = int(message.text) - 1
    user_topic1_dictionary[user_id] = topic_list[topic_index]
    await send_final_prompt_topic1(message)

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_topic1" and message.text == "19")
async def topic1_other(message: types.Message):
    user_id = message.from_user.id
    user_state_dictionary[user_id] = "wait_topic1_text"
    await message.answer(
        "Пожалуйста, введите тему (topic1) для генерации идей (любой текст):",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_topic1_text")
async def topic1_custom(message: types.Message):
    user_id = message.from_user.id
    user_topic1_dictionary[user_id] = message.text
    await send_final_prompt_topic1(message)

async def send_final_prompt_topic1(message: types.Message):
    import re
    user_id = message.from_user.id
    desc = user_new_prompt_desc_dictionary.get(user_id, "")
    topic1 = user_topic1_dictionary.get(user_id, "")
    user_state_dictionary[user_id] = "workshop"
    new_prompt = (
        f"Ты — креативный копирайтер. Я — специалист по теме \"{topic1}\".\n"
        f"<b>Описание аудитории и задачи</b>: {desc}\n"
        "Придумай 30 тем для постов, которые помогут мне рассказать моей целевой аудитории о своем проекте, услугах, опыте и ценностях.\n"
        "Каждая тема — отдельным пунктом, пронумеруй. К каждой теме добавь формат (например: сторис, пост, чек-лист, подкаст, видео и т.д.)"
    )

    await message.answer("<b>Генерирую темы, подождите...</b>", parse_mode="HTML")
    try:
        completion = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Генерируй идеи на русском языке, используй креатив и вариативность. Ответ только списком."},
                    {"role": "user", "content": new_prompt},
                ],
            )
        )
        result_text = completion.choices[0].message.content

        topics = re.findall(r'(?:^|\n)(\d{1,2})[.)\-]?\s*(.+)', result_text)
        sent_count = 0
        for num, text in topics:
            if 1 <= int(num) <= 30:
                await message.answer(f"<b>{num}.</b> {text.strip()}", parse_mode="HTML")
                sent_count += 1
                await asyncio.sleep(0.3)
        if sent_count < 15:
            lines = [line.strip() for line in result_text.split('\n') if line.strip()]
            n = 1
            for line in lines:
                if n > 30:
                    break
                await message.answer(f"<b>{n}.</b> {line}", parse_mode="HTML")
                n += 1
                await asyncio.sleep(0.2)
        await message.answer("Выберите дальнейшее действие:", reply_markup=details_keyboard)
        user_state_dictionary[user_id] = "wait_details_action"
    except Exception as e:
        await message.answer(f"<b>Ошибка генерации тем:</b> {e}", parse_mode="HTML", reply_markup=workshop_keyboard)

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_details_action" and message.text == "Подробно")
async def details_action(message: types.Message):
    user_id = message.from_user.id
    user_state_dictionary[user_id] = "wait_details_topic"
    await message.answer("Напишите тему, по которой нужен подробный пост (или скопируйте интересующую из списка выше):", reply_markup=types.ReplyKeyboardRemove())

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_details_action" and message.text == "Назад")
async def details_back(message: types.Message):
    user_id = message.from_user.id
    user_state_dictionary[user_id] = "workshop"
    await workshop(message)

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_details_topic")
async def details_generate(message: types.Message):
    user_id = message.from_user.id
    topic = message.text.strip()
    user_state_dictionary[user_id] = "workshop"
    prompt = f"Ты эксперт в области социальных сетей и построения личного бренда. Сделай отличный пост на тему - \"{topic}\""
    await message.answer("<b>Генерирую подробный пост...</b>", parse_mode="HTML")
    try:
        completion = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Пиши на русском, креативно и структурировано."},
                    {"role": "user", "content": prompt},
                ],
            )
        )
        result_text = completion.choices[0].message.content
        await send_long_message(message, result_text, reply_markup=workshop_keyboard)
    except Exception as e:
        await message.answer(f"<b>Ошибка генерации поста:</b> {e}", parse_mode="HTML", reply_markup=workshop_keyboard)

# ====== Ветка создания поста ======
@dispatcher.message(lambda message: message.text == "Создание поста")
async def start_create_post(message: types.Message):
    topic_text = (
        "Выберите тему для вашего поста:\n\n" +
        "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(topic_list)]) +
        "\n\nПожалуйста, выберите номер темы:"
    )
    user_state_dictionary[message.from_user.id] = "wait_topic"
    await message.answer(topic_text, reply_markup=topic_keyboard)

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_topic" and message.text in [str(i) for i in range(1, 19)])
async def topic_chosen(message: types.Message):
    user_id = message.from_user.id
    topic_index = int(message.text) - 1
    user_topic_dictionary[user_id] = topic_list[topic_index]
    user_state_dictionary[user_id] = "wait_post_type"
    await message.answer(post_types_text, reply_markup=post_type_keyboard)

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_topic" and message.text == "19")
async def topic_other(message: types.Message):
    user_id = message.from_user.id
    user_state_dictionary[user_id] = "wait_topic_text"
    await message.answer(
        "Пожалуйста, введите тему вашего поста (любой текст):",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_topic_text")
async def topic_custom(message: types.Message):
    user_id = message.from_user.id
    user_topic_dictionary[user_id] = message.text
    user_state_dictionary[user_id] = "wait_post_type"
    await message.answer(post_types_text, reply_markup=post_type_keyboard)

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_post_type" and message.text in [str(i) for i in range(1, 24)])
async def post_type_chosen(message: types.Message):
    user_id = message.from_user.id
    post_number = int(message.text)
    user_post_number_dictionary[user_id] = post_number
    user_state_dictionary[user_id] = "wait_post_length"
    await message.answer(
        "Выберите длину поста:",
        reply_markup=post_length_keyboard
    )

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_post_length" and "Короткий" in message.text)
async def post_length_short(message: types.Message):
    user_id = message.from_user.id
    user_post_length_dictionary[user_id] = "800"
    user_state_dictionary[user_id] = "wait_tone"
    await message.answer("Выберите тон написания поста:", reply_markup=tone_keyboard)

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_post_length" and "Обычный" in message.text)
async def post_length_normal(message: types.Message):
    user_id = message.from_user.id
    user_post_length_dictionary[user_id] = "2100"
    user_state_dictionary[user_id] = "wait_tone"
    await message.answer("Выберите тон написания поста:", reply_markup=tone_keyboard)

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_post_length" and "Длинный" in message.text)
async def post_length_long(message: types.Message):
    user_id = message.from_user.id
    user_post_length_dictionary[user_id] = "3200"
    user_state_dictionary[user_id] = "wait_tone"
    await message.answer("Выберите тон написания поста:", reply_markup=tone_keyboard)

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_post_length" and message.text == "Своя длина")
async def post_length_custom_prompt(message: types.Message):
    user_state_dictionary[message.from_user.id] = "wait_post_length_custom"
    await message.answer("Введите желаемую длину (только число):", reply_markup=types.ReplyKeyboardRemove())

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_post_length_custom" and message.text.isdigit())
async def post_length_custom(message: types.Message):
    user_id = message.from_user.id
    user_post_length_dictionary[user_id] = message.text
    user_state_dictionary[user_id] = "wait_tone"
    await message.answer("Выберите тон написания поста:", reply_markup=tone_keyboard)

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_tone" and message.text in [
    "Обычно", "Воодушевляюще", "По-деловому", "Иронично", "Юмористически"
])
async def tone_chosen(message: types.Message):
    user_id = message.from_user.id
    user_tone_dictionary[user_id] = message.text
    user_state_dictionary[user_id] = "wait_emoji_count"
    await message.answer(
        "Выберите количество эмодзи в посте:",
        reply_markup=emoji_keyboard
    )

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_emoji_count" and message.text in [
    "Без эмодзи", "Оптимально", "Много"
])
async def emoji_count_chosen(message: types.Message):
    user_id = message.from_user.id
    user_emoji_count_dictionary[user_id] = message.text
    await send_final_prompt(message)

async def send_final_prompt(message: types.Message):
    user_id = message.from_user.id
    user_state_dictionary[user_id] = "workshop"
    gender = user_gender_dictionary.get(user_id, "мужчина")
    topic = user_topic_dictionary.get(user_id, "тематика не указана")
    post_number = user_post_number_dictionary.get(user_id, 1)
    post_title = post_types_list[post_number - 1]
    post_length = user_post_length_dictionary.get(user_id, "2100")
    post_structure = post_structures.get(post_number, "Структура для этого типа поста еще не задана.")
    tone = user_tone_dictionary.get(user_id, "Обычно")
    emoji_count = user_emoji_count_dictionary.get(user_id, "Оптимально")
    prompt_text = (
        f"Ты — эксперт по digital-маркетингу и продвижению личного бренда в соцсетях.\n"
        f"Твоя задача — написать отличный пост для соцсетей для автора блогов по теме \"{topic}\", который уже ведёт аккаунт.\n"
        f"Тип поста: {post_title}\n"
        f"Пост должен быть создан по следующей структуре:\n{post_structure}\n"
        f"Длина поста около {post_length} символов.\n"
        f"Стиль написания: {tone}.\n"
        f"Пол автора: {gender}.\n"
        f"Количество эмодзи: {emoji_count}."
    )
    await message.answer("<b>Генерирую пост...</b>", parse_mode="HTML")
    try:
        completion = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Пиши на русском, креативно и структурировано."},
                    {"role": "user", "content": prompt_text},
                ],
            )
        )
        result_text = completion.choices[0].message.content
        await send_long_message(message, result_text, reply_markup=workshop_keyboard)
    except Exception as e:
        await message.answer(f"<b>Ошибка генерации поста:</b> {e}", parse_mode="HTML", reply_markup=workshop_keyboard)

# ====== Остальные ветки бота (контент-план, генерация изображения, поддержка, баланс и т.д.) ======

@dispatcher.message(lambda message: message.text == "Контент-план")
async def content_plan_period(message: types.Message):
    user_id = message.from_user.id
    user_state_dictionary[user_id] = "cp_period"
    await message.answer(
        "На какой период вы хотите создать контентплан?",
        reply_markup=period_keyboard
    )

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "cp_period" and message.text in ["неделя", "две недели", "месяц", "квартал"])
async def content_plan_frequency(message: types.Message):
    user_id = message.from_user.id
    user_cp_period_dictionary[user_id] = message.text
    user_state_dictionary[user_id] = "cp_frequency"
    await message.answer(
        "Какой частоты публикаций вы хотите придерживаться?",
        reply_markup=frequency_keyboard
    )

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "cp_frequency" and message.text in ["часто", "оптимально", "редко"])
async def content_plan_audience(message: types.Message):
    user_id = message.from_user.id
    user_cp_frequency_dictionary[user_id] = message.text
    user_state_dictionary[user_id] = "cp_audience"
    await message.answer(
        "Опишите вашу целевую аудиторию (например: женщины 30-45, предприниматели, мамы в декрете и т.д.):",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "cp_audience")
async def content_plan_themes(message: types.Message):
    user_id = message.from_user.id
    user_cp_audience_dictionary[user_id] = message.text
    user_state_dictionary[user_id] = "cp_themes"
    await message.answer(
        "Перечислите основные темы/рубрики, которые хотите включить в контентплан.\n\n"
        "Подсказка (вы можете копировать подходящие или придумать свои):\n\n"
        # ... (оставьте остальной подсказочный текст без изменений, как в вашей версии) ...
        "Добавьте несколько тем — их число зависит от выбранного вами периода планирования.",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "cp_themes")
async def content_plan_result(message: types.Message):
    user_id = message.from_user.id
    user_cp_themes_dictionary[user_id] = message.text

    period = user_cp_period_dictionary.get(user_id, "месяц")
    frequency = user_cp_frequency_dictionary.get(user_id, "оптимально")
    audience = user_cp_audience_dictionary.get(user_id, "")
    themes = user_cp_themes_dictionary.get(user_id, "")

    prompt_text = (
        f"Ты — дорогой копирайтер и контент-стратег. Тебе необходимо составить подробный контентплан для блога.\n"
        f"Параметры:\n"
        f"- Период планирования: <b>{period}</b>\n"
        f"- Периодичность публикаций: <b>{frequency}</b>\n"
        f"- Описание целевой аудитории: <b>{audience}</b>\n"
        f"- Основные рубрики и темы для публикаций:\n{themes}\n\n"
        "Распредели темы в соответствии с выбранным периодом и периодичностью. Для каждого дня/публикации предложи отдельную тему, формат и краткое описание.\n"
        "Удели внимание разнообразию форматов и вовлечению аудитории. "
        "Добавь call-to-action для каждой публикации, чтобы повысить активность и продажи."
    )

    user_state_dictionary[user_id] = "workshop"

    await message.answer("<b>Генерирую контент-план...</b>", parse_mode="HTML")
    try:
        completion = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Пиши на русском, креативно и структурировано."},
                    {"role": "user", "content": prompt_text},
                ],
            )
        )
        result_text = completion.choices[0].message.content
        await send_long_message(message, result_text, reply_markup=workshop_keyboard)
    except Exception as e:
        await message.answer(f"<b>Ошибка генерации контент-плана:</b> {e}", parse_mode="HTML", reply_markup=workshop_keyboard)

@dispatcher.message(lambda message: message.text == "Генерация изображения для поста")
async def image_generation_prompt(message: types.Message):
    user_id = message.from_user.id
    user_state_dictionary[user_id] = "wait_social_network"
    await message.answer(
        "Для какой социальной сети вы хотите сгенерировать изображение?",
        reply_markup=social_network_keyboard
    )

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_social_network" and message.text in [
    "Instagram", "ВКонтакте", "Telegram", "Facebook", "Другое"
])
async def image_generation_choose_network(message: types.Message):
    user_id = message.from_user.id
    user_state_dictionary[user_id] = "wait_image_desc"
    user_cp_social_network_dictionary[user_id] = message.text
    await message.answer(
        "Опишите, какое изображение вы хотите сгенерировать для поста (максимально подробно):",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "wait_image_desc")
async def image_generation_result(message: types.Message):
    user_id = message.from_user.id
    description = message.text.strip()
    social_network = user_cp_social_network_dictionary.get(user_id, "")
    user_state_dictionary[user_id] = "workshop"
    prompt_text = (
        "<b>Текст промта для генерации изображения:</b>\n\n"
        f"Социальная сеть: <b>{social_network}</b>\n"
        f"Описание изображения: {description}\n\n"
        "Сгенерируй яркое и привлекательное изображение для этой соцсети по этому описанию. "
        "Убедись, что изображение подходит для оформления поста."
    )
    await message.answer(
        prompt_text,
        parse_mode="HTML",
        reply_markup=workshop_keyboard
    )

@dispatcher.message(lambda message: message.text == "Назад")
async def go_back(message: types.Message):
    user_id = message.from_user.id
    state = user_state_dictionary.get(user_id, "")

    if state in ["workshop"]:
        user_state_dictionary[user_id] = "main_menu"
        await show_main_menu(message)
        return

    if state in [
        "wait_topic", "wait_topic_text", "wait_post_type", "wait_post_length",
        "wait_post_length_custom", "wait_tone", "wait_emoji_count",
        "wait_new_prompt_desc", "wait_topic1", "wait_topic1_text",
        "cp_period", "cp_frequency", "cp_audience", "cp_themes",
        "wait_social_network", "wait_image_desc"
    ]:
        user_state_dictionary[user_id] = "workshop"
        await workshop(message)
        return

    user_state_dictionary[user_id] = "main_menu"
    await show_main_menu(message)

SUPPORT_OWNER_ID = 493061725  # ID владельца аккаунта ТГ, которому будут приходить сообщения поддержки

@dispatcher.message(lambda message: message.text == "Поддержка")
async def support_start(message: types.Message):
    user_state_dictionary[message.from_user.id] = "support_waiting"
    await message.answer(
        "Сюда можете направить Ваши пожелания, предложения или вопросы.",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dispatcher.message(lambda message: user_state_dictionary.get(message.from_user.id) == "support_waiting")
async def support_receive_message(message: types.Message):
    user_id = message.from_user.id
    await message.answer(
        "Ваше сообщение отправлено владельцу бота. Спасибо!",
        reply_markup=workshop_keyboard
    )
    user_state_dictionary[user_id] = "workshop"
    text_to_owner = (
        f"Новое сообщение в поддержку от пользователя @{message.from_user.username or message.from_user.id} (ID: {user_id}):\n\n"
        f"{message.text}"
    )
    try:
        await bot.send_message(SUPPORT_OWNER_ID, text_to_owner)
    except Exception as e:
        pass

@dispatcher.message(lambda message: message.text == "Баланс")
async def show_payment(message: types.Message):
    await message.answer(
        "Для оплаты нажмите кнопку ниже:",
        reply_markup=payment_keyboard
    )

async def main():
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())