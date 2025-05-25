# Top-Down Shooter Game

A simple top-down shooter game built with Pygame where you control a player that shoots bullets to destroy enemies.

## Features

- Player-controlled character that moves with arrow keys
- Enemies that spawn at the top of the screen with randomized side-to-side movement
- Shooting mechanics with spacebar
- Collision detection between bullets and enemies
- Score system (10 points per enemy destroyed)
- Game over when an enemy hits the player

## Controls

- **Arrow keys**: Move the player
- **Spacebar**: Shoot bullets
- **ESC**: Quit the game

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Make sure you have Python installed on your system
2. Install Pygame:

  ```pip install pygame```

3. Clone or download this repository

## How to Run

Navigate to the project directory and run:


```python3 main.py```

## Game Mechanics

- The player is represented by a blue square at the bottom of the screen
- Enemies (red squares) spawn at random positions at the top of the screen
- Enemies move downward with randomized side-to-side motion
- Shooting bullets destroys enemies and increases your score
- The game ends when an enemy collides with the player
- Your final score is displayed on the game over screen

## Future Enhancements

Potential features to add:
- Different enemy types
- Power-ups
- Multiple levels with increasing difficulty
- Sound effects and music
- High score system
