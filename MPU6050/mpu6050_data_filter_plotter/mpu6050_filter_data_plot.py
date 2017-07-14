
'''
# Created in 20170709 By YunShuiXin, this is some preprared work for a raspberry pi self-balancing robot.
# This moudle provides the fuction through which the euler angle(pitch,roll,directly caculated from acceleration sensor and
  filered by using 1st or 2nd complimentary filter) will be ploted with pyqtgraph.
# the delta_T is the sample time in milliseconds. During test, it is found that delta_T should not be larger than 25 
  milliseconds due to the limitation of the raspberry pi 3 B+ computation ablity.
'''

from pyqtgraph.Qt import QtGui, QtCore
from collections import deque
from filter import Complimentary_Filter as Filter
import pyqtgraph as pg
import math
import datetime
from mpu6050 import mpu6050

filter = Filter()
delta_T = 50
pen_width = 2
rad2deg = 180.0/math.pi
framenum = 200
x_label = range(0,framenum)
for i in range(framenum):
    x_label[i] *= delta_T
acce_pitch_deque = deque(maxlen=framenum)
acce_roll_deque = deque(maxlen=framenum)
order1_filter_pitch_deque = deque(maxlen=framenum)
order1_filter_roll_deque = deque(maxlen=framenum)
order2_filter_pitch_deque = deque(maxlen=framenum)
order2_filter_roll_deque = deque(maxlen=framenum)

sensor = mpu6050(0x68)

for i in xrange(framenum):
    acce_pitch_deque.append(0.0)
    acce_roll_deque.append(0.0)
    order1_filter_pitch_deque.append(0.0)
    order1_filter_roll_deque.append(0.0)
    order2_filter_pitch_deque.append(0.0)
    order2_filter_roll_deque.append(0.0)

win = pg.GraphicsWindow(title = "MPU6050 Plotter")
win.resize(1200,600)
win.setWindowTitle('MPU6050 Pitch and Roll Plotter')
pg.setConfigOptions(antialias = True)

def addplot(title_name,left_name,unit_name,bottom_name,Y_range_min,Y_range_max):
    subplot= win.addPlot(title = title_name)
    subplot.showGrid(x = True,y = True)
    subplot.setLabel('left', left_name, units = unit_name)
    subplot.setLabel('bottom', bottom_name)
    subplot.setYRange(Y_range_min,Y_range_max)
    return subplot

acce_pitch_plotter = addplot('Acce_Pitch_Plotter','Pitch','deg','time/ms',-180,180)
curve_acce_pitch = acce_pitch_plotter.plot(pen = pg.mkPen(color = (255,0,255),width = pen_width))
acce_roll_plotter = addplot('Acce_Roll_Plotter','Roll','deg','time/ms',-180,180)
curve_acce_roll = acce_roll_plotter.plot(pen = pg.mkPen(color = (0, 255, 127),width = pen_width))

win.nextRow()

order1_filter_pitch_plotter = addplot('1st-order-filter_Pitch_Plotter','Pitch','deg','time/ms',-180,180)
curve_order1_filter_pitch = order1_filter_pitch_plotter.plot(pen = pg.mkPen(color = (255,0,255),width = pen_width))
order1_filter_roll_plotter = addplot('1st-order-filter_Roll_Plotter','Roll','deg','time/ms',-180,180)
curve_order1_filter_roll = order1_filter_roll_plotter.plot(pen = pg.mkPen(color = (0, 255, 127),width = pen_width))

win.nextRow()

order2_filter_pitch_plotter = addplot('2nd-order-filter_Pitch_Plotter','Pitch','deg','time/ms',-180,180)
curve_order2_filter_pitch = order2_filter_pitch_plotter.plot(pen = pg.mkPen(color = (255,0,255),width = pen_width))
order2_filter_roll_plotter = addplot('2nd-order-filter_Roll_Plotter','Roll','deg','time/ms',-180,180)
curve_order2_filter_roll = order2_filter_roll_plotter.plot(pen = pg.mkPen(color = (0, 255, 127),width = pen_width))

def update():
    time1 = datetime.datetime.now()
    acce_data = [sensor.get_accel_data().get('x'),sensor.get_accel_data().get('y'),sensor.get_accel_data().get('z')]
    gyro_data = [sensor.get_gyro_data().get('x'),sensor.get_gyro_data().get('y'),sensor.get_gyro_data().get('z')]
    
    order1_filter_pitch_roll_data = filter.combine_order1(delta_T/1000.0, acce_data, gyro_data)
    order2_filter_pitch_roll_data = filter.combine_order2(delta_T/1000.0, acce_data, gyro_data)	

    acce_pitch_deque.append(order1_filter_pitch_roll_data[0])
    acce_roll_deque.append(order1_filter_pitch_roll_data[1])
    
    order1_filter_pitch_deque.append(order1_filter_pitch_roll_data[2])
    order1_filter_roll_deque.append(order1_filter_pitch_roll_data[3])
    
    order2_filter_pitch_deque.append(order2_filter_pitch_roll_data[2])
    order2_filter_roll_deque.append(order2_filter_pitch_roll_data[3])

    curve_acce_pitch.setData(x_label, list(acce_pitch_deque))
    curve_acce_roll.setData(x_label, list(acce_roll_deque))

    curve_order1_filter_pitch.setData(x_label, list(order1_filter_pitch_deque))
    curve_order1_filter_roll.setData(x_label, list(order1_filter_roll_deque))

    curve_order2_filter_pitch.setData(x_label, list(order2_filter_pitch_deque))
    curve_order2_filter_roll.setData(x_label, list(order2_filter_roll_deque))

    delta_time=datetime.datetime.now()-time1
    #print delta_time.microseconds/1000.0
    
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(delta_T) #take a sample every * ms

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()