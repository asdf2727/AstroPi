from pathlib import Path

from io_logic import DataParse
from volcano_logic import CloseVolcano

def main():
    base_path = str(Path(__file__).parent.resolve()) + '/Data/'
    
    sorted_data = DataParse(base_path, "data_sorted.csv")
    volc_data = CloseVolcano(base_path, "volcanoes_mini.csv")
    
    file = open(base_path + 'data_linked.csv', 'w')
    file.write("time,magnetometer,position,,volcano,distance,coeficient,picture\n")
    file.write("seconds,abs,latitude,longitude,name,radians,value,id\n")

    for snapshot in sorted_data:
        file.write(str(snapshot["time"]) + ',')
        file.write(str(snapshot["magnetometer"]) + ',')
        file.write(str(snapshot["position"][0]) + ',' + str(snapshot["position"][1]) + ',')
        closest = volc_data.GetClose(snapshot["position"][0], snapshot["position"][1])
        file.write(closest[0] + ',' + str(closest[1]) + ',')
        coef = volc_data.GetCoef(snapshot["position"][0], snapshot["position"][1])
        file.write(str(coef) + ',')
        file.write(str(snapshot["picture"]) + ',')
        file.write('\n')

    file.close()
    return

if __name__ == '__main__':
    main()
