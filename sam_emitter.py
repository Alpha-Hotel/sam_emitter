import json
import time
import pymap3d as pm
import geotool as gt


class Sam_Emitter():
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.azimuth_degrees= 0.0
        self.elevation_degrees = 00.0
        self.antenna_height =10
        self.target = ''
        self.latitude = latitude
        self.longitude = longitude
        self.speed =  0.
        self.heading= 0.
        self.slew_azimuth_rate = 10.0 #degrees per second
        self.slew_elevation_rate = 5.0
        self.status = 'not ready'
        self.threat = 'merciful_potato'
        self.slant_range_to_target = 0
        self.geo_data= []
        self.time_data=[]
        self.elevation_data=[]

    def track_target(self, pos_reps): 
        '''Change altitude + azimuth based on degrees from desired angle'''
        pos_reps = json.loads(pos_reps)
        try:
            pos_rep = [report for report in pos_reps if report["name"] == self.target][0]
        except IndexError:
            print('nothing to be tracked')
            self.range=0
            return


        if len(self.geo_data) == 5:
            self.geo_data.remove(self.geo_data[0])
            self.time_data.remove(self.time_data[0])
            self.elevation_data.remove(self.elevation_data[0])
            self.geo_data.append([pos_rep["lng"], pos_rep["lat"]])
            self.time_data.append([pos_rep['time']])
            self.elevation_data.append(pos_rep['alt'])
        else:
            self.geo_data.append([pos_rep["lng"], pos_rep["lat"]])
            self.time_data.append(pos_rep['time'])
            self.elevation_data.append(pos_rep['alt'])

        lat, lon, alt = gt.interpolate(self.geo_data, self.time_data, self.elevation_data)
        desired_antenna_azimuth_degrees, desired_antenna_elevation_degrees, self.slant_range_to_target = pm.geodetic2aer(
            float(lat), 
            float(lon), 
            alt/1000, 
            self.latitude, 
            self.longitude, 
            self.feet_to_meters(self.antenna_height)) #meters"
        print("moving to {} az, {} el".format(desired_antenna_azimuth_degrees, desired_antenna_elevation_degrees))
        ### changing antenna elevation
        difference = self.double_angle_difference(self.elevation_degrees, desired_antenna_elevation_degrees)
        if abs(desired_antenna_elevation_degrees - self.elevation_degrees) < 10: # changing antenna elevation
            self.elevation_degrees = desired_antenna_elevation_degrees
        else:
            if difference > 0:
                 self.elevation_degrees = self.elevation_degrees+self.slew_elevation_rate
            else:
                self.elevation_degrees=self.elevation_degrees - self.slew_elevation_rate

        difference = self.double_angle_difference(self.azimuth_degrees, desired_antenna_azimuth_degrees)
        ### changing antenna azimuth
        if abs(difference) < 10: 
            self.azimuth_degrees = desired_antenna_azimuth_degrees
        else:
            if difference > 0:
                 self.azimuth_degrees = self.azimuth_degrees+self.slew_azimuth_rate
            else:
                self.azimuth_degrees = self.azimuth_degrees-self.slew_azimuth_rate
                if self.azimuth_degrees < 0:
                    self.azimuth_degrees += 360
        if abs(desired_antenna_elevation_degrees-self.elevation_degrees) < 10 and abs(desired_antenna_azimuth_degrees-self.azimuth_degrees) < 10:
            self.status="ready"
        else: 
            self.status="moving"
        #else:
        #    self.status= "not ready"
        #    self.slant_range_to_target=0


    def double_angle_difference(self, angle1, angle2):
        diff = ( angle2 - angle1 + 180 ) % 360 - 180
        if (diff < -180):
            return (diff +360)
        else:
            return diff

    def feet_to_meters(self, feet):
        return feet/3.2808399

    def get_status(self):
        return {
            "sam_id" : self.name,
            "el": self.elevation_degrees,
            "az":self.azimuth_degrees,
            "status": self.status,
            "cur_threat":self.threat,
            "cur_target":self.target,
            "lat":self.latitude,
            "long":self.longitude,
            "heading":self.heading,
            "gnd_speed":self.speed,
            "range_to_target": self.slant_range_to_target
            }
    def change_target(self, sam_status):
        self.target = sam_status["cur_target"]
        self.threat = sam_status['cur_threat']
