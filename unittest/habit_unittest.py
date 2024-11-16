import unittest
from habit import Habit
import db


class TestHabitClass(unittest.TestCase):
    def setUp(self):
        # Create a test database and tables if needed
        self.db_conn = db.connect_database()
        db.create_tables(self.db_conn)

    def test_add_habit(self):
        habit = Habit(name="Exercise", description="Daily exercise", periodicity="daily", category="Health",
                      database="test_db.db")

        # Test adding a habit
        habit.add()
        self.assertTrue(db.check_habit_exists(self.db_conn, "Exercise"))

        # Test adding an existing habit (should print a message)
        habit.add()
        self.assertFalse(db.check_habit_exists(self.db_conn, "NonexistentHabit"))

    def test_modify_streak(self):
        habit = Habit(name="Exercise", database="test_db.db")

        # Test modifying streak for an existing habit
        habit.add()
        habit.modify_streak(new_streak="5")
        updated_streak = db.get_habit_streak_count(self.db_conn, "Exercise")
        self.assertEqual(updated_streak, 5)

        # Test modifying streak with invalid input
        habit.modify_streak(new_streak="invalid")
        unchanged_streak = db.get_habit_streak_count(self.db_conn, "Exercise")
        self.assertEqual(unchanged_streak, 5)

    def test_update_habit(self):
        habit = Habit(name="Exercise", description="Daily exercise", periodicity="daily", category="Health",
                      database="test_db.db")

        # Test updating an existing habit
        habit.add()
        habit.update(new_name="Running", new_description="Running daily", new_periodicity="weekly",
                     new_category="Fitness")
        updated_habit = db.get_habit_names(self.db_conn)
        self.assertIn("Running", updated_habit)

    def test_increase_streak(self):
        habit = Habit(name="Exercise", database="test_db.db")

        # Test increasing streak for an existing habit
        habit.add()
        initial_streak = db.get_habit_streak_count(self.db_conn, "Exercise")
        habit.increase_streak()
        updated_streak = db.get_habit_streak_count(self.db_conn, "Exercise")
        self.assertEqual(updated_streak, initial_streak + 1)

    def test_clear_streak(self):
        habit = Habit(name="Exercise", database="test_db.db")

        # Test clearing streak for an existing habit
        habit.add()
        habit.increase_streak()
        habit.clear_streak()
        updated_streak = db.get_habit_streak_count(self.db_conn, "Exercise")
        self.assertEqual(updated_streak, 0)

        # Test clearing streak for a non-existing habit
        habit.name = "Running"
        habit.clear_streak()

    def test_complete_habit(self):
        habit = Habit(name="Exercise", database="test_db.db")

        # Test completing a habit
        habit.add()
        habit.complete_habit()
        completion_time = db.retrieve_habit_completion_time(self.db_conn, "Exercise")
        self.assertIsNotNone(completion_time)

if __name__ == '__main__':
    unittest.main()
