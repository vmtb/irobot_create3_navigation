
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
from time import sleep
from sensor_ir import SensorIr

robot = Create3(Bluetooth())
th = 500 

def print_pos(robot):
    print('🐢 (x  y  heading) =', robot.pose)
    
@event(robot.when_bumped, [True, True]) # Triggers when either bumper is depressed
async def bumped(robot):
    await robot.set_wheel_speeds(0, 0)
    await robot.move(-1) 

async def getSensors(robot):
    sensors = (await robot.get_ir_proximity())
    if sensors is not None:
        return sensors.sensors 
    else:
        return [0,0,0,0,0,0,0]

@event(robot.when_play)
async def play(robot):
    sr = SensorIr(7, robot)
    await robot.set_wheel_speeds(20, 20)

    
    while True: 

        # await robot.turn_left(180)  
     
        # await robot.play_note(Note.A5, .05)  #sonore 
        sensors = await getSensors(robot)
        output3 = await sr.agir(sensors, focus=3)  
        output0 = await sr.agir(sensors, focus=1)
        output6 = await sr.agir(sensors, focus=6) 
        print(f"o = {output0} -- o3 = {output3} -- o6 = {output6}") 

        if output3 == 0 or output3==1: # arrêt forcé; critique
            await robot.set_wheel_speeds(0, 0)
            #await robot.turn_left(20)
        else:
            await robot.set_wheel_speeds(20, 20)
        if output0 == 0 :
            await robot.turn_right(15)
        if output6 == 0: 
            await robot.turn_left(15)



        

robot.play()