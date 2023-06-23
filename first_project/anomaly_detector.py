import numpy as np

# general helper class with least squares method and the inverse of max difference over a window of time
class SlidingWindow:

    def __init__(self, duration):
        self.duration = duration
        self.points = {}

    def AddPoint(self, time, value):
        #remove old points
        for key in list(self.points.keys()):
            if key + self.duration < time:
                self.points.pop(key)
        #add the new one
        self.points[time] = value
    
    def GetDiff(self):
        #compute the biggest difference in the window
        minimum = 1000000000
        maximum = -1000000000
        for value in self.points.values():
            minimum = min(value, minimum)
            maximum = max(value, maximum)
        
        return abs(maximum - minimum)
    
    def GetSlope(self):
        #compute least squares
        sumxy = 0
        sumx = 0
        sumy = 0
        sumx2 = 0
        for point in self.points.items():
            sumxy += point[0] * point[1]
            sumx2 += point[0] * point[0]
            sumx += point[0]
            sumy += point[1]
        size = len(self.points)

        if (size * sumx2 == sumx * sumx):
            return 0
        else:
            return (size * sumxy - sumx * sumy) / (size * sumx2 - sumx * sumx)

# detects anomalies expected to have a duration in the order of self.sens seconds
# anomalies were considered where the first derivative changes most in a window of time
# this is because deviations too short are smoothed out and those too long don't have a big impact over the derivative
# is used to detect magnetic anomalies, setting the sensitivity as the time requiered for the station to pass ~400 km
class AnomalyDetector:

    def __init__(self):
        self.sens = 2*7.66/400
        self.smooth = 0
        self.lastT = -1
        self.firstD = SlidingWindow(400/7.66)
        self.window = SlidingWindow(400/7.66)

    def AddMeasurement(self, time, value):
        # applies exponential smoothing
        if(self.lastT < 0):
            self.smooth = value
            self.lastT = time
        else:
            param = np.exp(-self.sens * (time - self.lastT))
            self.smooth = param * self.smooth + (1 - param) * value
            self.lastT = time
        # use the smoothed funtion for the derivative calculation
        self.firstD.AddPoint(time, self.smooth)
        # here the slope for the last self.sens seconds is used as a derivative
        self.window.AddPoint(time, self.firstD.GetSlope())
    
    def GetLastValue(self):
        return self.smooth
    
    def GetAnomaly(self):
        return self.window.GetDiff()
