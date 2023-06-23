import numpy as np

def SphereDistance(A, B):
    degToRad = np.pi / 180
    return np.arccos(np.cos(A[0] * degToRad) * np.cos(B[0] * degToRad) * np.cos((A[1] - B[1]) * degToRad) + 
                     np.sin(A[0] * degToRad) * np.sin(B[0] * degToRad)) / degToRad

class VolcanoSearch:

    def __init__(self, file_name):
        self.volcanoes = []

        file = open(file_name, 'r')
        text = file.readlines()
        file.close()
        for i in range(len(text)):
            words = text[i].split('\t')
            self.volcanoes.append({'name': words[0], 'location': (float(words[1]), float(words[2]))})
    
    def GetClose(self, position):
        min_dist = 1000000000
        min_id = -1
        for i in range(len(self.volcanoes)):
            new_dist = SphereDistance(self.volcanoes[i]['location'], position)
            if(min_dist > new_dist):
                min_dist = new_dist
                min_id = i
        return self.volcanoes[min_id]