# 🚀 Ultimate Arcade Breakout

A game that is full of features and runs fast. Game is a **PyGame** breakout arcade game that has roguelike meta‑progression, dynamic difficulty scaling many power‑ups, random brick layouts and a lasting Gem economy!

---

## ✨ Features

- **🎮 Arcade Physics & Smooth 60 FPS Controls:**

Paddle bounces at angles when it hits the edge.

Balls bounce off each other in elastic 2D collisions.

Each brick break shows a particle explosion.

- **💎 Roguelike Meta-Progression & Gem Economy:**

All shop purchases reset after each run.

At the end of every run, permanent **Gems** are earned from Cash, Level and Difficulty multiplier.

**25 Permanent Gem Upgrades:** Use Gems to buy perks such as extra lives, laser starts, magnet paddles, score multipliers, compound interest and revive chances.

- **🚀 Advanced 5-Tier Laser System:**

**Base / Tier 0:** One laser shot, 0.5 second cooldown (`SPACE`).

**Tiers 1–3:** Cooldown drops to 0.4, 0.3 then 0.25 seconds.

**Tier 4:** Hold `SPACE` for auto-fire 0.1 cooldown.

**Tier 5:** Two twin lasers fire at the time from both paddle edges.

- **📊 Dynamic Difficulty System:**

**Easy:** Score of $5 gives $1 cash bricks take longer to lose HP shop items are cheaper power‑up drops are 50% higher. Gems are halved.

**Normal:** Score of $10 gives $1 cash, scaling and costs are normal and Gems are normal.

**Hard:** Score of $20 gives $1 cash shop costs are 1.5 times higher power‑up drops are as many and Gems double.

- **💾 In-Run Pause & Save System:**

Press `ESC` at any time to pause the game.

**Save & Quit** brings you back, to the title screen allowing the run to be resumed later.

When a new run starts a confirmation dialog appears to avoid overwrites.

- **🏆 Steam‑Style Achievements:**

Notifications slide in from the corner and show animated overlays.

A special Achievements Menu lists all achievements across 12 milestones.

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or newer must be installed on your system.

- The `pygame` library is required.

### Installation Steps

1. **Clone or download the repository:**

```bash

git clone [https://github.com/HELPIMINCAVE/breakout-arcade.git](https://github.com/HELPIMINCAVE/breakout-arcade.git)

cd breakout-arcade-pro

```

2. Install dependencies:

```bash

pip install -r requirements.txt

```

3. Run the game:

```bash

python3 main.py (or python main.py)

```

## 🕹️ Controls

| Action                                | Control             |
|---------------------------------------|:--------------------|
| **Move Paddle Left**                  | `Left Arrow` / `A`  |
| **Move Paddle Right**                 | `Right Arrow` / `D` |
| **Fire Lasers / Release Magnet Ball** | `SPACE`             |
| **Pause Menu**                        | `ESC`               |
| **Menu Interactions**                 | `Left Mouse Click`  |
