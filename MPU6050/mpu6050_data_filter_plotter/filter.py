
'''
# Created in 20170709 By YunShuiXin, this is some preprared work for a raspberry pi self-balancing robot.
# This filter moudle provides 1st-order and 2nd-order complimentary filter function to combine accelarometer and gyro data
  from mpu6050 to get euler angle(pitch and roll).
# order1_ratio represents the influence of the gyro data in 1st complimentary filter, 
  larger order1_ratio lead to smoother angle result due to the integral effect.
# order2_ratio represents the influence of the accelerometer data,  
  larger order2_ratio lead to quicker angle change reaction to the mpu6050, but also result in rougher angle-time curve.
'''

import math

class Complimentary_Filter:
    def __init__(self, order1_ratio=0.75, order2_ratio=0.2): 
        self.order1_ratio = order1_ratio
	self.order2_ratio = order2_ratio
        self.order1_pitch = 0.0 # angle around X axis
        self.order1_roll = 0.0 # angle around Y axis
	self.order2_pitch = 0.0 # angle around X axis
        self.order2_roll = 0.0 # angle around Y axis
        self.y_pitch=0.0
	self.y_roll=0.0
        return

    def combine_order1(self, dt, accel_data, gyro_data):
	
	# Turning around the X axis results in a vector on the Y-axis
        pitch_accel = math.atan2(accel_data[1], accel_data[2]) * 180 / math.pi
        # Turning around the Y axis results in a vector on the X-axis
        roll_accel = math.atan2(accel_data[0], accel_data[2]) * 180 / math.pi

        self.order1_pitch = (self.order1_pitch- gyro_data[2] * dt) * self.order1_ratio + pitch_accel * (1.0 - self.order1_ratio)
        self.order1_roll = (self.order1_roll- gyro_data[1] * dt)* self.order1_ratio + roll_accel * (1.0 - self.order1_ratio)
        return [pitch_accel, roll_accel, self.order1_pitch, self.order1_roll]

    def combine_order2(self, dt, accel_data, gyro_data):
	
	# Turning around the X axis results in a vector on the Y-axis
        pitch_accel = math.atan2(accel_data[1], accel_data[2]) * 180 / math.pi
        # Turning around the Y axis results in a vector on the X-axis
        roll_accel = math.atan2(accel_data[0], accel_data[2]) * 180 / math.pi

        x1=(pitch_accel-self.order2_pitch)*(1.0-self.order2_ratio)*(1.0-self.order2_ratio)
        self.y_pitch = self.y_pitch + x1*dt
        x2 = self.y_pitch + 2 * (1.0-self.order2_ratio) * (pitch_accel - self.order2_pitch) + gyro_data[2]
        self.order2_pitch = self.order2_pitch + x2*dt

	x1=(roll_accel-self.order2_roll)*(1.0-self.order2_ratio)*(1.0-self.order2_ratio)
        self.y_roll = self.y_roll + x1*dt
        x2 = self.y_roll + 2 * (1.0-self.order2_ratio) * (roll_accel - self.order2_roll) + gyro_data[1]
        self.order2_roll = self.order2_roll + x2*dt

        return [pitch_accel, roll_accel, self.order2_pitch, self.order2_roll]
