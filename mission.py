import asyncio
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3
from time import sleep
from sensor_ir import SensorIr

robot = Create3(Bluetooth())




# Fonction de contournement
async def contourner(robot, sr: SensorIr, sens=1):
    print("Début du contournement")
    await robot.set_wheel_speeds(0, 0)
    sr.initSensorsValuesList()
    coef = 1 if sens == 1 else -1
    await robot.set_lights_on_rgb(255, 80, 0)

    # ← 
    await robot.turn_left(coef * 90)
    output6 = 0
    while output6 >= -1:
        await robot.set_wheel_speeds(20, 20)
        output6 = await sr.agir([], focus=7)
        print(f"out6 = {output6}")
    await robot.move(25)
    sleep(1)
    sr.initSensorsValuesList()

    # ↑
    await robot.turn_right(coef * 90)
    output6 = 0
    while output6 >= -1:
        await robot.set_wheel_speeds(20, 20)
        output6 = await sr.agir([], focus=7)
    await robot.move(25)
    await robot.set_wheel_speeds(0, 0)
    sleep(1)
    sr.initSensorsValuesList()

    # →
    output3 = -1
    await robot.turn_right(coef * 90)
    while output3 < 0:
        await robot.set_wheel_speeds(20, 20)
        output3 = await sr.agir([], focus=3)
    await robot.set_wheel_speeds(0, 0)
    sleep(1)
    await robot.turn_left(coef * 90)
    sr.initSensorsValuesList()

# Fonction de contournement
async def contourner_right(robot, sr: SensorIr, sens=1):
    print("Début du contournement")
    await robot.set_wheel_speeds(0, 0)
    sr.initSensorsValuesList()
    coef = 1 if sens == 1 else -1
    await robot.set_lights_on_rgb(255, 80, 0)

    # ← 
    await robot.turn_right(coef * 90)
    output6 = 0
    while output6 >= -1:
        await robot.set_wheel_speeds(20, 20)
        output6 = await sr.agir([], focus=1)
        print(f"out6 = {output6}")
    await robot.move(25)
    sleep(1)
    sr.initSensorsValuesList()

    # ↑
    await robot.turn_left(coef * 90)
    output6 = 0
    while output6 >= -1:
        await robot.set_wheel_speeds(20, 20)
        output6 = await sr.agir([], focus=1)
    await robot.move(25)
    await robot.set_wheel_speeds(0, 0)
    sleep(1)
    sr.initSensorsValuesList()

    # →
    output3 = -1
    await robot.turn_left(coef * 90)
    while output3 < 0:
        await robot.set_wheel_speeds(20, 20)
        output3 = await sr.agir([], focus=3)
    await robot.set_wheel_speeds(0, 0)
    sleep(1)
    await robot.turn_right(coef * 90)
    sr.initSensorsValuesList()

# Événement principal
@event(robot.when_play)
async def play(robot):
    sr = SensorIr(7, robot)
    await robot.set_wheel_speeds(20, 20) 
    compt =  0 
    while True: 
        output3 = await sr.agir([], focus=3)

        if output3 >= 0:  # Arrêt forcé, cas critique
            await robot.set_wheel_speeds(0, 0)
            await robot.move(14)
            if compt == 0: 
                await contourner(robot, sr, )
                compt = compt+1
            else:
                break
            
            sr.initSensorsValuesList()
        else:
            await robot.set_wheel_speeds(20, 20)
    
    await robot.move(-20)
    await robot.turn_left(180)
    compt = 0
    while True: 
        output3 = await sr.agir([], focus=3)

        if output3 >= 0:  # Arrêt forcé, cas critique
            await robot.set_wheel_speeds(0, 0)
            await robot.move(14.5)
            if compt == 0: 
                await contourner_right(robot, sr, )
                compt = compt+1
            else:
                break
            
            sr.initSensorsValuesList()
        else:
            await robot.set_wheel_speeds(20, 20)

robot.play()
