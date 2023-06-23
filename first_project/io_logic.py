from picamera import PiCamera
from sense_hat import SenseHat
from orbit import ISS
import numpy as np
from time import time
from time import sleep

# sense_hat is quite finicky with the magnometer readings so I let it read for a bit to get the real value
class MagnometerLogic:

    def __init__(self):
        self.sense = SenseHat()

    def Get(self):
        finalT = time() + 0.4
        while(time() < finalT):
            raw = self.sense.get_compass_raw()
        raw["abs"] = np.sqrt(raw["x"]*raw["x"] + raw["y"]*raw["y"] + raw["z"]*raw["z"])
        return raw

# General input class. Reads all relevant data.
class Reader:

    def __init__(self):
        self.magnetometer = MagnometerLogic()
 
    def Read(self):
        output = {}

        location = ISS.coordinates()
        output['location'] = (location.latitude.degrees, location.longitude.degrees)
        
        output['magnet'] = self.magnetometer.Get()
        
        output['time'] = time()

        return output

# I/O class. Saves a picture.
class Picture:

    def __init__(self, base_path, max_count):
        self.base_path = base_path
        self.max_count = max_count

        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        sleep(2)

        self.counter = {}
        self.values = {}

    def Save(self, location):
        
        if(location not in self.counter):
            self.counter[location] = 0
        
        name = self.base_path + location + '/image_' + str(self.counter[location]) + '.jpg'
        self.camera.capture(name)

        self.counter[location] += 1
        return str(self.counter[location] - 1)
    
    #save only photos with smallest criteria, and overwrite the rest
    def OverwriteMin(self, location, criteria):
        if(location not in self.values):
            self.values[location] = []
            for i in range(self.max_count):
                self.values[location].append(1000000000)
        crit = -1
        id = -1
        for i in range(self.max_count):
            if(crit < self.values[location][i]):
                crit = self.values[location][i]
                id = i

        if(crit > criteria):
            name = self.base_path + location + '/image_' + str(id) + '.jpg'
            self.camera.capture(name)
            self.values[location][id] = criteria
            return str(id)
        return ""
    
    #save only photos with biggest criteria, and overwrite the rest
    def OverwriteMax(self, location, criteria):
        if(location not in self.values):
            self.values[location] = []
            for i in range(self.max_count):
                self.values[location].append(-1)
        crit = 1000000000
        id = -1
        for i in range(self.max_count):
            if(crit > self.values[location][i]):
                crit = self.values[location][i]
                id = i

        if(crit < criteria):
            name = self.base_path + location + '/image_' + str(id) + '.jpg'
            self.camera.capture(name)
            self.values[location][id] = criteria
            return str(id)
        return ""