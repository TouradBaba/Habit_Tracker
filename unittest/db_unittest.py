import unittest
from datetime import datetime, timedelta
import db


class TestDatabaseModule(unittest.TestCase):
    def setUp(self):
        # Set up a temporary database for testing
        self.db_conn = db.connect_database()

    def tearDown(self):
        # Roll back changes to maintain a clean state after each test
        self.db_conn.rollback()
        # Close the database connection
        self.db_conn.close()

    def test_add_habit(self):
        # Test adding a habit to the database
        db.add_habit(self.db_conn, "Run", "Running daily", "daily", "Fitness", datetime.now(), 0)
        habit_exists = db.check_habit_exists(self.db_conn, "Run")
        self.assertTrue(habit_exists)

    def test_delete_habit(self):
        # Test deleting a habit from the database
        habit_name = "Run"

        # Check if the habit exists before trying to add it
        if not db.check_habit_exists(self.db_conn, habit_name):
            db.add_habit(self.db_conn, habit_name, "Running daily", "daily", "Fitness", datetime.now(), 0)

        # Now try to delete the habit
        db.delete_habit(self.db_conn, habit_name)

        # Check if the habit exists after deletion
        habit_exists_after_deletion = db.check_habit_exists(self.db_conn, habit_name)
        self.assertFalse(habit_exists_after_deletion)

    def test_update_habit(self):
        # Test updating a habit in the database
        unique_name = "Run_" + datetime.now().strftime("%Y%m%d%H%M%S%f")
        db.add_habit(self.db_conn, unique_name, "Running daily", "daily", "Fitness", datetime.now(), 0)
        db.update_habit(self.db_conn, unique_name, "Jog", "Jogging daily", "daily", "Fitness")
        updated_habit_name = db.get_habit_names(self.db_conn)[0]
        self.assertEqual(updated_habit_name, "Jog")

    def test_increment_streak(self):
        # Test incrementing the streak for a habit
        unique_name = "Run_" + datetime.now().strftime("%Y%m%d%H%M%S%f")
        db.add_habit(self.db_conn, unique_name, "Running daily", "daily", "Fitness", datetime.now(), 0)
        db.increment_streak(self.db_conn, unique_name)
        streak_count = db.get_habit_streak_count(self.db_conn, unique_name)
        self.assertEqual(streak_count, 1)

    def test_reset_streak(self):
        # Test resetting the streak for a habit
        unique_name = "Run_" + datetime.now().strftime("%Y%m%d%H%M%S%f")
        db.add_habit(self.db_conn, unique_name, "Running daily", "daily", "Fitness", datetime.now(), 3)
        db.reset_streak(self.db_conn, unique_name)
        streak_count = db.get_habit_streak_count(self.db_conn, unique_name)
        self.assertEqual(streak_count, 0)

    def test_update_habit_progress(self):
        # Test updating the progress (streak) for a habit
        unique_name = "Run_" + datetime.now().strftime("%Y%m%d%H%M%S%f")
        db.add_habit(self.db_conn, unique_name, "Running daily", "daily", "Fitness", datetime.now(), 0)
        db.update_habit_progress(self.db_conn, unique_name, 5)
        streak_count = db.get_habit_streak_count(self.db_conn, unique_name)
        self.assertEqual(streak_count, 5)

    def test_mark_as_completed(self):
        # Test marking a habit as completed
        unique_name = "Run_" + datetime.now().strftime("%Y%m%d%H%M%S%f")
        db.add_habit(self.db_conn, unique_name, "Running daily", "daily", "Fitness", datetime.now(), 0)
        completion_time = datetime.now() - timedelta(days=2)
        db.mark_as_completed(self.db_conn, unique_name, completion_time)
        habit_completion_time = db.retrieve_habit_completion_time(self.db_conn, unique_name)

        # Convert completion_time to the expected format
        expected_completion_time = completion_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        # Convert strings to datetime objects
        habit_completion_time = datetime.strptime(habit_completion_time, '%Y-%m-%d %H:%M:%S.%f')
        expected_completion_time = datetime.strptime(expected_completion_time, '%Y-%m-%d %H:%M:%S.%f')

        # Use assertAlmostEqual to compare datetime objects with a small delta
        self.assertAlmostEqual(habit_completion_time, expected_completion_time, delta=timedelta(milliseconds=1))

    def test_check_habit_exists(self):
        # Test checking if a habit exists in the database
        habit_name = "Run"
        habit_exists_before_adding = db.check_habit_exists(self.db_conn, habit_name)

        if not habit_exists_before_adding:
            db.add_habit(self.db_conn, habit_name, "Running daily", "daily", "Fitness", datetime.now(), 0)

        habit_exists_after_adding = db.check_habit_exists(self.db_conn, habit_name)
        self.assertTrue(habit_exists_after_adding)

    def test_get_habit_names(self):
        # Test getting the names of all habits in the database
        db.add_habit(self.db_conn, "Run", "Running daily", "daily", "Fitness", datetime.now(), 0)
        db.add_habit(self.db_conn, "Read", "Reading weekly", "weekly", "Hobby", datetime.now(), 0)
        habit_names = db.get_habit_names(self.db_conn)
        self.assertEqual(len(habit_names), 2)

    def test_get_habit_streak_count(self):
        # Test getting the streak count for a habit
        unique_name = "Run_" + datetime.now().strftime("%Y%m%d%H%M%S%f")
        db.add_habit(self.db_conn, unique_name, "Running daily", "daily", "Fitness", datetime.now(), 3)
        streak_count = db.get_habit_streak_count(self.db_conn, unique_name)
        self.assertEqual(streak_count, 3)


if __name__ == '__main__':
    unittest.main()
