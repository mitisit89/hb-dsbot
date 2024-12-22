import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from bot.db import Q


class TestQ(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"
        self.q = Q(self.db_path)
        self.q.create_tables()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_user_hb_and_get_user(self):
        username = "test_user"
        birthday = datetime(1990, 1, 1)
        self.q.add_user_hb(username, birthday)

        birthday_and_days = self.q.get_user_hb(username)
        self.assertEqual(len(birthday_and_days), 2)
        self.assertEqual(birthday_and_days[0], birthday.strftime("%d.%b"))

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

        users = self.q.get_user_hb(username)
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0], new_birthday.strftime("%d.%b"))

    def test_add_user_hb_duplicate(self):
        username = "test_user"
