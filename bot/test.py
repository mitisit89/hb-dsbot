import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from bot.db import Q


class TestQ(unittest.TestCase):
    def setUp(self):
        # Создаем временную базу данных
        self.temp_dir = TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"
        self.q = Q(self.db_path)
        self.q.create_tables()

    def tearDown(self):
        # Удаляем временную базу данных
        self.temp_dir.cleanup()

    def test_add_user_hb_and_get_users(self):
        username = "test_user"
        birthday = datetime(1990, 1, 1)
        self.q.add_user_hb(username, birthday)

        users = self.q.get_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0][0], username)
        self.assertEqual(users[0][1], birthday.strftime("%Y-%m-%d %H:%M:%S"))

    def test_check_user_happy_birthday_is_exists(self):
        username = "test_user"
        birthday = datetime(1990, 1, 1)
        self.q.add_user_hb(username, birthday)

        exists = self.q.check_user_happy_birthday_is_exists(username)
        self.assertTrue(exists)

        not_exists = self.q.check_user_happy_birthday_is_exists("unknown_user")
        self.assertFalse(not_exists)

    def test_update_user_hb(self):
        username = "test_user"
        old_birthday = datetime(1990, 1, 1)
        new_birthday = datetime(1995, 5, 15)

        self.q.add_user_hb(username, old_birthday)
        self.q.update_user_hb(username, new_birthday)

        users = self.q.get_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0][1], new_birthday.strftime("%Y-%m-%d %H:%M:%S"))

    def test_add_user_hb_duplicate(self):
        username = "test_user"
