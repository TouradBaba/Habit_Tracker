import sqlite3
from habit import Habit
from analytics_module import *
import questionary as q

"""The CLI(Command Line Interface)"""

DB_NAME = "habit_tracker.db"
conn = sqlite3.connect(DB_NAME)


def connect_database(db_name="habit_tracker.db"):
    conn = sqlite3.connect(db_name)
    db.create_tables(conn)
    return conn


def show_all_habits_menu(db_conn):
    habits = db.get_habit_names(db_conn)
    if not habits:
        print("No habits found.")
    else:
        print("All Habits:")
        for habit in habits:
            print(habit)


def add_habit_menu():
    predefined_habits = [
        {"name": "Drink Water", "periodicity": "daily", "category": "Health", "description": "Stay hydrated."},
        {"name": "Read for 30 Minutes", "periodicity": "daily", "category": "Personal Development", "description":
            "Read to learn and grow."},
        {"name": "Exercise", "periodicity": "weekly", "category": "Health", "description": "Stay fit and healthy."},
        {"name": "Write a Journal Entry", "periodicity": "weekly", "category": "Personal Development", "description":
            "Reflect on your thoughts and experiences."},
        {"name": "Monthly Reflection", "periodicity": "monthly", "category": "Personal Development", "description":
            "Reflect on the month's achievements and areas for improvement."}
    ]

    while True:
        choices = ["Enter Custom Habit"]
        choices.extend([f"Choose '{habit['name']}' (Periodicity: {habit['periodicity']}, "
                        f"Category: {habit['category']}, Description: {habit['description']})"
                        for habit in predefined_habits])
        choices.append("Back")

        choice = q.select("Choose an option:", choices=choices).ask()

        if choice == "Back":
            break

        if choice == "Enter Custom Habit":
            name = q.text("Habit Name:").ask()

            # Check if the custom habit name is empty
            if not name.strip():
                print("Habit name cannot be empty. Please provide a valid name.")
                continue

            periodicity = q.select("Periodicity:", choices=["daily", "weekly", "monthly"]).ask()
            category = q.text("Category:").ask()
            description = q.text("Description:").ask()
        else:
            # Extract the actual habit name from the user's selection
            selected_habit_name = choice.split("Choose '")[1].split("'")[0]
            selected_habit = next(h for h in predefined_habits if h['name'] == selected_habit_name)
            name = selected_habit['name']
            periodicity = selected_habit['periodicity']
            category = selected_habit['category']
            description = selected_habit['description']

        # Create a new Habit and add it to the database
        new_habit = Habit(name, description, periodicity, category, "habit_tracker.db")
        new_habit.add()
        """new_habit.update(name, description, periodicity, category)"""


def remove_habit_menu():
    while True:
        choice = q.select("Choose an option:", choices=["Remove Single Habit", "Remove All Habits", "Back"]).ask()

        if choice == "Back":
            break

        if choice == "Remove Single Habit":
            name = q.text("Habit Name:").ask()
            habit = Habit(name, database="habit_tracker.db")
            habit.remove()
            print(f"Habit '{name}' removed successfully.")

        elif choice == "Remove All Habits":
            confirm = q.confirm("Are you sure you want to remove all habits?, Y for Yes and N for No").ask()
            if confirm:
                db_conn = db.connect_database()
                db.remove_all_habits(db_conn)
                print("All habits removed successfully.")
                db_conn.close()
            else:
                print("Operation canceled.")


def update_habit_menu():
    name = q.text("Habit Name:").ask()
    new_name = q.text("New Name: ").ask()

    # Check if the new name is empty
    if not new_name.strip():
        print("New name cannot be empty. Please provide a valid name.")
        return

    description = q.text("Description:").ask()
    periodicity = q.select("Periodicity:", choices=["daily", "weekly", "monthly"]).ask()
    category = q.text("Category:").ask()
    habit = Habit(name, database=DB_NAME)
    habit.update(new_name, description, periodicity, category)


