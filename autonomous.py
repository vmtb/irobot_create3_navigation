from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth())

# Very basic example for avoiding front obstacles.

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth())
speed = 50
th = 50


async def forward(robot):
    await robot.set_lights_on_rgb(0, 255, 0)
    await robot.set_wheel_speeds(speed, speed)


async def backoff(robot):
    await robot.set_lights_on_rgb(255, 80, 0)
    await robot.move(-10)
    await robot.turn_left(30)


def front_obstacle(sensors):
    print(f"Sensors 2: {sensors[2]} - Sensors 3: {sensors[3]} - Sensors: 4 {sensors[4]}")
    return  sensors[2] > th or sensors[3] > th  or sensors[4] > th  


@event(robot.when_play)
async def play(robot):
    await forward(robot)
    while True:
        sensors = (await robot.get_ir_proximity()).sensors
        if front_obstacle(sensors):
            await backoff(robot)
            await forward(robot)

robot.play()