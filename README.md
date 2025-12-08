# Chess Game with AI & Multiplayer

A feature-rich Chess application built with Python and Pygame, offering single-player challenges against a Stockfish-integrated AI, local and network multiplayer, and puzzle solving modes.

## Repository
[https://github.com/Asandu178/ia4]

## Team & Contributions

*   **Argatu Ioan Dinu**:
    *   **GUI & Menu System:** Implemented the entire graphical user interface, including menus, buttons, and visual styling.
    *   **Networking:** Developed the client-server architecture for multiplayer support effectively.
    *   **Settings:** Created the preferences and settings management system.
*   **Scorei Dragos Alexandru**:
    *   **Game Backbone:** Implemented the core chess logic, including piece rules, board representation, and game state management.
    *   **Assets:** Handled the integration of board and piece assets.
    *   **Bot:** Implemented the Stockfish integration for AI opponent.

## Difficulties & Solutions

During the development, we encountered several challenges:

*   **Version Control & Merging:** We faced significant merge conflicts while pushing changes to Git.
    *   _Solution:_ We resolved this through better communication and careful conflict resolution during merges, ensuring no code was lost.
*   **Network Synchronization:** syncing game state across the server and clients was complex.
    *   _Solution:_ We implemented a robust protocol to send board states and move updates, ensuring all clients stay in sync.
*   **Bot Performance:** The bot gathered from Stockfish initially froze the UI while calculating moves.
    *   _Solution:_ We moved the bot's calculation logic to a separate **thread**, allowing the UI to remain responsive while the AI thinks.

## Features

### Game Modes
*   **Player vs Player (PvP):**
    *   **Local Play:** Play hotseat mode on the same machine.
    *   **Network Play:** Host or Join a game over LAN/IP.
        *   **Host:** Starts a server and waits for an opponent.
        *   **Join:** Connect to a host via IP address (default: `localhost`).
    *   **Time Controls:** Select from 1, 3, 5, 10 minutes, or Unlimited time configurations.
*   **Player vs Bot (PvB):**
    *   Challenge an AI powered by the Stockfish engine.
    *   **Difficulty Levels:**
        *   **Easy** (Depth 1)
        *   **Medium** (Depth 5)
        *   **Hard** (Depth 10)
        *   **Demon** (Depth 30 - Grandmaster level)
*   **Puzzle Mode:**
    *   Solve random chess puzzles loaded from FEN strings.
    *   Hints available after failed attempts.
    *   Instant feedback on correct/incorrect moves.

### Customization
*   **Preferences Menu:**
    *   **Board Themes:** Choose from various board styles (Classic, Gold, Wood, etc.).
    *   **Piece Themes:** Select different piece sets to suit your style.
    *   Settings are saved automatically.

## Languages & Technologies
*   **Python 3.12+**
*   **Pygame-CE** (Community Edition) for graphics and input.
*   **Stockfish** generic engine for AI opponent.
*   **Sockets** for network communication.
*   **Threading** for non-blocking AI execution.

## Installation & Usage

It is recommended to use a **virtual environment**.

### 1. Setup
bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


### 2. Running the Game
You can run the game using Python directly or use the provided `Makefile`.


**Using Makefile (Linux/WSL):**
bash
make run

This will open the **Main Menu**, where you can navigate to all game modes and settings.

## Project Structure

*   `src/` - Source code for the application.
    *   `main.py` - Entry point of the application.
    *   `menu/` - Menu logic (Main, PvP, PvB, Settings).
    *   `gui/` - Board rendering and game interfaces.
    *   `game/` - Core chess logic and state management.
    *   `board/` - Board representation and move generation.
    *   `pieces/` - Piece definitions.
    *   `network/` - Server and Client networking code.
*   `assets/` - Images for pieces, boards, and other resources.
*   `requirements.txt` - List of Python dependencies.

---
*Developed for IA4 Course.*