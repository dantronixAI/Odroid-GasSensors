import serial
import time
import datetime

def get2sComplementLong(HSB, MSB, LSB):
    k = (2 ** 24) - 1
    complement2 = HSB*(2**16)+MSB*(2**8) + LSB
    if HSB >= 0x20:
        complement2 = complement2 - k - 1
    return complement2

def get_Values():
    isGoodO3 = False
    isGoodCO = False
    while not (isGoodCO and isGoodO3):
        try:
            ser_OZONE_2_CLICK.write(OZONE_2_CLICK_address)
            data = ser_OZONE_2_CLICK.read(3)

            if (data[0] >= 0x40):
                time.sleep(1)
                print('O3 sensor not hot enough')
                isGoodO3 = False
            else:
                O3 = get2sComplementLong(data[0], data[1], data[2])
                isGoodO3 = True
        except:
            print('Error - O3')
        try:
            ser_SPEC_CO.write(SPEC_CO_address)
            data = ser_SPEC_CO.readline()
            data = data.decode("ascii")
            data = data.split(",")
            CO = int(data[4])
            Temp = int(data[2])
            RH = int(data[3])
            isGoodCO = True
        except:
            print('Error - CO')
        if isGoodO3 & isGoodCO:
            now = datetime.datetime.now()
            Data1 = 'O3: ' + str(O3) + ' * '
            Data2 = 'CO: ' + str(CO) + ' * '
            Data3 = 'RH: ' + str(RH) + ' % * '
            Data4 = 'T: ' + str(Temp) + ' C * '
            DATES = now.strftime("%Y-%m-%d")
            TIMES = now.strftime(" %H:%M:%S")
            print(Data1 + Data2 + Data3 + Data4 + 'Date : ' + DATES + ' ' + TIMES)
            Data = {"O3": O3, 'CO': CO, 'RH': RH, 'T': Temp, 'DATE': DATES, 'TIME': TIMES}
    return Data


O3_bridge = 'dev/ttyUSB1' # USB1 usb-to-serial bridge
CO_bridge = '/dev/ttyUSB0' # USB0 usb-to-serial bridge

ser_OZONE_2_CLICK = serial.Serial(O3_bridge, 115200, timeout=1)
ser_SPEC_CO = serial.Serial(CO_bridge, 9600, timeout=1)
OZONE_2_CLICK_address = b'\x42'
SPEC_CO_address = b'\r\n'

while True:
    Data=get_Values(ser_OZONE_2_CLICK ,ser_SPEC_CO,OZONE_2_CLICK_address,SPEC_CO_address)
    
