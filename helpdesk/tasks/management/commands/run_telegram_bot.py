from django.core.management.base import BaseCommand
import telebot

from telebot import types
from telebot.types import Message

from tasks.models import Task
bot = telebot.TeleBot('6849022542:AAHdr5PuAzzEuuNfoG09EoBNbXCB4rir6gk')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Приветсвую коллега!\n\nИспользуй /help для просмотра всех команд")

@bot.message_handler(commands=['tasks'])
def tasks(message):
    tasks = Task.objects.all()
    for task in tasks:
        task_message = f'#{task.id} {task.description} в {task.classroom} аудитории'
        bot.send_message(message.chat.id, task_message)


@bot.message_handler(commands=['help'])
def help(message):
    help_message_commands = "Команды \n\n/tasks - просмотр заявок\n/add - добавить заявку"
    bot.send_message(message.chat.id, help_message_commands)

# Определение состояний
WAITING_FOR_DESCRIPTION, WAITING_FOR_CLASSROOM = range(2)
user_state = {}

# Функция для получения текущего состояния пользователя
def get_user_state(message):
    return user_state.get(message.chat.id, None)

# Функция для обновления состояния пользователя
def update_user_state(message, state):
    user_state[message.chat.id] = state

# Обработчик для команды '/add'
@bot.message_handler(commands=['add'])
def handle_add(message):
    bot.send_message(message.chat.id, "Введите описание проблемы:")
    update_user_state(message, WAITING_FOR_DESCRIPTION)

# Обработчик для ввода описания
@bot.message_handler(func=lambda message: get_user_state(message) == WAITING_FOR_DESCRIPTION)
def handle_description(message):
    # Здесь можно сохранить описание во временное хранилище
    temp_storage[message.chat.id] = {'description': message.text}
    bot.send_message(message.chat.id, "Введите номер аудитории:")
    update_user_state(message, WAITING_FOR_CLASSROOM)

# Обработчик для ввода аудитории
@bot.message_handler(func=lambda message: get_user_state(message) == WAITING_FOR_CLASSROOM)
def handle_classroom(message):
    task_info = temp_storage.get(message.chat.id, {})
    task_info['classroom'] = message.text

    # Здесь создайте и сохраните объект задачи
    Task.objects.create(description=task_info['description'], classroom=task_info['classroom'])

    bot.send_message(message.chat.id, "Задача успешно добавлена, ожидайте!")
    update_user_state(message, None)  # Сбросить состояние

# Инициализация temp_storage
temp_storage = {}


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting bot...")
        bot.polling()
        print("Bot stopped")