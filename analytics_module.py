import db
from datetime import datetime


def get_all_tracked_habits(db_conn):
    """
        Retrieve a list of all tracked habits from the database.

        Parameters:
        - db_conn (sqlite3.Connection): The SQLite database connection.

        Returns:
        list: A list of habit names.
        """

    tracked_habits = db.get_habit_names(db_conn)
    return tracked_habits


def habits_by_periodicity(db_conn, periodicity):
    """
        Retrieve habits based on their periodicity from the database.

        Parameters:
        - db_conn (sqlite3.Connection): The SQLite database connection.
        - periodicity (str): The periodicity to filter habits (e.g., daily, weekly, monthly).

        Returns:
        list: A list of habits with the specified periodicity.
        """

    habits_periodicity = db.get_habits_with_periodicity(db_conn, periodicity)
    return habits_periodicity


def find_longest_streak_overall(db_conn):
    """
       Find the longest streak among all habits.

       Parameters:
       - db_conn (sqlite3.Connection): The SQLite database connection.

       Returns:
       int: The longest streak count.
       """

    cursor = db_conn.cursor()
    cursor.execute("SELECT MAX(streak) FROM habits")
    longest_streak = cursor.fetchone()
    return longest_streak[0] if longest_streak else 0


def find_longest_streak_for_habit(db_conn, habit_name):
    """
        Find the longest streak for a specific habit.

        Parameters:
        - db_conn (sqlite3.Connection): The SQLite database connection.
        - habit_name (str): The name of the habit.

        Returns:
        int: The longest streak count for the specified habit.
        """

    cursor = db_conn.cursor()
    cursor.execute("SELECT streak FROM habits WHERE name=?", (habit_name,))
    streak = cursor.fetchone()
    return streak[0] if streak else 0


def calculate_completion_rate(db_conn):
    """
        Calculate the completion rates for all habits.

        Parameters:
        - db_conn (sqlite3.Connection): The SQLite database connection.

        Returns:
        dict: A dictionary mapping habit names to their completion rates.
        """

    success_rates = {}
    cursor = db_conn.cursor()
    cursor.execute("SELECT name, periodicity, creation_time FROM habits")
    habits = cursor.fetchall()

    for habit in habits:
        habit_name, periodicity, creation_time_str = habit[0], habit[1], habit[2]

        # Convert creation_time to a datetime object
        creation_time = datetime.strptime(creation_time_str, "%Y-%m-%d %H:%M:%S.%f")

        # Calculate the date difference since the habit's creation
        date_diff = (datetime.now().date() - creation_time.date()).days

        # Calculate available days, weeks, and months as integers
        available_days = date_diff
        available_weeks = date_diff // 7
        available_months = date_diff // 30  # assume month 30 days

        # Check the periodicity and calculate the success rate
        if periodicity == 'daily' and available_days >= 1:
            cursor.execute(
                "SELECT COUNT(*) FROM habit_logs WHERE habit_id = (SELECT id FROM habits WHERE name=?)",
                (habit_name,))
            completed_count = cursor.fetchone()[0]

            success_rate = completed_count / available_days if available_days > 0 else 0
        elif periodicity == 'weekly' and available_weeks >= 1:
            cursor.execute(
                "SELECT COUNT(*) FROM habit_logs WHERE habit_id = (SELECT id FROM habits WHERE name=?)",
                (habit_name,))
            completed_count = cursor.fetchone()[0]

            success_rate = completed_count / available_weeks if available_weeks > 0 else 0
        elif periodicity == 'monthly' and available_months >= 1:
            cursor.execute(
                "SELECT COUNT(*) FROM habit_logs WHERE habit_id = (SELECT id FROM habits WHERE name=?) ",
                (habit_name,))
            completed_count = cursor.fetchone()[0]

            success_rate = completed_count / available_months if available_months > 0 else 0
        else:
            success_rate = 0  # For habits with insufficient time since creation

        success_rates[habit_name] = success_rate

    return success_rates


def find_habit_with_lowest_completion_rate(db_conn):
    """
        Find the habit with the lowest completion rate.

        Parameters:
        - db_conn (sqlite3.Connection): The SQLite database connection.

        Returns:
        tuple: A tuple containing the habit name and its lowest completion rate.
        """

    # Calculate success rates for all habits
    success_rates = calculate_completion_rate(db_conn)

    lowest_completion_rate = 1.0
    lowest_completion_habit = None

    for habit_name, success_rate in success_rates.items():
        if success_rate < lowest_completion_rate:
            lowest_completion_rate = success_rate
            lowest_completion_habit = habit_name

    return lowest_completion_habit, lowest_completion_rate


def identify_habits_needing_improvement(db_conn, completion_rate_threshold=0.7):
    """
        Identify habits needing improvement based on a completion rate threshold.

        Parameters:
        - db_conn (sqlite3.Connection): The SQLite database connection.
        - completion_rate_threshold (float): The threshold for identifying habits needing improvement.

        Returns:
        list: A list of tuples containing habit names and their completion rates needing improvement.
        """

    habits_needing_improvement = []

    # Calculate success rates for all habits
    success_rates = calculate_completion_rate(db_conn)

    # Check for habits needing improvement based on the completion rate threshold
    for habit_name, success_rate in success_rates.items():
        if success_rate < completion_rate_threshold:
            habits_needing_improvement.append((habit_name, success_rate))

    return habits_needing_improvement


