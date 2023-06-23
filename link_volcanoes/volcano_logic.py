import numpy as np

def GetDist(lat1: float, lon1: float, lat2: float, lon2: float):
    degtorad = np.pi / 180
    phi1 = lat1 * degtorad
    phi2 = lat2 * degtorad
    delta_phi = (lat2-lat1) * degtorad
    delta_lambda = (lon2-lon1) * degtorad

    a = np.sin(delta_phi / 2) * np.sin(delta_phi / 2) + \
        np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) * np.sin(delta_lambda / 2)
    return 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

class CloseVolcano:
    
    def __init__(self, file_path: str, file_name: str):
        self.list = []
        
        file = open(file_path + file_name, 'r')
        text = file.readlines()
        file.close()
        
        for i in range(1, len(text)):
            words = text[i].split(',')
            self.list.append({'id': words[0], 
                              'name': words[1], 
                              'lat': float(words[2]), 
                              'lon': float(words[3])})
    
    def GetClose(self, cam_lat: float, cam_lon: float):
        ans = ('', 1000000)
        for volc in self.list:
            new_dist = GetDist(cam_lat, cam_lon, volc['lat'], volc['lon'])
            if ans[1] > new_dist:
                ans = (volc['name'], new_dist)
        return ans