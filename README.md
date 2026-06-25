# 🚀 NOVA STRIKE — Advanced Space Shooter v2.0

Nova Strike is a fast-paced, action-packed 2D space shooter game built entirely from scratch using Python and Pygame. Instead of relying on ready-made game engines, this project focuses on custom game loops, vector-style rendering pipelines, and manual state tracking.

---

## 🎮 Key Features

### 🛠️ Core Gameplay & Systems
* **Player Spaceship & HUD:** Responsive movement and rotation tracking with a real-time Heads-Up Display showing lives, scores, and active weapons.
* **Dynamic Weapon Upgrades:** 3 levels of weapon evolution (Standard Laser ➡️ Plasma ➡️ Ion Cannon).
* **Power-up Drops:** Collectable items spawning at runtime, including Shields, Speed boosts, Triple Shots, and Nukes.

### 🧠 AI & Scaling
* **Predictive Enemy AI:** Enemy ships track player coordinates, calculating precise angles to chase and attack.
* **Procedural Obstacles:** Randomly spawning and scaled asteroids that add continuous difficulty.
* **Epic Boss Fights:** Encounter a massive boss ship every 5 levels, featuring 3 unique, cycling attack patterns.

### ✨ Visuals & Tactile Feedback ("Game Juice")
* **Neon Glow Effects:** Custom vector-style graphics using neon rendering utilities.
* **Particle Explosions:** Full particle-effect bursts triggered on every impact and destruction.
* **Screen Shake:** Dynamic viewport manipulation providing intense feedback on major collisions.
* **Animated Backdrop:** Multilayered parallax nebula background creating a smooth depth effect.

### 📊 Persistent Systems
* **Achievement System:** Tracks and unlocks 10 distinct in-game milestones.
* **Local Leaderboard:** File-handling mechanism implemented to save and persist high scores locally.

---

## 🕹️ Controls

| Key | Action |
| :--- | :--- |
| **W / A / S / D** or **Arrow Keys** | Move & Rotate Spaceship |
| **SPACEBAR** | Fire Main Weapon |
| **U** | Upgrade Weapon (Costs 200 Score Points) |
| **P** | Pause Game |
| **ESC** | Quit Game |

---

## 💻 How to Run Locally

### 1. Prerequisites
Make sure you have **Python 3.13** (or any stable Python 3.x version) installed on your machine.

### 2. Install Dependencies
Open your terminal inside the project directory and install the required library:
bash
pip install pygame
3. Launch the Game
Run the main game script using the following command:

Bash
python game_project.py
Tech Stack & Concepts Covered
Language: Python 3.13

Graphics/Audio Framework: Pygame

Concepts: Object-Oriented Programming (OOP), Custom Game Loops, State Management, Collision Matrices, File Handling (JSON/Txt for leaderboard data persistence).

