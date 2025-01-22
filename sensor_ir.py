import numpy as np
from irobot_edu_sdk.music import Note
from time import sleep
import asyncio

class SensorIr:
    def __init__(self, nbre_total, robot):
        self.robot = robot
        self.nbre_total = nbre_total
        self.initSensorsValuesList()
        self.sensors = self.getSensors(robot)  # Initialisation synchrone 


    def initSensorsValuesList(self):
        """Initialise ou réinitialise les valeurs des capteurs."""
        self.IRValues = {i: [] for i in range(0, self.nbre_total)}  # Crée un dictionnaire avec des listes vides
        print("Valeurs des IR réinitialisées.")

    async def getSensors(self, robot):
        sensors = (await robot.get_ir_proximity())
        if sensors is not None:
            return sensors.sensors 
        else:
            return [0,0,0,0,0,0,0]

    async def agir(self, sensors, focus=3, recursive=True):
        if not sensors:  
            sensors = await self.getSensors(self.robot)
        print(sensors)
        for i in range(0, self.nbre_total):
            new_value = sensors[i]  
            self.IRValues[i].append(new_value)

        # Calculer la moyenne des trois dernières valeurs non nulles du capteur 'focus'
        if len(self.IRValues.get(focus-1, [])) >= 1: 
            mean = sensors[focus-1] #np.mean(non_zero_values_focus) if non_zero_values_focus else 0 

            print(f"Valeur du capteur {focus} : {mean}") 

            # Analyse des valeurs et actions
            if 0 <= mean < 10:
                print("Objet normalement très éloigné, l'infini.")
                return -2
            elif 10 <= mean < 80: #40
                print("Objet juste éloigné autour des 30 cm et plus.")
                return -1
            elif 80 <= mean <= 800 :
                print("L'objet entre en zone critique [15, 30] ; il faut opérer et traiter.")   
                return 0  
            elif 800 <= mean <= 2000 :
                print("L'objet entre en zone critique - 2e alerte ; il faut opérer et traiter.")   
                return 1
            else:
                print(f"Très critique pour ce capteur IR {focus}.")
                if focus == 3:  # Cas spécifique pour le capteur central
                    print("IR central, on doit s'arrêter.")
                    await self.robot.set_wheel_speeds(0, 0)  
                return 2
        else:
            print(f"Pas assez de données pour analyser le capteur {focus}.")
            return -4

    async def treat_zone_critique(self):
        angle = 30
        compteur = 0 
        output_code = 1 
        
        await self.robot.set_wheel_speeds(0, 0)  # Arrêt complet
        while(output_code==0 and compteur<360/angle):
            await self.robot.turn_left(angle)
            sensors = (await self.robot.get_ir_proximity()).sensors 
            output_code = await self.agir(sensors, recursive=False) 
            compteur = compteur+1
            print(f"Output du tour de 60°: {output_code}")
        return output_code