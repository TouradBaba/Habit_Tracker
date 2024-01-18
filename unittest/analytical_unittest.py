import unittest
from analytics_module import *


class TestAnalyticalModule(unittest.TestCase):
    def setUp(self):
        self.db_conn = db.connect_database()
        db.create_tables(self.db_conn)

    def test_calculate_completion_rate(self):
        # Test calculating completion rates for habits
        db.add_habit(self.db_conn, "Exercise1", "Daily exercise", "daily", "Health", datetime.now(), 0)
        db.add_habit(self.db_conn, "Running", "Running daily", "daily", "Fitness", datetime.now(), 0)

        completion_rates = calculate_completion_rate(self.db_conn)
        self.assertEqual(completion_rates["Exercise1"], 0)
        self.assertEqual(completion_rates["Running"], 0)

        # Mark a habit as completed and test again
        db.mark_as_completed(self.db_conn, "Exercise1", datetime.now())
        completion_rates = calculate_completion_rate(self.db_conn)
        self.assertEqual(completion_rates["Exercise1"], 0)

    def test_find_habit_with_lowest_completion_rate(self):
        # Test finding the habit with the lowest completion rate
        db.add_habit(self.db_conn, "UniqueHabit1", "Daily exercise", "daily", "Health", datetime.now(), 0)

        # Add another habit with a completion rate greater than 0
        db.add_habit(self.db_conn, "UniqueHabit2", "Daily exercise", "daily", "Health", datetime.now(), 0)
        db.mark_as_completed(self.db_conn, "UniqueHabit2", datetime.now())

        lowest_habit, lowest_rate = find_habit_with_lowest_completion_rate(self.db_conn)
        self.assertEqual(lowest_habit, "Exercise1")
        self.assertEqual(lowest_rate, 0)

    def test_find_longest_streak_for_habit(self):
        # Test finding the longest streak for a specific habit
        db.add_habit(self.db_conn, "UniqueHabit3", "Daily exercise", "daily", "Health", datetime.now(), 5)

        longest_streak = find_longest_streak_for_habit(self.db_conn, "UniqueHabit3")
        self.assertEqual(longest_streak, 5)

    def test_find_longest_streak_overall(self):
        # Test finding the longest streak overall
        db.add_habit(self.db_conn, "UniqueHabit4", "Daily exercise", "daily", "Health", datetime.now(), 5)

        longest_streak = find_longest_streak_overall(self.db_conn)
        self.assertEqual(longest_streak, 5)

    def test_get_all_tracked_habits(self):
        # Test getting all tracked habits
        db.add_habit(self.db_conn, "UniqueHabit5", "Daily exercise", "daily", "Health", datetime.now(), 0)

        tracked_habits = get_all_tracked_habits(self.db_conn)
        self.assertEqual(len(tracked_habits), 7)

    def test_habits_by_periodicity(self):
        # Test getting habits by periodicity
        db.add_habit(self.db_conn, "UniqueHabit6", "Daily exercise", "daily", "Health", datetime.now(), 0)

        habits_daily = habits_by_periodicity(self.db_conn, "daily")
        self.assertIn("UniqueHabit6", habits_daily)

    def test_identify_habits_needing_improvement(self):
        # Test identifying habits needing improvement
        db.add_habit(self.db_conn, "UniqueHabit7", "Daily exercise", "daily", "Health", datetime.now(), 0)

        habits_needing_improvement = identify_habits_needing_improvement(self.db_conn)
        self.assertEqual(len(habits_needing_improvement), 9)


if __name__ == '__main__':
    unittest.main()
