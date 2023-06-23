from time import time
from pathlib import Path

from io_logic import Reader, Picture
from anomaly_detector import AnomalyDetector
from volcano_logic import VolcanoSearch
from volcano_logic import SphereDistance

from picamera import PiCamera
from time import sleep

def main():
    durationT = 179 * 60

    initT = time()
    finalT = initT + durationT

    lastPicT = initT
    deltaT = 0.5
    deltaPicT = 20

    volcDist1 = 0
    volcDist2 = 0
    volcDist3 = 0

    base_path = str(Path(__file__).parent.resolve()) + '/Data/'

    print('reading volcano database...')
    volcanoes = VolcanoSearch(base_path + 'volcanoes.csv')
    reader = Reader()
    saver = Picture(base_path, 500)
    detector = AnomalyDetector()

    print('opening file...')
    file = open(base_path + 'experiment.csv', 'w')
    file.write("time,magnetometer,,,,position,,volcano,,,picture,,\n")
    file.write("seconds,x,y,z,abs,latitude,longitude,name,latitude,longitude,general,anomaly,volcanoes\n")

    readCount = 0
    nowT = time() + deltaT
    while(nowT < finalT):
        while(time() < nowT + deltaT):
            pass
        nowT = time()

        print('Run ' + str(readCount) + '...')
        readCount += 1

        data = reader.Read()
        file.write(str(data["time"]) + ',')
        file.write(str(data["magnet"]["x"]) + ',' + str(data["magnet"]["y"]) + ',' + 
                   str(data["magnet"]["z"]) + ',' + str(data["magnet"]["abs"]) + ',')
        file.write(str(data["location"][0]) + ',' + str(data["location"][1]) + ',')
        best_volcano = volcanoes.GetClose(data["location"])
        file.write(best_volcano["name"] + ',' + str(best_volcano["location"][0]) + ',' + str(best_volcano["location"][1]) + ',')

        # capture a picture every deltaPicT seconds
        if(lastPicT < data["time"]):
            lastPicT += deltaPicT
            file.write(saver.Save('general'))
        file.write(',')

        # capture a picture every anomaly
        detector.AddMeasurement(data["time"] - initT, data["magnet"]["abs"])
        if(data['time'] - initT > 120):
            file.write(saver.OverwriteMax('magnetometer', detector.GetAnomaly()))
        file.write(',')

        # capture a picture at every closest aproach
        volcDist3 = volcDist2
        volcDist2 = volcDist1
        volcDist1 = SphereDistance(data["location"], best_volcano["location"])
        if(readCount > 2 and volcDist2 <= volcDist1 and volcDist2 <= volcDist3):
            file.write(saver.OverwriteMin('volcanoes', volcDist2))
        file.write('\n')

    file.close()
    return

if __name__ == '__main__':
    main()
