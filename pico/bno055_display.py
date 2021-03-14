# Reads BNO055  9DoF IMU and sends Orentation (Euler angles) data over USB and to a LCD display.  
# The LCD display is independent of the USB connection so the orentation data can be read with 
# only power to the board. 

# Runs under Circuit Python on PICO Raspberrypi

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

#Copyright 2021 Ward Hills 

import time
import board

#for the bno055
import busio
import adafruit_bno055


# Use these lines for I2C
SDA = board.GP16
SCL = board.GP17

#i2c = busio.I2C(board.SCL, board.SDA)
i2c = busio.I2C(SCL,SDA)
print(i2c)

#i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

# User these lines for UART
# uart = busio.UART(board.TX, board.RX)
# sensor = adafruit_bno055.BNO055_UART(uart)

last_val = 0xFFFF


def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result


def decdeg2dms(dd):
    mnt,sec = divmod(dd*3600,60)
    deg,mnt = divmod(mnt,60)
    return deg,mnt,sec



# ---------------------------------------------------

#for the lcd
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2


# Pico Pin Config:
lcd_rs = digitalio.DigitalInOut(board.GP8)
lcd_en = digitalio.DigitalInOut(board.GP9)
lcd_d7 = digitalio.DigitalInOut(board.GP13)
lcd_d6 = digitalio.DigitalInOut(board.GP12)
lcd_d5 = digitalio.DigitalInOut(board.GP11)
lcd_d4 = digitalio.DigitalInOut(board.GP10)
lcd_backlight = digitalio.DigitalInOut(board.GP14)

# Initialise the LCD class
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
)


while True:

#    print("Temperature: {} degrees C".format(sensor.temperature))
#    """
#    print(
#        "Temperature: {} degrees C".format(temperature())
#    )  # Uncomment if using a Raspberry Pi
#    """
#    print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
#    print("Magnetometer (microteslas): {}".format(sensor.magnetic))
#    print("Gyroscope (rad/sec): {}".format(sensor.gyro))
#    print("Euler angle: {}".format(sensor.euler))
#    print("Quaternion: {}".format(sensor.quaternion))
#    print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
#    print("Gravity (m/s^2): {}".format(sensor.gravity))
#    print()

#send the data over the serial (USB) port
    print('X:',sensor.euler[0], '  Y:',sensor.euler[1], '  Z:',sensor.euler[2])

# send the data to the lcd screen
# the LCD screen is connected directly to the microcontroller board so that when powered it can be used with out the Pi
    # Turn backlight on
    lcd.backlight = True
    # Print a two line message
    #lcd.message = "Hello\nCircuitPython"
    nl = "\n"

# average the values before displaying
    cnt=1
    n = 100         # number of samples to average 
    az_list = []
    alt_list = []

    while cnt <= n+1:
        az_list.append(sensor.euler[0])
        alt_list.append(sensor.euler[1])
        cnt +=1
    az_ave  = sum(az_list)/n
    alt_ave = sum(alt_list)/n

    #az = str(sensor.euler[0])
    #alt = str(sensor.euler[1])
    #lcd.message =az+nl+alt

#change to deg min and sec
    #az_dms = decdeg2dms(sensor.euler[0])   #use this to display raw data , no average  
    az_dms = decdeg2dms(az_ave)
    az =  str(az_dms[0])+" "+str(az_dms[1])+" "+str(az_dms[2])

    #alt_dms = decdeg2dms(sensor.euler[1])  #use this to display raw data , no average 
    alt_dms = decdeg2dms(alt_ave)
    alt =  str(alt_dms[0])+" "+str(alt_dms[1])+" "+str(alt_dms[2])

    lcd.message =az+nl+alt