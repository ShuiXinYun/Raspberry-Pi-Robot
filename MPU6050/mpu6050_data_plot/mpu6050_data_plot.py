from pyqtgraph.Qt import QtGui, QtCore
from collections import deque
import pyqtgraph as pg
import math
from mpu6050 import mpu6050


pen_width=2
rad2deg=180.0/math.pi
framenum=200
x_label=range(1,framenum+1)
acce_x_deque=deque(maxlen=framenum)
acce_y_deque=deque(maxlen=framenum)
acce_z_deque=deque(maxlen=framenum)
gyro_x_deque=deque(maxlen=framenum)
gyro_y_deque=deque(maxlen=framenum)
gyro_z_deque=deque(maxlen=framenum)

sensor = mpu6050(0x68)

for i in xrange(framenum):
    acce_x_deque.append(0.0)
    acce_y_deque.append(0.0)
    acce_z_deque.append(0.0)
    gyro_x_deque.append(0.0)
    gyro_y_deque.append(0.0)
    gyro_z_deque.append(0.0)

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1200,600)
win.setWindowTitle('MPU6050 Data Plotter')
pg.setConfigOptions(antialias=True)


def addplot(title_name,left_name,unit_name,bottom_name,Y_range_min,Y_range_max):
    subplot= win.addPlot(title=title_name)
    subplot.showGrid(x=True,y=True)
    subplot.setLabel('left', left_name, units=unit_name)
    subplot.setLabel('bottom', bottom_name)
    subplot.setYRange(Y_range_min,Y_range_max)
    return subplot

acce_x_plotter=addplot('Acce_X_Plotter','X Accel','m/(s^2)','FrameNum',-12,12)
curve_acce_x=acce_x_plotter.plot(pen=pg.mkPen(color=(255, 99, 71),width=pen_width))
acce_y_plotter=addplot('Acce_Y_Plotter','Y Accel','m/(s^2)','FrameNum',-12,12)
curve_acce_y=acce_y_plotter.plot(pen=pg.mkPen(color=(60, 179, 113),width=pen_width))
acce_z_plotter=addplot('Acce_Z_Plotter','Z Accel','m/(s^2)','FrameNum',-12,12)
curve_acce_z=acce_z_plotter.plot(pen=pg.mkPen(color=(30, 144, 255),width=pen_width))

win.nextRow()

gyro_x_plotter=addplot('Gyro_X_Plotter','X Angle Velo','deg/s','FrameNum',-200,200)
curve_gyro_x=gyro_x_plotter.plot(pen=pg.mkPen(color=(255, 0, 255),width=pen_width))
gyro_y_plotter=addplot('Gyro_Y_Plotter','Y Angle Velo','deg/s','FrameNum',-200,200)
curve_gyro_y=gyro_y_plotter.plot(pen=pg.mkPen(color=(0, 255, 127),width=pen_width))
gyro_z_plotter=addplot('Gyro_Z_Plotter','Z Angle Velo','deg/s','FrameNum',-200,200)
curve_gyro_z=gyro_z_plotter.plot(pen=pg.mkPen(color=(0, 245, 255),width=pen_width))

def update():
    acce_data=sensor.get_accel_data()
    gyro_data=sensor.get_gyro_data()

    acce_x_deque.append(acce_data.get('x'))
    acce_y_deque.append(acce_data.get('y'))
    acce_z_deque.append(acce_data.get('z'))
    
    gyro_x_deque.append(gyro_data.get('x'))
    gyro_y_deque.append(gyro_data.get('y'))
    gyro_z_deque.append(gyro_data.get('z'))

    curve_acce_x.setData(x_label, list(acce_x_deque))
    curve_acce_y.setData(x_label, list(acce_y_deque))
    curve_acce_z.setData(x_label, list(acce_z_deque))

    curve_gyro_x.setData(x_label, list(gyro_x_deque))
    curve_gyro_y.setData(x_label, list(gyro_y_deque))
    curve_gyro_z.setData(x_label, list(gyro_z_deque))

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100) 
'''
take a sample every * ms
'''
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()