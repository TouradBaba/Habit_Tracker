# Habit Tracking Application

## Overview

The Habit Tracking Application is designed to help users manage and analyze their habits effectively. It provides a user-friendly interface for adding, updating, and analyzing habits, along with insightful analytics to track habit performance.

## Features

- **User-Friendly CLI:** An intuitive command-line interface for seamless habit management.
- **Dynamic Habit Tracking:** Add, remove, update, and analyze habits with flexibility.
- **Streak Management:** Complete habits, increase streaks, clear streaks, and modify streak counts.
- **Insightful Analytics:** Analyze habit completion rates and identify habits needing improvement.
- **Seamless Predefined Habits:** Easily integrate predefined habits into your routine through the CLI.

## Installation

1. Install Python
To install Python, click [here](https://www.python.org/downloads/).
Ensure that Python has been added to the system's PATH.
2. Install questionary, the tool used to build the CLI
you can use the following command
```bash
pip install questionary
```
3. Navigate to the project directory:
After downloading the files from the repository , create a folder and add them to it
4. Go to the CMD\Terminal "cd" to your folder, example shown below
```bash
cd  C:\users\user\folder
```
5. Run the application
Now you can run the application by using this command
```bash
python main.py
```

## Usage

The application provides a menu-driven interface for interacting with the Habit Tracking features. Follow the on-screen prompts to perform actions such as adding, updating, and analyzing habits.

## Habit Analysis

To access habit analysis features, select the "Habit Analysis" option from the main menu. This menu provides insights into habit statistics, including completion rates, longest streaks, and habits needing improvement.

## Predefined Habits

When adding a new habit, users have the option to choose from predefined habits. These habits cover daily, weekly, and monthly routines, offering a convenient way to get started with habit tracking.

## Exit
Select Exit on the main menu.

## Tests
To run tests add the files in the folder unittest to the same directory as other app files
to run each test after cd the directory you can use this command(replace the testname by the actual test name):
```bash
   python testname.py
   ```
After each test, it is recommended to delete all the habits from the app, as having existing habits may interfere with certain tests and produce inaccurate results.
