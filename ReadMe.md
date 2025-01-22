# Mobile Robot Create 3

This project demonstrates how to control the iRobot Create 3 robot using the [iRobot Python SDK](https://github.com/iRobotEducation/irobot-edu-python-sdk) via Bluetooth.

## Features

1. **Obstacle Avoidance (Évitement d'Obstacles)**

   - Implemented in the `mission` file.
   - The robot can detect and avoid obstacles by navigating around them in a rectangular pattern.

2. **Bumper Touch (Aller-Retour)**

   - Implemented in the `bumper_touch.py` file.
   - The robot moves back and forth, responding to bumper touch events.

3. **Custom Sensor Management**

   - A custom `SensorIr` class is used to manage the relationship between sensor states and obstacles.

4. **Autonomous Movement + Obstacle Detection**
   - Demonstrated in the `autonomous.py` file.
   - The robot moves autonomously while detecting and avoiding obstacles.

## Demo

You can watch the demo [here](https://youtu.be/NgfMsF4fDJk):

- **First Part**: Bumper Touch + Aller-Retour
- **Second Part**: Obstacle Avoidance with Rectangular Path Navigation

## Installation

1. Clone this repository:
   ```bash
   git clone <repository_url>
   ```
