import asyncio
import serial


class shutter:
    # class attributes

    def __init__(self, port_name):
        self.port_name = port_name
        self.Baud_rate = 19200
        self.Bits_per_byte = 8
        self.Stop_bits = 1
        self.serialPort = serial.Serial(
            port=self.port_name,
            baudrate=self.Baud_rate,
            bytesize=self.Bits_per_byte,
            timeout=2,
            stopbits=serial.STOPBITS_ONE,
        )

    async def start_interactive_session(self):
        print("Starting interactive session - - - -")
        if not self.serialPort.isOpen():
            self.serialPort.open()
        else:
            pass
        self.serialPort.write(b"ia 1 <CR> \r\n")
        await asyncio.sleep(5)

    # Opening the ports
    # The input is the initialised serial port
    async def open_shutter(self):
        print("opening shutter")
        if not self.serialPort.isOpen():
            self.serialPort.open()
        else:
            pass
        self.serialPort.write(b"os <CR> \r\n")
        await asyncio.sleep(2)
        return

    # Closing the port
    # input is the initialized serial port
    async def close_shutter(self):
        print("closing shutter")
        if not self.serialPort.isOpen():
            self.serialPort.open()
        else:
            pass
        self.serialPort.write(b"cs <CR> \r\n")
        await asyncio.sleep(2)
        return

    # Resetting everything to the factory default value
    async def reset_fd(self):
        # Reset everything to factory default
        print("Resetting everything to factory default value")
        if not self.serialPort.isOpen():
            self.serialPort.open()
        else:
            pass
        self.serialPort.write(b"fd <CR> \r\n")
        await asyncio.sleep(2)

    # set the exposure time
    async def set_exposure_time(self, exp_time):
        # exp_time is the shutter open time
        print("Setting exposure time as", exp_time, "ms")
        if not self.serialPort.isOpen():
            self.serialPort.open()
        if exp_time <= 1000:
            self.serialPort.write(b"ex " + str(exp_time).encode("Ascii") + b"<CR> \r\n")
            await asyncio.sleep(2)
        else:
            await self.open_shutter()
            await asyncio.sleep((exp_time / 1000))
            await self.close_shutter()


# initialize the class
async def main():
    Bonn_shutter = shutter("COM7")
    await Bonn_shutter.start_interactive_session()
    await Bonn_shutter.open_shutter()
    await Bonn_shutter.close_shutter()
    await Bonn_shutter.set_exposure_time(300)


asyncio.run(main())
