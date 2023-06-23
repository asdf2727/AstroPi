import shutil

def DataParse(file_path: str, file_name: str):
    snapshots = []
    found_mag = ['']
    found_vol = ['']
    
    source = ['general', 'magnetometer', 'volcanoes']
    
    picture_count = 0

    file = open(file_path + file_name, 'r')
    text = file.readlines()
    file.close()
    
    for i in range(len(text) - 1, 1, -1):
        words = text[i].split(',')
        words[12] = words[12].replace('\n', '')
        
        has_picture = 0
        if(words[10] != ""):
            has_picture = 1
        if(words[11] not in found_mag):
            found_mag.append(words[11])
            has_picture = 2
        if(words[12] not in found_mag):
            found_mag.append(words[12])
            has_picture = 3
        
        if (has_picture > 0):
            shutil.copy(file_path + source[has_picture - 1] + "/image_" + words[9 + has_picture] + ".jpg", 
                        file_path + "final/image_" + str(picture_count) + ".jpg", )
            picture_count += 1
        
        snapshots.append({'time': float(words[0]), 
                          'magnetometer': float(words[4]), 
                          'position': (float(words[5]), float(words[6])), 
                          'picture': (str(picture_count - 1) if has_picture > 0 else "")} )
    
    snapshots.reverse()
    return snapshots