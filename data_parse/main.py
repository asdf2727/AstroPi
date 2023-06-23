from pathlib import Path

from data_rearange import DataParse

def main():
    base_path = str(Path(__file__).parent.resolve()) + '/Data/'
    sorted_data = DataParse(base_path, "experiment.csv")
    
    file = open(base_path + 'data_sorted.csv', 'w')
    file.write("time,magnetometer,position,,picture\n")
    file.write("seconds,abs,latitude,longitude,id\n")

    for snapshot in sorted_data:
        file.write(str(snapshot["time"]) + ',')
        file.write(str(snapshot["magnetometer"]) + ',')
        file.write(str(snapshot["position"][0]) + ',' + str(snapshot["position"][1]) + ',')
        file.write(str(snapshot["picture"]) + ',')
        file.write('\n')

    file.close()
    return

if __name__ == '__main__':
    main()
