from flask import Flask

app = Flask(__name__)

# import os
import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define the tricks and their associated difficulties
tricks = {
    'Invert': 4,
    'Climb': 2,
    'Fireman spin': 1,
    'Back hook spin': 3,
    'Chair spin': 1,
    'Cross knee release': 4,
    'Gemini': 5,
    'Superman': 7,
    'Iron X': 10,
    'Phoenix': 9,
    'Marion Amber': 9,
    'Aysha': 8,
    'Dew Drop': 1,
    'Knee Hold': 2,
    'Hip Hold': 3,
    'Pencil': 4,
    'Figurehead': 5,
    'Russian Layback': 6,
    'Gargoyle': 6
}

# Global variables
current_difficulty = 1
lower_bound = 1
upper_bound = 3
difficulty_window = 3
combo_mode = 'single'
num_tricks = 1
streak_counter = 0


@app.route('/', methods=['GET', 'POST'])
def home():
    global current_difficulty, lower_bound, upper_bound, difficulty_window, combo_mode, num_tricks, streak_counter

    if request.method == 'POST':
        if 'start_game' in request.form:
            current_difficulty = int(request.form['difficulty'])
            combo_mode = request.form['combo_mode']

            lower_bound = max(1, current_difficulty - 1)
            upper_bound = min(10, current_difficulty + 1)
            difficulty_window = 3
            streak_counter = 0

            if combo_mode == 'single':
                num_tricks = 1
            elif combo_mode == 'combo 2':
                num_tricks = 2
            elif combo_mode == 'combo 3':
                num_tricks = 3

            return redirect(url_for('game'))
    return render_template('home.html')


@app.route('/game', methods=['GET', 'POST'])
def game():
    global current_difficulty, lower_bound, upper_bound, difficulty_window, combo_mode, num_tricks, streak_counter

    valid_tricks = [t for t in tricks if lower_bound <= tricks[t] <= upper_bound]
    while len(valid_tricks) < num_tricks and upper_bound > 1:
        upper_bound -= 1
        valid_tricks = [t for t in tricks if lower_bound <= tricks[t] <= upper_bound]

    if len(valid_tricks) < num_tricks:
        return "Not enough tricks available even after adjusting the difficulty range. Exiting game."

    selected_tricks = random.sample(valid_tricks, num_tricks)

    if request.method == 'POST':
        if 'success' in request.form:
            successful = request.form['success'] == 'yes'
            if successful:
                streak_counter += 1
                if streak_counter == 3:
                    upper_bound = min(10, upper_bound + 1)
                    streak_counter = 0
            else:
                streak_counter = 0
                upper_bound = max(1, upper_bound - 1)

            lower_bound = max(1, upper_bound - difficulty_window + 1)
            upper_bound = min(10, lower_bound + difficulty_window - 1)

            if request.form['continue'] == 'no':
                return redirect(url_for('home'))
            return redirect(url_for('game'))

    return render_template('Game.html', tricks=selected_tricks)


if __name__ == '__main__':
    app.run(debug=True)
