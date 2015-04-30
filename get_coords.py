import serial

class KMLFile(object):
    def __init__(self):
        self.filename = 'test.kml'
        self.header = '''<?xml version="1.0" encoding="UTF-8"?>
                        <kml xmlns="http://www.opengis.net/kml/2.2">'''
        self.body = []
        self.footer = '</kml>'

    def addPlaceMarker(self,name,description,point):
        placemarker = "<Placemark>" +  \
                    "<name>" + name + "</name>" + \
                    "<description>" + description + "</description>" + \
                    "<Point><coordinates>" + str(point['lng']) + ', '  + str(point['lat']) + ', ' + str(point['alt']) + "</coordinates></Point>" + \
                    "</Placemark>"
        self.body.append(placemarker)

    def save(self):
        FILE = open(self.filename, 'w')
        FILE.write(self.header)
        for i in self.body:
            FILE.write(i)
        FILE.write(self.footer)
        FILE.close()

class IMU(object):
    def __init__(self):
        self.coordinates = []

    def parseGPS(self, data):
        gps_data = {}
        split_data = data.split(';')
        gps_data['lat'] = float(split_data[0])/10000000
        gps_data['lng'] = float(split_data[1])/10000000
        gps_data['alt'] = split_data[2]
        return gps_data

if __name__ == "__main__":
    imu = IMU()
    ser = serial.Serial('/dev/ttyUSB0', 38400)

    while True:
        try:
            buff = ser.readline()
            kmlfile = KMLFile()
            if buff[0] == '~': # means GPS coords
                data = imu.parseGPS(buff[1:-2])
                kmlfile.addPlaceMarker('','',data)
                kmlfile.save()
                #imu.coordinates.append((data['lat'],data['lng'],data['alt']))
                print(data['lat'], data['lng'])


        except KeyboardInterrupt:
            break