def habit_streak_menu(db_conn):
    while True:
        streak_choice = q.select("Select a streak action:", choices=[
            "Complete Habit",
            "Increase Streak",
            "Clear Streak",
            "Modify Streak",
            "Back"
        ]).ask()

        if streak_choice == "Complete Habit":
            habit_name = q.text("Enter Habit Name:").ask()
            habit = Habit(habit_name, database=DB_NAME)  # Create a Habit object for the specified habit_name

            if db.check_habit_exists(db_conn, habit_name):
                cursor = db_conn.cursor()
                cursor.execute("SELECT id FROM habits WHERE name=?", (habit_name,))
                habit_id = cursor.fetchone()

                if habit_id:
                    habit_id = habit_id[0]
                    habit.complete_habit()  # Pass habit_id to the complete_habit method
                    print(f"\nHabit '{habit_name}' has been completed.\n")
                else:
                    print(f"Habit ID for '{habit_name}' not found.")
            else:
                print(f"Habit '{habit_name}' not found.")

        elif streak_choice == "Increase Streak":
            habit_name = q.text("Enter Habit Name:").ask()
            habit = Habit(habit_name, database=DB_NAME)  # Create a Habit object for the specified habit_name

            if db.check_habit_exists(db_conn, habit_name):
                habit.increase_streak()
            else:
                print(f"Habit '{habit_name}' not found.")
        elif streak_choice == "Clear Streak":
            habit_name = q.text("Enter Habit Name:").ask()
            habit = Habit(habit_name, database=DB_NAME)  # Create a Habit object for the specified habit_name

            if db.check_habit_exists(db_conn, habit_name):
                habit.clear_streak()
            else:
                print(f"Habit '{habit_name}' not found.")
        elif streak_choice == "Modify Streak":
            habit_name = q.text("Enter Habit Name:").ask()
            habit = Habit(habit_name, database=DB_NAME)  # Create a Habit object for the specified habit_name

            if db.check_habit_exists(db_conn, habit_name):
                new_streak_str = q.text("Enter New Streak Count:").ask()
                new_streak = None
                try:
                    new_streak = int(new_streak_str)
                except ValueError:
                    print("Please enter a valid integer for the new streak count.")
                habit.modify_streak(new_streak)
            else:
                print(f"Habit '{habit_name}' not found.")
        elif streak_choice == "Back":
            break


def analyze_habits_menu(db_conn):
    while True:
        analysis_choice = q.select("Select an analysis action:", choices=[
            "List Tracked Habits",
            "List Habits by Periodicity",
            "Longest Streak Overall",
            "Longest Streak for a Habit",
            "Habit with Lowest Completion Rate",
            "Habit Completion Rate",
            "Habits Needing Improvement",
            "Back"
        ]).ask()

        if  analysis_choice == "List Tracked Habits":
            tracked_habits = get_all_tracked_habits(db_conn)
            if tracked_habits:
                print("Currently Tracked Habits:")
                for habit in tracked_habits:
                    print(habit)
            else:
                print("No habits are currently being tracked.")

        elif analysis_choice == "List Habits by Periodicity":
            periodicity = q.text("Enter Periodicity (daily, weekly, monthly):").ask()
            matching_habits = habits_by_periodicity(db_conn, periodicity)
            if matching_habits:
                print(f"Habits with Periodicity '{periodicity}':")
                for habit in matching_habits:
                    print(habit)
            else:
                print(f"No habits found with Periodicity '{periodicity}'.")

        elif analysis_choice == "Longest Streak Overall":
            # Calculate and display the longest streak overall
            longest_streak = find_longest_streak_overall(db_conn)
            if longest_streak:
                print(f"Longest Streak Overall: {longest_streak}")
            else:
                print("No habits found, Add some habits")
        elif analysis_choice == "Longest Streak for a Habit":

            # Calculate and display the longest streak for a specific habit

            habit_name = q.text("Enter Habit Name:").ask()

            if db.check_habit_exists(db_conn, habit_name):

                streak = find_longest_streak_for_habit(db_conn, habit_name)

                print(f"Longest Streak for {habit_name}: {streak}")

            else:

                print(f"Habit '{habit_name}' not found.")

        elif analysis_choice == "Habit with Lowest Completion Rate":
            # Find and display the habit with the lowest completion rate
            habit_name, lowest_completion_rate = find_habit_with_lowest_completion_rate(db_conn)
            print(f"Habit with Lowest Completion Rate: {habit_name}, Completion Rate: {lowest_completion_rate:.2%}")

        elif analysis_choice == "Habit Completion Rate":
            # Calculate and display the success rate for all habits
            success_rates = calculate_completion_rate(db_conn)
            if success_rates:
                for habit, rate in success_rates.items():
                    print(f"Habit: {habit}, Success Rate: {rate:.2%}")
            else:
                print("No habits found, Add some habits")
        elif analysis_choice == "Habits Needing Improvement":
            # Find and display habits needing improvement
            habits_needing_improvement = identify_habits_needing_improvement(db_conn, completion_rate_threshold=0.7)
            if habits_needing_improvement:
                for habit, rate in habits_needing_improvement:
                    print(f"Habit: {habit}, Completion Rate: {rate:.2%}")
            else:
                print("No habits needs improvements")

        elif analysis_choice == "Back":
            break


def main_menu():
    conn = connect_database()  # Establish the database connection
    while True:
        choice = q.select("Select an action:", choices=[
            "Show All Habits",
            "Add Habit",
            "Remove Habit",
            "Update Habit",
            "Habit Streak",
            "Habit Analysis",
            "Exit"
        ]).ask()

        if choice == "Show All Habits":
            show_all_habits_menu(conn)
        elif choice == "Add Habit":
            add_habit_menu()
        elif choice == "Remove Habit":
            remove_habit_menu()
        elif choice == "Update Habit":
            update_habit_menu()
        elif choice == "Habit Streak":
            habit_streak_menu(conn)
        elif choice == "Habit Analysis":
            analyze_habits_menu(conn)
        elif choice == "Exit":
            break

    conn.close()


if __name__ == '__main__':
    main_menu()
