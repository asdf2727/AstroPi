import shutil

def DataParse(file_path: str, file_name: str):
    snapshots = []

    file = open(file_path + file_name, 'r')
    text = file.readlines()
    file.close()
    
    for i in range(2, len(text)):
        words = text[i].split(',')
        snapshots.append({'time': float(words[0]), 
                          'magnetometer': float(words[1]), 
                          'position': (float(words[2]), float(words[3])), 
                          'picture': words[4]})
    
    return snapshots