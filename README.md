# Quidditch Tournament

## Overview
Quidditch Tournament is a Simulation App that allows you to create Quidditch teams with random skills and simulate a tournament.


## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/JonasEndriss/quidditch-tournament.git
    cd quidditch-tournament
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/Scripts/activate  # On Linux use `venv\bin\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Run the application:
    ```sh
    python src/main.py
    ```

2. The main window will open, allowing you to create and manage Quidditch teams.

## Project Structure
- `src/main.py`: Entry point of the application.

## Dependencies
- `ttkbootstrap`: Used for the application.
- `numpy`: Used for generating random skill values.
- `matplotlib`: Used for creating the plots that analyze the tournament.
- `seaborn`: Also used for the plots.
- `pandas`:  Also used for the plots.
- `tqdm`: Used to create a progress bars to show the progress of the tournament.
