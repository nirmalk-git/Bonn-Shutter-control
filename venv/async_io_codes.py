import serial
import serial.tools.list_ports as port_lists
import time


# Bonn shutter serial communication setup
# Baudrate 19200
# Bits per byte 8
# Stop bits 1
# Parity no
# Protocol none

# Commands of the Bonns shutter
# os - open shutter
# cs - close shutter
# sh - shows an explanatory list of the velocity parameters
# ex 1000 - Perform 1000ms exposure
# ex 100 - Perform 100ms exposure
# fd - reset all parameters to factory reset
# rs - Wait till the blades have reached their destination


# Get the list of available serial ports
def list_ports():
    ports = list(port_lists.comports())
    for p in ports: print(p)


# Initializing the serial port for communication
def init_serialport(port_name, baud_rate, byte_size):
    serial_Port = serial.Serial(
        port=port_name, baudrate=baud_rate, bytesize=byte_size, timeout=2, stopbits=serial.STOPBITS_ONE
    )
    time.sleep(2)
    return serial_Port


# this is to start an interactive session with the Bonn shutter
# The input is the initialised serial port
# this function should be called before communicating with the Bonn shutter
def start_interactive_session(serialPort):
    print('Starting interactive session - - - -')
    if not serialPort.isOpen():
        serialPort.open()
    else:
        pass
    serialPort.write(b'ia 1 <CR> \r\n')
    time.sleep(5)


# Opening the ports
# The input is the initialised serial port
def open_shutter(serialPort):
    print('opening shutter')
    if not serialPort.isOpen():
        serialPort.open()
    else:
        pass
    serialPort.write(b'os <CR> \r\n')
    time.sleep(2)
    return


# Closing the port
# input is the initialized serial port
def close_shutter(serialPort):
    print('closing shutter')
    if not serialPort.isOpen():
        serialPort.open()
    else:
        pass
    serialPort.write(b'cs <CR> \r\n')
    time.sleep(2)
    return


# Resetting everything to the factory default value
def reset_fd(serialPort):
    # Reset everything to factory default
    print('Resetting everything to factory default value')
    if not serialPort.isOpen():
        serialPort.open()
    else:
        pass
    serialPort.write(b'fd <CR> \r\n')


# set the exposure time
def set_exposure_time(serialPort, exp_time):
    # exp_time is the shutter open time
    print('Setting exposure time as', exp_time, 'ms')
    if not serialPort.isOpen():
        serialPort.open()
    if exp_time <= 1000:
        serialPort.write(b'ex ' + str(exp_time).encode('Ascii') + b'<CR> \r\n')
        time.sleep(2)
    else:
        open_shutter(serialPort)
        time.sleep((exp_time / 1000))
        close_shutter(serialPort)


list_ports()
serialPort = init_serialport('COM7', 19200, 8)
start_interactive_session(serialPort)
open_shutter(serialPort)
close_shutter(serialPort)
set_exposure_time(serialPort, 100)
