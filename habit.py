import db
from datetime import datetime


class Habit:
    def __init__(self, name=None, description=None, periodicity=None, category=None, database="habit_tracker.db"):

        """ Initialize a Habit object with the provided parameters.
               Parameters:
               - name (str): The name of the habit.
               - description (str): The description of the habit.
               - periodicity (str): The periodicity of the habit (e.g., daily, weekly).
               - category (str): The category to which the habit belongs.
               - database (str): The name of the SQLite database.
               """

        self.name = name
        self.description= description
        self.periodicity = periodicity
        self.category = category
        self.db = db.connect_database()
        self.streak = 0
        self.current_time = datetime.now()

    def add(self):
        """ Add a new habit to the database.
        If the habit already exists, print a message indicating so. """

        if not db.check_habit_exists(self.db, self.name):
            db.add_habit(self.db, self.name, self.description,self.periodicity, self.category, self.current_time, self.streak)
            print(f"\nHabit '{self.name.capitalize()}' added successfully.\n")
        else:
            print("\nHabit already exists, please choose another name.\n")

    def remove(self):
        """Remove the habit from the database.
        If the habit does not exist, print a message indicating so."""

        if db.check_habit_exists(self.db, self.name):
            db.delete_habit(self.db, self.name)
            print(f"\nHabit '{self.name.capitalize()}' removed successfully.\n")
        else:
            print("\nHabit not found, please check the name.\n")

    def update(self, new_name, new_description, new_periodicity, new_category):
        """     Update the habit's information in the database.
                If the habit does not exist, print a message indicating so."""

        if db.check_habit_exists(self.db, self.name):
            db.update_habit(self.db, self.name, new_name, new_description, new_periodicity, new_category)
            self.name = new_name
            self.periodicity = new_periodicity
            self.category = new_category
            print(f"\nHabit '{new_name.capitalize()}' updated successfully.\n")
        else:
            print("\nHabit not found, please check the name.\n")

    def increase_streak(self):
        """ Increase the streak count for the habit in the database. """

        current_streak = db.get_habit_streak_count(self.db, self.name)
        if current_streak is not None:
            current_streak += 1
        else:
            current_streak = 1  # Initialize to 1 if it's None
        db.increment_streak(self.db, self.name)
        print(f"\nStreak for habit '{self.name.capitalize()}' increased to {current_streak}.\n")

    def clear_streak(self):
        """ Reset the streak count for the habit in the database. """

        self.streak = 0
        db.reset_streak(self.db, self.name)
        print(f"\nStreak for habit '{self.name.capitalize()}' has been reset.\n")

    def modify_streak(self, new_streak):
        """ Modify the streak count for the habit in the database.
            If the input is not a valid integer, print a message indicating so."""

        try:
            new_streak = int(new_streak)
            db.update_habit_progress(self.db, self.name, new_streak)
            print(f"\nStreak for habit '{self.name.capitalize()}' has been updated to {new_streak}.\n")
        except ValueError:
            print(f"\nInvalid input. Streak for habit '{self.name.capitalize()}' remains unchanged.\n")

    def complete_habit(self):
        """Mark the habit as completed in the database and increase the streak."""

        db.mark_as_completed(self.db, self.name, self.current_time)
        self.increase_streak()
