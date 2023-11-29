from django.test import TestCase
from unittest.mock import patch, MagicMock
from tasks.models import Task
from tasks.management.commands.run_telegram_bot import start, tasks, help, handle_add, handle_description, bot, update_user_state, WAITING_FOR_DESCRIPTION, WAITING_FOR_CLASSROOM

class BotCommandsTestCase(TestCase):

    def setUp(self):
        self.chat_id = 12345
        self.message = MagicMock()
        self.message.chat.id = self.chat_id

    @patch.object(bot, 'send_message')
    def test_start_command(self, mock_send_message):
        self.message.text = '/start'
        start(self.message)
        mock_send_message.assert_called_with(self.chat_id, "Приветсвую коллега!\n\nИспользуй /help для просмотра всех команд")

    @patch.object(bot, 'send_message')
    @patch('tasks.management.commands.run_telegram_bot.update_user_state')
    def test_add_command(self, mock_update_user_state, mock_send_message):
        self.message.text = '/add'
        handle_add(self.message)
        mock_send_message.assert_called_with(self.chat_id, "Введите описание проблемы:")
        mock_update_user_state.assert_called_with(self.message, WAITING_FOR_DESCRIPTION)

    @patch('tasks.management.commands.run_telegram_bot.user_state', new_callable=dict)
    @patch.object(bot, 'send_message')
    @patch('tasks.management.commands.run_telegram_bot.update_user_state')
    def test_handle_description(self, mock_update_user_state, mock_send_message, mock_user_state):
        self.message.text = "Проблема с проектором"
        mock_user_state[self.chat_id] = WAITING_FOR_DESCRIPTION
        handle_description(self.message)
        mock_send_message.assert_called_with(self.chat_id, "Введите номер аудитории:")
        mock_update_user_state.assert_called_with(self.message, WAITING_FOR_CLASSROOM)
