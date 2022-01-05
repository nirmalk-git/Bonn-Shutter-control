import serial
import serial.tools.list_ports as port_lists
# import time
import asyncio


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
async def list_ports():
    ports =   list(port_lists.comports())
    for p in ports: print(p)


# Initializing the serial port for communication
async def init_serialport(port_name, baud_rate, byte_size):
    serial_Port =   serial.Serial(
        port=port_name, baudrate=baud_rate, bytesize=byte_size, timeout=2, stopbits=serial.STOPBITS_ONE
    )
    await asyncio.sleep(2)
    return serial_Port


# this is to start an interactive session with the Bonn shutter
# The input is the initialised serial port
# this function should be called before communicating with the Bonn shutter

async def start_interactive_session(serialPort):
    print('Starting interactive session - - - -')
    if not serialPort.isOpen():
        serialPort.open()
    else:
        pass
    serialPort.write(b'ia 1 <CR> \r\n')
    await asyncio.sleep(5)

# Opening the ports
# The input is the initialised serial port
async def open_shutter(serialPort):
    print('opening shutter')
    if not serialPort.isOpen():
        serialPort.open()
    else:
        pass
    serialPort.write(b'os <CR> \r\n')
    await asyncio.sleep(2)
    return


# Closing the port
# input is the initialized serial port
async def close_shutter(serialPort):
    print('closing shutter')
    if not serialPort.isOpen():
        serialPort.open()
    else:
        pass
    serialPort.write(b'cs <CR> \r\n')
    await asyncio.sleep(2)
    return

# Resetting everything to the factory default value
async def reset_fd(serialPort):
    # Reset everything to factory default
    print('Resetting everything to factory default value')
    if not serialPort.isOpen():
        serialPort.open()
    else:
        pass
    serialPort.write(b'fd <CR> \r\n')
    await asyncio.sleep(2)

# set the exposure time
async def set_exposure_time(serialPort, exp_time):
    # exp_time is the shutter open time
    print('Setting exposure time as', exp_time, 'ms')
    if not serialPort.isOpen():
        serialPort.open()
    if exp_time <= 1000:
        serialPort.write(b'ex ' + str(exp_time).encode('Ascii') + b'<CR> \r\n')
        await asyncio.sleep(2)
    else:
        await open_shutter(serialPort)
        await asyncio.sleep((exp_time / 1000))
        await close_shutter(serialPort)



async def main():
    await list_ports()
    serialPort = await init_serialport('COM7', 19200, 8)
    await start_interactive_session(serialPort)
    await open_shutter(serialPort)
    await close_shutter(serialPort)
    await set_exposure_time(serialPort, 5000)
    await reset_fd(serialPort)


asyncio.run(main())
# serialPort = init_serialport('COM7', 19200, 8)


'''start_interactive_session(serialPort)
open_shutter(serialPort)
close_shutter(serialPort)
set_exposure_time(serialPort, 100)'''
