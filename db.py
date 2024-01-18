import sqlite3


def connect_database():
    """
        Connect to the SQLite database.

        Returns:
        sqlite3.Connection: The SQLite database connection.
        """
    conn = sqlite3.connect("habit_tracker.db")
    create_tables(conn)
    return conn


def create_tables(conn):
    """
        Initialize the database with the necessary tables.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.
        """
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            periodicity TEXT,
            category TEXT,
            creation_time DATETIME,
            streak INTEGER DEFAULT 0,
            completion_time DATETIME DEFAULT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY,
            habit_id INTEGER,
            completed BOOLEAN,
            completion_time DATETIME,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    ''')
    conn.commit()


def add_habit(conn, name, description, periodicity, category, creation_time, streak=0, completion_time=None):
    """
        Add a new habit to the database.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.
        - name (str): The name of the habit.
        - description (str): The description of the habit.
        - periodicity (str): The periodicity of the habit (e.g., daily, weekly).
        - category (str): The category of the habit.
        - creation_time (datetime): The creation time of the habit.
        - streak (int): The initial streak count (default is 0).
        - completion_time (datetime): The completion time of the habit (default is None).
        """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO habits (name, description, periodicity, category, creation_time, streak) VALUES (?, ?, ?, ?, ?, ?)',
                   (name, description, periodicity, category, creation_time, streak))
    conn.commit()


def delete_habit(conn, habit_name):
    """
        Delete a habit from the database.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.
        - habit_name (str): The name of the habit to be deleted.
        """
    cursor = conn.cursor()
    cursor.execute('DELETE FROM habits WHERE name=?', (habit_name,))
    cursor.execute('DELETE FROM habit_logs WHERE habit_id=(SELECT id FROM habits WHERE name=?)', (habit_name,))
    conn.commit()


def remove_all_habits(conn):
    """
            Delete all the habits from the database.

            Parameters:
            - conn (sqlite3.Connection): The SQLite database connection.
            """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habits")
    cursor.execute("DELETE FROM habit_logs")
    conn.commit()


def update_habit(conn, habit_name, name, description, periodicity, category):
    """
        Update the information of an existing habit in the database.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.
        - old_name (str): The current name of the habit.
        - new_name (str): The new name for the habit.
        - new_description (str): The new description for the habit.
        - new_periodicity (str): The new periodicity for the habit (e.g., daily, weekly).
        - new_category (str): The new category for the habit.
        """
    cursor = conn.cursor()
    cursor.execute('UPDATE habits SET name=?, description=?, periodicity=?, category=? WHERE name=?',
                   (name, description, periodicity, category, habit_name))
    conn.commit()


def increment_streak(conn, habit_name):
    """
        Increment the streak count of a habit in the database.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.
        - habit_name (str): The name of the habit.
        """
    cursor = conn.cursor()
    cursor.execute('UPDATE habits SET streak = streak + 1 WHERE name=?', (habit_name,))
    conn.commit()


def reset_streak(conn, habit_name):
    """
        Reset the streak count of a habit in the database.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.
        - habit_name (str): The name of the habit.
        """
    cursor = conn.cursor()
    cursor.execute('UPDATE habits SET streak = 0 WHERE name=?', (habit_name,))
    conn.commit()


def update_habit_progress(conn, habit_name, streak, completion_time=None):
    """
        Update the streak count of a habit in the database.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.
        - habit_name (str): The name of the habit.
        - streak (int): The new streak count for the habit.
        """
    cursor = conn.cursor()
    cursor.execute('UPDATE habits SET streak = ? WHERE name=?', (streak, habit_name))
    conn.commit()


def mark_as_completed(conn, habit_name, completion_time):
    """
        Mark a habit as completed in the database.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.
        - habit_name (str): The name of the habit.
        - completion_time (datetime): The completion time of the habit.
        """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO habit_logs (habit_id, completed, completion_time) VALUES ((SELECT id FROM habits WHERE name=?), ?, ?)',
                   (habit_name, 1, completion_time))
    conn.commit()


def check_habit_exists(conn, habit_name):
    """
        Check if a habit with the given name already exists in the database.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.
        - habit_name (str): The name of the habit.

        Returns:
        bool: True if the habit exists, False otherwise.
        """
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM habits WHERE name=?', (habit_name,))
    count = cursor.fetchone()[0]
    return count > 0


def get_habit_names(conn):
    """
        Retrieve names of all tracked habits from the database.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.

        Returns:
        list: A list of habit names.
        """
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM habits')
    habits = cursor.fetchall()
    return [habit[0] for habit in habits]


def get_habit_streak_count(conn, habit_name):
    """
        Retrieve the streak count of a specific habit from the database.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.
        - habit_name (str): The name of the habit.

        Returns:
        int: The streak count of the habit.
        """
    cursor = conn.cursor()
    cursor.execute('SELECT streak FROM habits WHERE name=?', (habit_name,))
    streak_count = cursor.fetchone()
    return streak_count[0] if streak_count is not None else None


def get_habits_with_periodicity(db_conn, periodicity):
    """
        Retrieve habits with a specific periodicity from the database.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.
        - periodicity (str): The periodicity to filter habits (e.g., daily, weekly, monthly).

        Returns:
        list: A list of habits with the specified periodicity.
        """
    cursor = db_conn.cursor()
    cursor.execute("SELECT name FROM habits WHERE periodicity = ?", (periodicity,))
    habits = cursor.fetchall()
    return [habit[0] for habit in habits]


def retrieve_habit_completion_time(conn, habit_name):
    """
        Retrieve the completion time of a specific habit from the database.

        Parameters:
        - conn (sqlite3.Connection): The SQLite database connection.
        - habit_name (str): The name of the habit.

        Returns:
        datetime: The completion time of the habit.
        """
    cursor = conn.cursor()
    cursor.execute('SELECT completion_time FROM habit_logs WHERE habit_id=(SELECT id FROM habits WHERE name=?)', (habit_name,))
    completion_time = cursor.fetchone()
    return completion_time[0] if completion_time is not None else None


def main():
    conn = connect_database()
    print("Connected to the habit tracker database.")


if __name__ == "__main__":
    main()
