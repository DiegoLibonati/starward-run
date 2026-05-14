# Starward Run

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

## Description

**Starward Run** is a 2D side-scrolling runner game built in Python using the Pygame library. The player controls a space runner character that must survive an endless wave of incoming obstacles — snails crawling along the ground, bats swooping through the air, and fast-moving grounders that charge across the terrain. The goal is simple: stay alive as long as possible.

**Gameplay mechanics:**
- Move left and right with `A` and `D`, and jump with `SPACE` to dodge obstacles.
- Survival time is your score — every second you stay alive adds one point.
- As your score grows, new and faster obstacles are introduced, progressively increasing the difficulty.
- Obstacle movement speed scales with your score through defined thresholds, so the longer you survive, the harder it gets.

**Power-up system:**
- Mystery boxes spawn randomly on the map every 15 to 30 seconds.
- Walking into a mystery box grants one of two powers chosen at random:
  - **Immunity:** the next obstacle collision is completely negated — you pass through it unharmed.
  - **Killer:** the next obstacle you collide with is destroyed instead of ending your run, and a kill sound plays to confirm the elimination.
- Powers last 5 seconds. After the timer expires, the effect wears off and you return to normal.

**Progression:**
- Snails are available from the start.
- Bats unlock at score 10.
- Grounders unlock at score 20.
- Beyond score 200, obstacles reach their maximum speed of 30 pixels per frame.

**Game states:**
- The game opens on a waiting screen showing the title and your last score. Press `SPACE` to start or restart a run.
- A collision with an obstacle while unprotected ends the game immediately, plays the game-over music, and returns to the waiting screen.

**Technical highlights:**
- Built entirely with Pygame, structured around a sprite-group architecture with `GroupSingle` for the player and power, and `Group` for obstacles.
- Environment-aware configuration system supporting `development`, `production`, and `testing` modes via a `.env` file.
- PyInstaller-compatible asset resolution through a custom `resource_path()` helper, enabling distribution as a single standalone executable on Windows, Linux, and Mac.
- Comprehensive test suite covering configs, models, constants, helpers, and game logic, all running headless via SDL dummy drivers.

## Technologies used

1. Python >= 3.11

## Libraries used

#### Runtime (`[project.dependencies]`)

```
pygame==2.6.1
python-dotenv==1.2.2
```

#### Dev (`[project.optional-dependencies]` dev)

```
pre-commit==4.3.0
pip-audit==2.7.3
ruff==0.11.12
```

#### Test (`[project.optional-dependencies]` test)

```
pytest==9.0.3
pytest-env==1.1.5
pytest-cov==4.1.0
pytest-timeout==2.3.1
pytest-xdist==3.5.0
```

#### Build (`[project.optional-dependencies]` build)

```
pyinstaller==6.16.0
```

## Getting Started

With the stack in mind, follow these steps to set up a virtual environment, install the dependencies, and provide the required environment variables to run the game locally.

1. Clone the repository
2. Go to the repository folder and execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute in Linux/Mac: `source venv/bin/activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.dev.txt`
7. Execute: `pip install -r requirements.test.txt`
8. Copy `.env.example.dev` to `.env` so the application can load its configuration (see [Env Keys](#env-keys) for the available variables).
9. Use `python app.py` or `python -m src` to execute the program

### Pre-Commit for Development

1. Once you're inside the virtual environment, let's install the hooks specified in the pre-commit. Execute: `pre-commit install`
2. Now every time you try to commit, the pre-commit lint will run. If you want to do it manually, you can run the command: `pre-commit run --all-files`

## Env Keys

The `.env` file you copied during setup defines the runtime environment of the application. The following variables are recognized:

1. `ENVIRONMENT`: Defines the application environment. Accepts `development`, `production`, or `testing`.
2. `ENV_NAME`: A custom environment variable for template demonstration purposes.

```
ENVIRONMENT=development
ENV_NAME=your-app-name
```

## Testing

With the environment configured and dependencies installed, you can run the full test suite to verify the game logic.

1. Go to the repository folder
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute in Linux/Mac: `source venv/bin/activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.test.txt`
7. Execute: `pytest --log-cli-level=INFO`

## Security Audit

Beyond functional correctness, you should also verify that the project's dependencies do not contain known vulnerabilities. You can check them using **pip-audit**.

1. Go to the repository folder
2. Activate your virtual environment
3. Execute: `pip install -r requirements.dev.txt`
4. Execute: `pip-audit -r requirements.txt`

## Build

Once the project has been tested and audited, you can package it for distribution. You can generate a standalone executable (`.exe` on Windows, or binary on Linux/Mac) using **PyInstaller**.

### Windows

1. Go to the repository folder
2. Activate your virtual environment: `venv\Scripts\activate`
3. Install build dependencies: `pip install -r requirements.build.txt`
4. Create the executable: `pyinstaller app.spec`

Alternatively, you can run the helper script: `build.bat`

### Linux / Mac

1. Go to the repository folder
2. Activate your virtual environment: `source venv/bin/activate`
3. Install build dependencies: `pip install -r requirements.build.txt`
4. Create the executable: `pyinstaller app.spec`

Alternatively, you can run the helper script: `./build.sh`

## Known Issues

None at the moment.

## Portfolio link

[`https://www.diegolibonati.com.ar/#/project/starward-run`](https://www.diegolibonati.com.ar/#/project/starward-run)
