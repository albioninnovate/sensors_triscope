import time
import board
import busio
import adafruit_bno055
import json
import pprint
import datetime
from datetime import timezone

import serial


"""
reference; 
https://github.com/adafruit/Adafruit_CircuitPython_BNO055

"""

# Use these lines for I2C
def start_sensor():
    i2c = busio.I2C(board.SCL, board.SDA)

    print(i2c)

    sensor = adafruit_bno055.BNO055_I2C(i2c)

    print(sensor)


    return sensor

# User these lines for UART
#    uart = busio.UART(board.TX, board.RX)
#    sensor = adafruit_bno055.BNO055_UART(uart)


#    uart = serial.Serial("/dev/serial0")
#   sensor = adafruit_bno055.BNO055_UART(uart)
    #sensor = Adafruit_Python_BNO055.BNO055(uart)
#    sensor = BNO055.BNO055(serial_port='/dev/serial0', rst=18)



def read(sensor, verbose=False):
    """
    reads the values from the sensor into a dictonary.

    :param sensor:  instance of data source
    :param verbose: if True prints the resulting dictionary
    :return:
    """
    readings = {
        "temperature"           : sensor.temperature,
        "acceleration"          : sensor.acceleration,
        "magnetic"              : sensor.magnetic,
        "gyro"                  : sensor.gyro,
        "euler"                 : sensor.euler,
        "quaternion"            : sensor.quaternion,
        "linear_acceleration"   : sensor.linear_acceleration,
        "gravity"               : sensor.gravity

                }

    if verbose is True:
        #pprint(readings)
            print("Temperature: {} degrees C".format(sensor.temperature))
            print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
            print("Magnetometer (microteslas): {}".format(sensor.magnetic))
            print("Gyroscope (rad/sec): {}".format(sensor.gyro))
            print("Euler angle: {}".format(sensor.euler))
            print("Quaternion: {}".format(sensor.quaternion))
            print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
            print("Gravity (m/s^2): {}".format(sensor.gravity))
            print()

    return readings


def to_json(dict):
    return json.dumps(dict).encode('utf-8')


def main(output_format='dict',cnt=0):
    try:
        sensor
    
    except NameError:
        print('restartng sensor')
        sensor = start_sensor()
        x = 0
        while x <= 20:
            read(sensor, verbose=False)
            x += 1

    imu_data_stamped = {}    # dict. of dicts {timestamp : imu_data}, imu_data is alsp a dict.

    while cnt <= 9:

        try:
            imu_data = read(sensor, verbose=False)

            if (None, None, None) in imu_data.values():
                raise Exception('Nones found')

            elif (None, None, None, None) in imu_data.values():
                raise Exception ('Nones found in Quat')
#            pprint.pprint(imu_data)

        # Getting the current date
        # and time
            dt = datetime.datetime.now()

            utc_time = dt.replace(tzinfo = timezone.utc)
            timestamp = utc_time.timestamp()
        #print(utc_timestamp))

            imu_data_stamped[timestamp] = imu_data
            cnt += 1
            time.sleep(0.1)


        except Exception as e:
            print(e)
            pass

    if output_format=='json':
        imu_data_stamped = to_json(imu_data_stamped)


    #time.sleep(0.1)
    return imu_data_stamped

if __name__ == '__main__':
    sensor = start_sensor()

    while True:
        main()
