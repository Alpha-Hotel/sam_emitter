import json
import time
import pymap3d as pm


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

    def track_target(self, pos_reps): 
        '''Change altitude + azimuth based on degrees from desired angle'''
        pos_reps = json.loads(pos_reps)
        pos_rep = [report for report in pos_reps if report["name"] == self.target][0]
        def double_angle_difference(angle1, angle2):
            diff = ( angle2 - angle1 + 180 ) % 360 - 180
            if (diff < -180):
                return (diff +360)
            else:
                return diff
        def feet_to_meters(feet):
            return feet/3.2808399
        if not self.target:
            desired_antenna_azimuth_degrees,desired_antenna_elevation_degrees, self.slant_range_to_target = pm.geodetic2aer(
                float(pos_rep[self.target]['latitude']), 
                float(pos_rep[self.target]['longitude']), 
                feet_to_meters(float(pos_rep[self.target]['altitude'])), 
                self.latitude, 
                self.longitude, 
                feet_to_meters(self.antenna_height)) #meters"

            ### changing antenna elevation
            difference= double_angle_difference(self.elevation_degrees, desired_antenna_elevation_degrees)
            if abs(desired_antenna_elevation_degrees-self.elevation_degrees) < 10: # changing antenna elevation
                self.elevation_degrees = desired_antenna_elevation_degrees
            else:
                if difference > 0:
                     self.elevation_degrees = self.elevation_degrees+self.slew_elevation_rate
                else:
                    self.elevation_degrees=self.elevation_degrees-self.slew_elevation_rate
            desired_antenna_azimuth_degrees = 273
            difference= double_angle_difference(self.azimuth_degrees, desired_antenna_azimuth_degrees)
            ### changing antenna azimuth
            if abs(difference) < 10: 
                self.azimuth_degrees = desired_antenna_azimuth_degrees
            else:
                if difference > 0:
                     self.azimuth_degrees = self.azimuth_degrees+self.slew_azimuth_rate
                else:
                    self.azimuth_degrees=self.azimuth_degrees-self.slew_azimuth_rate
                    if self.azimuth_degrees < 0:
                        self.azimuth_degrees+=360
            if abs(desired_antenna_elevation_degrees-self.elevation_degrees) < 10 and abs(desired_antenna_azimuth_degrees-self.azimuth_degrees) < 10:
                self.status="ready"
            else: 
                self.status="moving"
        else:
            self.status= "not ready"
            self.slant_range_to_target=0

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
